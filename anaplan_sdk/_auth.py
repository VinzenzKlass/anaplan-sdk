import logging
import os
from base64 import b64encode
from typing import Callable

import httpx

from ._oauth import _OAuthRequestFactory
from .exceptions import AnaplanException, InvalidCredentialsException, InvalidPrivateKeyException

logger = logging.getLogger("anaplan_sdk")


class _AnaplanAuth(httpx.Auth):
    requires_response_body = True

    def __init__(self, token: str | None = None):
        self._token: str = token or ""
        if not token:
            logger.info("Creating Authentication Token.")
            with httpx.Client(timeout=15.0) as client:
                self._parse_auth_response(client.send(self._build_auth_request()))

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
        self._token = response.json()["tokenInfo"]["tokenValue"]


class _StaticTokenAuth(httpx.Auth):
    def __init__(self, token: str):
        self._token = token

    def auth_flow(self, request):
        request.headers["Authorization"] = f"AnaplanAuthToken {self._token}"
        response = yield request
        if response.status_code == 401:
            raise InvalidCredentialsException("Token is invalid or expired.")


class _AnaplanBasicAuth(_AnaplanAuth):
    def __init__(self, user_email: str, password: str, token: str | None = None):
        self.user_email = user_email
        self.password = password
        super().__init__(token)

    def _build_auth_request(self) -> httpx.Request:
        cred = b64encode(f"{self.user_email}:{self.password}".encode()).decode()
        return httpx.Request(
            method="post",
            url="https://auth.anaplan.com/token/authenticate",
            headers={"Authorization": f"Basic {cred}"},
        )


class _AnaplanCertAuth(_AnaplanAuth):
    requires_request_body = True

    def __init__(
        self,
        certificate: str | bytes,
        private_key: str | bytes,
        private_key_password: str | bytes | None = None,
        token: str | None = None,
    ):
        self.__set_certificate(certificate)
        self.__set_private_key(private_key, private_key_password)
        super().__init__(token)

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


class AnaplanLocalOAuth(_AnaplanAuth):
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        token: dict[str, str] | None = None,
        persist_token: bool = False,
        authorization_url: str = "https://us1a.app.anaplan.com/auth/prelogin",
        token_url: str = "https://us1a.app.anaplan.com/oauth/token",
        validation_url: str = "https://auth.anaplan.com/token/validate",
        scope: str = "openid profile email offline_access",
        state_generator: Callable[[], str] | None = None,
    ):
        """
        Initializes the AnaplanLocalOAuth class for OAuth2 authentication using the
        Authorization Code Flow. This is a utility class for local development and requires user
        interaction. For Web Applications and other scenarios, refer to `Oauth` or `AsyncOauth`.
        This class will refresh the access token automatically when it expires.
        :param client_id: The client ID of your Anaplan Oauth 2.0 application. This Application
               must be an Authorization Code Grant application.
        :param client_secret: The client secret of your Anaplan Oauth 2.0 application.
        :param redirect_uri: The URL to which the user will be redirected after authorizing the
               application.
        :param token: The OAuth token dictionary containing at least the `access_token` and
               `refresh_token`. If not provided, the user will be prompted to interactive
               authorize the application, if `persist_token` is set to False or no valid refresh
               token is found in the keyring.
        :param persist_token: If set to True, the refresh token will be stored in the system's
               keyring, allowing the application to use the same refresh token across multiple
               runs. If set to False, the user will be prompted to authorize the application each
               time. This requires the `keyring` extra to be installed. If a valid refresh token
               is found in the keyring, it will be used instead of the given `token` parameter.
        :param authorization_url: The URL to which the user will be redirected to authorize the
               application. Defaults to the Anaplan Prelogin Page, where the user can select the
               login method.
        :param token_url: The URL to post the authorization code to in order to fetch the access
               token.
        :param validation_url: The URL to validate the access token.
        :param scope: The scope of the access request.
        :param state_generator: A callable that generates a random state string. You can optionally
               pass this if you need to customize the state generation logic. If not provided,
               the state will be generated by `oauthlib`.
        """
        self._oauth_token = token or {}
        self._service_name = "anaplan_sdk"

        if persist_token:
            try:
                import keyring

                stored = keyring.get_password(self._service_name, self._service_name)
                if stored:
                    logger.info("Using persisted OAuth refresh token.")
                    self._oauth_token = {"refresh_token": stored}
                    self._token = ""  # Set to blank to trigger the super().__init__ auth request.
            except ImportError as e:
                raise AnaplanException(
                    "keyring is not available. Please install anaplan-sdk with the keyring extra "
                    "`pip install anaplan-sdk[keyring]` or install keyring separately."
                ) from e
        self._persist_token = persist_token
        self._oauth = _OAuthRequestFactory(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=scope,
            authorization_url=authorization_url,
            token_url=token_url,
            validation_url=validation_url,
            state_generator=state_generator,
        )
        if not self._oauth_token:
            self.__auth_code_flow()
        super().__init__(self._token)

    @property
    def token(self) -> dict[str, str]:
        """
        Returns the current token dictionary. You can safely use the `access_token`, but if you
        must not use the `refresh_token` outside of this class, if you expect to use this instance
        further. If you do use the `refresh_token` outside of this class, this will error on the
        next attempt to refresh the token, as the `refresh_token` can only be used once.
        """
        return self._oauth_token

    def _build_auth_request(self) -> httpx.Request:
        return self._oauth.refresh_token_request(self._oauth_token["refresh_token"])

    def _parse_auth_response(self, response: httpx.Response) -> None:
        if response.status_code == 401:
            raise InvalidCredentialsException
        if not response.is_success:
            raise AnaplanException(f"Authentication failed: {response.status_code} {response.text}")
        self._oauth_token = response.json()
        if self._persist_token:
            import keyring

            keyring.set_password(
                self._service_name, self._service_name, self._oauth_token["refresh_token"]
            )
        self._token: str = self._oauth_token["access_token"]

    def __auth_code_flow(self):
        from oauthlib.oauth2 import OAuth2Error

        try:
            logger.info("Creating Authentication Token with OAuth2 Authorization Code Flow.")
            url, _ = self._oauth.authorization_url()
            authorization_response = input(
                f"Please go to {url} and authorize the app.\n"
                "Then paste the entire redirect URL here: "
            )
            with httpx.Client() as client:
                res = client.send(self._oauth.token_request(authorization_response))
            self._parse_auth_response(res)
        except (httpx.HTTPError, ValueError, TypeError, OAuth2Error) as error:
            raise InvalidCredentialsException("Error during OAuth2 authorization flow.") from error


class AnaplanRefreshTokenAuth(_AnaplanAuth):
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        token: dict[str, str],
        token_url: str = "https://us1a.app.anaplan.com/oauth/token",
    ):
        """
        This class is a utility class for long-lived `Client` or `AsyncClient` instances that use
        OAuth. This class will use the `access_token` until the first request fails with a 401
        Unauthorized error, at which point it will attempt to refresh the `access_token` using the
        `refresh_token`. If the refresh fails, it will raise an `InvalidCredentialsException`. The
        `expires_in` field in the token dictionary is not considered. Manipulating any of the
        fields in the token dictionary is not recommended and will likely have no effect.

        **For its entire lifetime, you are ceding control of the token to this class.**
        You must not use the same token simultaneously in multiple instances of this class or
        outside of it, as this may lead to unexpected behavior when e.g. the refresh token is
        used, which can only happen once and will lead to errors when attempting to use the same
        refresh token again elsewhere.

        If you need the token back before this instance is destroyed, you can use the `token`
        method.

        :param client_id: The client ID of your Anaplan Oauth 2.0 application. This Application
               must be an Authorization Code Grant application.
        :param client_secret: The client secret of your Anaplan Oauth 2.0 application.
        :param redirect_uri: The URL to which the user will be redirected after authorizing the
               application.
        :param token: The OAuth token dictionary containing at least the `access_token` and
               `refresh_token`.
        :param token_url: The URL to post the refresh token request to in order to fetch the access
               token.
        """
        if not isinstance(token, dict) or not all(
            key in token for key in ("access_token", "refresh_token")
        ):
            raise ValueError(
                "The token must at least contain 'access_token' and 'refresh_token' keys."
            )
        self._oauth_token = token
        self._oauth = _OAuthRequestFactory(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            token_url=token_url,
        )
        super().__init__(self._oauth_token["access_token"])

    @property
    def token(self) -> dict[str, str]:
        """
        Returns the current OAuth token. You can safely use the `access_token`, but you
        must not use the `refresh_token` outside of this class, if you expect to use this instance
        further. If you do use the `refresh_token` outside of this class, this will error on the
        next attempt to refresh the token, as the `refresh_token` can only be used once.
        """
        return self._oauth_token

    def _build_auth_request(self) -> httpx.Request:
        return self._oauth.refresh_token_request(self._oauth_token["refresh_token"])

    def _parse_auth_response(self, response: httpx.Response) -> None:
        if response.status_code == 401:
            raise InvalidCredentialsException
        if not response.is_success:
            raise AnaplanException(f"Authentication failed: {response.status_code} {response.text}")
        self._oauth_token = response.json()
        self._token: str = self._oauth_token["access_token"]


def _create_auth(
    user_email: str | None = None,
    password: str | None = None,
    certificate: str | bytes | None = None,
    private_key: str | bytes | None = None,
    private_key_password: str | bytes | None = None,
    token: str | None = None,
) -> httpx.Auth:
    if certificate and private_key:
        return _AnaplanCertAuth(certificate, private_key, private_key_password, token)
    if user_email and password:
        return _AnaplanBasicAuth(user_email, password, token)
    if token:
        return _StaticTokenAuth(token)
    raise ValueError(
        "No valid authentication parameters provided. Please provide either:\n"
        "- `user_email` and `password`, or\n"
        "- `certificate` and `private_key`\n"
    )
