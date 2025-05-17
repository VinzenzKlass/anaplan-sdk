import logging
import os
from base64 import b64encode
from typing import Callable

import httpx

from .exceptions import AnaplanException, InvalidCredentialsException, InvalidPrivateKeyException

logger = logging.getLogger("anaplan_sdk")


class _AnaplanAuth(httpx.Auth):
    requires_response_body = True

    def __init__(self, pre_authed: bool = False):
        if not pre_authed:
            logger.info("Creating Authentication Token.")
            with httpx.Client(timeout=15.0) as client:
                res = client.send(self._build_auth_request())
                self._parse_auth_response(res)

    def _build_auth_request(self) -> httpx.Request:
        raise NotImplementedError("Must be implemented in subclass.")

    def auth_flow(self, request):
        request.headers["Authorization"] = f"AnaplanAuthToken {self._token}"
        response = yield request
        if response.status_code == 401:
            logger.info("Token expired, refreshing.")
            auth_res = yield self._build_auth_request()
            self._parse_auth_response(auth_res)
            request.headers["Authorization"] = f"AnaplanAuthToken {self._token}"
            yield request

    def _parse_auth_response(self, response: httpx.Response) -> None:
        if response.status_code == 401:
            raise InvalidCredentialsException
        if not response.is_success:
            raise AnaplanException(f"Authentication failed: {response.status_code} {response.text}")
        self._token: str = response.json()["tokenInfo"]["tokenValue"]


class AnaplanBasicAuth(_AnaplanAuth):
    def __init__(self, user_email: str, password: str):
        self.user_email = user_email
        self.password = password
        super().__init__()

    def _build_auth_request(self) -> httpx.Request:
        cred = b64encode(f"{self.user_email}:{self.password}".encode()).decode()
        return httpx.Request(
            method="post",
            url="https://auth.anaplan.com/token/authenticate",
            headers={"Authorization": f"Basic {cred}"},
        )


class AnaplanCertAuth(_AnaplanAuth):
    requires_request_body = True

    def __init__(
        self,
        certificate: str | bytes,
        private_key: str | bytes,
        private_key_password: str | bytes | None = None,
    ):
        self.__set_certificate(certificate)
        self.__set_private_key(private_key, private_key_password)
        super().__init__()

    def _build_auth_request(self) -> httpx.Request:
        encoded_cert, encoded_string, encoded_signed_string = self._prep_credentials()
        return httpx.Request(
            method="post",
            url="https://auth.anaplan.com/token/authenticate",
            headers={
                "Authorization": f"CACertificate {encoded_cert}",
                "Content-Type": "application/json",
            },
            json={"encodedData": encoded_string, "encodedSignedData": encoded_signed_string},
        )

    def _prep_credentials(self) -> tuple[str, str, str]:
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15

        message = os.urandom(150)
        return (
            b64encode(self._certificate).decode(),
            b64encode(message).decode(),
            b64encode(self._private_key.sign(message, PKCS1v15(), hashes.SHA512())).decode(),
        )

    def __set_certificate(self, certificate: str | bytes) -> None:
        if isinstance(certificate, str):
            if os.path.isfile(certificate):
                with open(certificate, "rb") as f:
                    self._certificate = f.read()
            else:
                self._certificate = certificate.encode()
        else:
            self._certificate = certificate

    def __set_private_key(
        self, private_key: str | bytes, private_key_password: str | bytes
    ) -> None:
        try:
            from cryptography.exceptions import InvalidKey, UnsupportedAlgorithm
            from cryptography.hazmat.backends import default_backend
            from cryptography.hazmat.primitives import serialization
            from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
        except ImportError as e:
            raise AnaplanException(
                "cryptography is not available. Please install anaplan-sdk with the cert extra "
                "`pip install anaplan-sdk[cert]` or install cryptography separately."
            ) from e
        try:
            if isinstance(private_key, str):
                if os.path.isfile(private_key):
                    with open(private_key, "rb") as f:
                        data = f.read()
                else:
                    data = private_key.encode()
            else:
                data = private_key
            password = (
                private_key_password.encode()
                if isinstance(private_key_password, str)
                else private_key_password
            )
            self._private_key: RSAPrivateKey = serialization.load_pem_private_key(
                data, password, backend=default_backend()
            )
        except (IOError, InvalidKey, UnsupportedAlgorithm) as error:
            raise InvalidPrivateKeyException from error


class AnaplanOauth2AuthCodeAuth(_AnaplanAuth):
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        refresh_token: str | None = None,
        scope: str = "openid profile email offline_access",
        on_token_refresh: Callable[[dict[str, str]], None] | None = None,
    ):
        try:
            from oauthlib.oauth2 import WebApplicationClient
        except ImportError as e:
            raise AnaplanException(
                "oauthlib is not available. Please install anaplan-sdk with the oauth extra "
                "`pip install anaplan-sdk[oauth]` or install oauthlib separately."
            ) from e
        self._oauth = WebApplicationClient(
            client_id=client_id, client_secret=client_secret, refresh_token=refresh_token
        )
        self._token_url = "https://us1a.app.anaplan.com/oauth/token"
        self._client_id = client_id
        self._client_secret = client_secret
        self._redirect_uri = redirect_uri
        self._refresh_token = refresh_token
        self._scope = scope
        self._id_token = None
        self._on_token_refresh = on_token_refresh
        if not refresh_token:
            self.__auth_code_flow()
        super().__init__(pre_authed=not refresh_token)

    def _build_auth_request(self) -> httpx.Request:
        url, headers, body = self._oauth.prepare_refresh_token_request(
            token_url=self._token_url,
            refresh_token=self._refresh_token,
            client_secret=self._client_secret,
            client_id=self._client_id,
        )
        return httpx.Request(method="post", url=url, headers=headers, content=body)

    def _parse_auth_response(self, response: httpx.Response) -> None:
        if response.status_code == 401:
            raise InvalidCredentialsException
        if not response.is_success:
            raise AnaplanException(f"Authentication failed: {response.status_code} {response.text}")
        token = response.json()
        self._token = token["access_token"]
        self._refresh_token = token["refresh_token"]
        if self._on_token_refresh:
            self._on_token_refresh(token)
        self._id_token = token.get("id_token")

    def __auth_code_flow(self):
        from oauthlib.oauth2 import OAuth2Error

        try:
            logger.info("Creating Authentication Token with OAuth2 Authorization Code Flow.")
            url, _, _ = self._oauth.prepare_authorization_request(
                "https://us1a.app.anaplan.com/auth/authorize",
                redirect_url=self._redirect_uri,
                scope=self._scope,
            )
            authorization_response = input(
                f"Please go to {url} and authorize the app.\n"
                "Then paste the entire redirect URL here: "
            )
            url, headers, body = self._oauth.prepare_token_request(
                token_url=self._token_url,
                redirect_url=self._redirect_uri,
                authorization_response=authorization_response,
                client_secret=self._client_secret,
            )
            self._parse_auth_response(httpx.post(url=url, headers=headers, content=body))
        except (httpx.HTTPError, ValueError, TypeError, OAuth2Error) as error:
            raise AnaplanException("Error during OAuth2 authorization flow.") from error


def create_auth(
    user_email: str | None = None,
    password: str | None = None,
    certificate: str | bytes | None = None,
    private_key: str | bytes | None = None,
    private_key_password: str | bytes | None = None,
    client_id: str | None = None,
    client_secret: str | None = None,
    redirect_uri: str | None = None,
    refresh_token: str | None = None,
    oauth2_scope: str = "openid profile email offline_access",
    on_token_refresh: Callable[[dict[str, str]], None] | None = None,
) -> _AnaplanAuth:
    if certificate and private_key:
        return AnaplanCertAuth(certificate, private_key, private_key_password)
    if user_email and password:
        return AnaplanBasicAuth(user_email=user_email, password=password)
    if client_id and client_secret and redirect_uri:
        return AnaplanOauth2AuthCodeAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            refresh_token=refresh_token,
            scope=oauth2_scope,
            on_token_refresh=on_token_refresh,
        )
    raise ValueError(
        "No valid authentication parameters provided. Please provide either:\n"
        "- user_email and password, or\n"
        "- certificate and private_key, or\n"
        "- client_id, client_secret, and redirect_uri"
    )
