"""
Custom Authentication class to pass to httpx alongside some helper functions.
"""

import logging
import os
from base64 import b64encode

import httpx
from cryptography.exceptions import InvalidKey, UnsupportedAlgorithm
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey

from .exceptions import AnaplanException, InvalidCredentialsException, InvalidPrivateKeyException

logger = logging.getLogger("anaplan_sdk")


class _AnaplanAuth(httpx.Auth):
    requires_response_body = True

    def __init__(self):
        self._auth_request = self._build_auth_request()
        logger.info("Creating Authentication Token.")
        with httpx.Client(timeout=15.0) as client:
            res = client.send(self._auth_request)
            self._parse_auth_response(res)

    def _build_auth_request(self) -> httpx.Request:
        raise NotImplementedError("Must be implemented in subclass.")

    def auth_flow(self, request):
        request.headers["Authorization"] = f"AnaplanAuthToken {self._token}"
        response = yield request
        if response.status_code == 401:
            logger.info("Token expired, refreshing.")
            auth_res = yield self._auth_request
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

    def __init__(self, certificate: bytes, private_key: RSAPrivateKey):
        self._certificate = certificate
        self._private_key = private_key
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
        message = os.urandom(150)
        return (
            b64encode(self._certificate).decode(),
            b64encode(message).decode(),
            b64encode(self._private_key.sign(message, PKCS1v15(), hashes.SHA512())).decode(),
        )


class AnaplanOauth2AuthCodeAuth(_AnaplanAuth):
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        auth_code: str | None = None,
        refresh_token: str | None = None,
    ):
        try:
            from oauthlib.oauth2 import Client
        except ImportError as e:
            raise AnaplanException(
                "oauthlib is not available. Please install anaplan-sdk with the oauth extra "
                "`pip install anaplan-sdk[oauth]` or install oauthlib separately."
            ) from e
        self._oauth = Client(
            client_id=client_id, client_secret=client_secret, refresh_token=refresh_token
        )
        self._client_id = client_id
        self._client_secret = client_secret
        self._redirect_uri = redirect_uri
        self._auth_code = auth_code
        self._refresh_token = refresh_token
        self._oauth.prepare_token_request()
        super().__init__()

    def _build_auth_request(self) -> httpx.Request:
        url, headers, body = self._oauth.prepare_refresh_token_request(
            token_url="https://us1a.app.anaplan.com/oauth/token", refresh_token=self._refresh_token
        )
        return httpx.Request(method="post", url=url, headers=headers, data=body)

    def _parse_auth_response(self, response: httpx.Response) -> None:
        if response.status_code == 401:
            raise InvalidCredentialsException
        if not response.is_success:
            raise AnaplanException(f"Authentication failed: {response.status_code} {response.text}")
        token = response.json()
        self._token: str = token["access_token"]
        self._refresh_token = token.get("refresh_token")


def get_certificate(certificate: str | bytes) -> bytes:
    """
    Get the certificate from a file or string.
    :param certificate: The certificate to use.
    :return: The certificate as bytes.
    """
    if isinstance(certificate, str):
        if os.path.isfile(certificate):
            with open(certificate, "rb") as f:
                return f.read()
        return certificate.encode()
    return certificate


def get_private_key(private_key: str | bytes, private_key_password: str | bytes) -> RSAPrivateKey:
    """
    Get the private key from a file or string.
    :param private_key: The private key to use.
    :param private_key_password: The password for the private key.
    :return: The private key as an RSAPrivateKey object.
    """
    try:
        if isinstance(private_key, str):
            if os.path.isfile(private_key):
                with open(private_key, "rb") as f:
                    data = f.read()
            else:
                data = private_key.encode()
        else:
            data = private_key

        password = None
        if private_key_password:
            if isinstance(private_key_password, str):
                password = private_key_password.encode()
            else:
                password = private_key_password
        return serialization.load_pem_private_key(data, password, backend=default_backend())
    except (IOError, InvalidKey, UnsupportedAlgorithm) as error:
        raise InvalidPrivateKeyException from error
