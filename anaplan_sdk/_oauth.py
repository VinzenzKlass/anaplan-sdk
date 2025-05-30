import logging
from typing import Callable

import httpx

from .exceptions import AnaplanException, InvalidCredentialsException

logger = logging.getLogger("anaplan_sdk")


class _BaseOauth:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_url: str,
        authorization_url: str = "https://us1a.app.anaplan.com/auth/prelogin",
        token_url: str = "https://us1a.app.anaplan.com/oauth/token",
        scope: str = "openid profile email offline_access",
        state_generator: Callable[[], str] | None = None,
    ):
        """
        Initializes the OAuth Client. This class provides the two utilities needed to implement
        the OAuth 2.0 authorization code flow for user-facing Web Applications. It differs from the
        other Authentication Strategies in this SDK in two main ways:

        1. You must implement the actual authentication flow in your application. You cannot pass
        the credentials directly to the `Client` or `AsyncClient`, and this class does not
        implement the SDK internal authentication flow, i.e. it does not subclass `httpx.Auth`.

        2. You then simply pass the resulting token to the `Client` or `AsyncClient`, rather than
        passing the credentials directly, which will internally construct an `httpx.Auth` instance

        Note that this class exist for convenience only, and you can implement the OAuth 2.0 Flow
        yourself in your preferred library, or bring an existing implementation. For details on the
        Anaplan OAuth 2.0 Flow, see the [the Docs](https://anaplanoauth2service.docs.apiary.io/#reference/overview-of-the-authorization-code-grant)
        :param client_id:
        :param client_secret:
        :param redirect_url:
        :param authorization_url:
        :param token_url:
        :param scope:
        """
        self._client_id = client_id
        self._client_secret = client_secret
        self._redirect_url = redirect_url
        self._authorization_url = authorization_url
        self._token_url = token_url
        self._scope = scope

        try:
            from oauthlib.oauth2 import WebApplicationClient
        except ImportError as e:
            raise AnaplanException(
                "oauthlib is not available. Please install anaplan-sdk with the oauth extra "
                "`pip install anaplan-sdk[oauth]` or install oauthlib separately."
            ) from e
        self._oauth = WebApplicationClient(client_id=client_id, client_secret=client_secret)
        self._state_generator = state_generator or self._oauth.state_generator

    def authorization_url(
        self, authorization_url: str | None = None, state: str | None = None
    ) -> tuple[str, str]:
        auth_url = authorization_url or self._authorization_url
        state = state or self._state_generator()
        url = self._oauth.prepare_authorization_request(
            auth_url, state, self._redirect_url, self._scope
        )
        return url, state


class AsyncOauth(_BaseOauth):
    async def fetch_token(self, authorization_response: str) -> dict[str, str]:
        from oauthlib.oauth2 import OAuth2Error

        try:
            url, headers, body = self._oauth.prepare_token_request(
                authorization_response=authorization_response,
                token_url=self._token_url,
                redirect_url=self._redirect_url,
            )
            with httpx.AsyncClient() as client:
                response = await client.post(url=url, headers=headers, content=body)
            if not response.is_success:
                raise AnaplanException(
                    f"Token request failed: {response.status_code} {response.text}"
                )
            return response.json()
        except (httpx.HTTPError, ValueError, TypeError, OAuth2Error) as error:
            raise InvalidCredentialsException("Error during token fetching.") from error


class Oauth(_BaseOauth):
    def fetch_token(self, authorization_response: str) -> dict[str, str]:
        from oauthlib.oauth2 import OAuth2Error

        try:
            url, headers, body = self._oauth.prepare_token_request(
                authorization_response=authorization_response,
                token_url=self._token_url,
                redirect_url=self._redirect_url,
            )
            with httpx.Client() as client:
                response = client.post(url=url, headers=headers, content=body)
            if not response.is_success:
                raise AnaplanException(
                    f"Token request failed: {response.status_code} {response.text}"
                )
            return response.json()
        except (httpx.HTTPError, ValueError, TypeError, OAuth2Error) as error:
            raise InvalidCredentialsException("Error during token fetching.") from error
