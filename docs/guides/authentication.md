# Authentication

There are three main ways to authenticate with Anaplan.

- Basic Authentication
- Certificate Authentication
- OAuth2

Anaplan SDK supports all of them, though Basic Authentication is strictly not recommended for production use.
Certificate
Authentication is currently the most suitable for production use, since the Anaplan OAuth 2.0 implementation does not
support the `client_credentials` grant type. This means you will have to manually manage the Refresh Token.

## Basic Authentication

Basic Authentication is the simplest way to authenticate with Anaplan. It is unsuitable for Production. Anaplan password
policies force password changes every 30, 60 or 90 days, depending on tenant settings, making this approach annoying to
maintain and error-prone.

=== "Synchronous"
    ```python
    import anaplan_sdk

    anaplan = anaplan_sdk.Client(
        workspace_id="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
        model_id="11111111111111111111111111111111",
        user_email="admin@company.com",
        password="my_super_secret_password",
    )
    ```

=== "Asynchronous"
    ```python
    import anaplan_sdk

    anaplan = anaplan_sdk.AsyncClient(
        workspace_id="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
        model_id="11111111111111111111111111111111",
        user_email="admin@company.com",
        password="my_super_secret_password",
    )
    ```

## Certificate Authentication

Certificate Authentication is the most suitable for production use. It uses an X.509 S/MIME Certificate (aka. Client Certificate or HTTPS-Certificate) and Private Key. The Process of acquiring such a certificate is well [documented](https://help.anaplan.com/procure-ca-certificates-47842267-2cb3-4e38-90bf-13b1632bcd44). Anaplan does not support self-signed certificates, so you will need to procure a certificate from a trusted Certificate Authority (CA).

??? tip "Requires Extra"
    If you want to use certificate authentication, you need to install the `cert` extra:
    === "pip"
        ```shell
        pip install anaplan-sdk[cert]
        ```
    ===+ "uv"
        ```shell
        uv add anaplan-sdk[cert]
        ```
    === "Poetry"
        ```shell
        poetry add anaplan-sdk[cert]
        ```
    This will install [cryptography](https://github.com/pyca/cryptography) to securely construct the authentication request.

=== "Synchronous"
    ```python
    import anaplan_sdk

    anaplan = anaplan_sdk.Client(
        workspace_id="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
        model_id="11111111111111111111111111111111",
        certificate="~/certs/anaplan.pem",
        private_key="~/keys/anaplan.pem",
        private_key_password="my_super_secret_password", # Optional
    )
    ```
=== "Asynchronous"
    ```python
    import anaplan_sdk

    anaplan = anaplan_sdk.AsyncClient(
        workspace_id="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
        model_id="11111111111111111111111111111111",
        certificate="~/certs/anaplan.pem",
        private_key="~/keys/anaplan.pem",
        private_key_password="my_super_secret_password", # Optional
    )
    ```



## OAuth for Web Applications

If you are building a Web Application and intend to have your users authenticate with Anaplan, you can use the `Oauth`
or `AsyncOauth` classes. These classes provide the necessary utilities to handle the Oauth2 `authorization_code` grant,
in which the authentication flow must occur outside the SDK for the user to log in.

These Classes exist for convenience only, and you can use any other Library to handle the Oauth2 flow.

An example for FastAPI is shown below, but you can use any other Web Framework.

??? tip "Requires Extra"
    If you want to use OAuth2 authentication, you need to install the `oauth` extra:
    === "pip"
        ```shell
        pip install anaplan-sdk[oauth]
        ```
    ===+ "uv"
        ```shell
        uv add anaplan-sdk[oauth]
        ```
    === "Poetry"
        ```shell
        poetry add anaplan-sdk[oauth]
        ```
    This will install [OAuthLib](https://oauthlib.readthedocs.io/en/latest/index.html) to securely construct the authentication request.


```python
import os
from typing import Annotated

from fastapi import FastAPI, HTTPException, Request, Security
from fastapi.responses import RedirectResponse

from anaplan_sdk import AsyncClient, AsyncOauth, exceptions

_oauth = AsyncOauth(
    client_id=os.environ["OAUTH_CLIENT_ID"],
    client_secret=os.environ["OAUTH_CLIENT_SECRET"],
    redirect_url="https://vinzenzklass.github.io/anaplan-sdk/oauth/callback",
)

app = FastAPI()


@app.get("/login")
async def login():
    # TODO: Store the state for subsequent validation.
    url, state = _oauth.authorization_url()
    return RedirectResponse(url, status_code=302)


@app.get("/oauth/callback")
async def oauth_callback(req: Request):
    # TODO: Validate the state and handle the token.
    token = await _oauth.fetch_token(str(req.url))
    return RedirectResponse("/home", status_code=303)


async def _validate_session(
        token: Annotated[dict[str, str], Security(...)],
) -> AsyncClient:
    # TODO: Implement the Security scheme.
    await _oauth.validate_token(token["access_token"])
    return AsyncClient(oauth_token=token)


@app.get("/profile")
async def profile(anaplan: Annotated[AsyncClient, Security(_validate_session)]):
    return await anaplan.audit.get_user("me")


@app.exception_handler(exceptions.InvalidCredentialsException)
async def invalid_credentials_exception_handler(_, __):
    raise HTTPException(
        status_code=401, detail="Invalid or expired Credentials."
    )
```


## OAuth for Local Applications

For local applications, the `Client` or `AsyncClient` classes can be used directly to handle the OAuth2 flow.

??? tip "Requires Extra"
    If you want to use OAuth2 authentication, you need to install the `oauth` extra:
    === "pip"
        ```shell
        pip install anaplan-sdk[oauth]
        ```
    ===+ "uv"
        ```shell
        uv add anaplan-sdk[oauth]
        ```
    === "Poetry"
        ```shell
        poetry add anaplan-sdk[oauth]
        ```
    This will install [OAuthLib](https://oauthlib.readthedocs.io/en/latest/index.html) to securely construct the authentication request.

=== "Synchronous"
    ```python
    import anaplan_sdk

    anaplan = anaplan_sdk.Client(
        workspace_id="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
        model_id="11111111111111111111111111111111",
        redirect_uri="https://vinzenzklass.github.io/anaplan-sdk",
        client_id="my_anaplan_oauth_client_id",
        client_secret="my_anaplan_oauth_client_secret",
    )
    ```
=== "Asynchronous"
    ```python
    import anaplan_sdk
    
    anaplan = anaplan_sdk.AsyncClient(
        workspace_id="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
        model_id="11111111111111111111111111111111",
        redirect_uri="https://vinzenzklass.github.io/anaplan-sdk",
        client_id="my_anaplan_oauth_client_id",
        client_secret="my_anaplan_oauth_client_secret",
    )
    ```

With these parameters, the SDK will prompt you to open the login URI in your browser. After you have logged in, you 
will need to copy the entire redirect URI from your browser and paste it into the terminal.

???+ info "Why do I need to copy the redirect URI?"
    Unfortunately, registering localhost redirect URIs is not supported by Anaplan. This means we cannot intercept the
    redirect URI and extract the `authorization_code` automatically. This is a limitation of Anaplan's OAuth2 implementation. See [this Community Note](https://community.anaplan.com/discussion/156599/oauth-rediredt-url-port-for-desktop-apps).
