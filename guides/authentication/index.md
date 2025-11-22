# Authentication

There are three main ways to authenticate with Anaplan.

- Basic Authentication
- Certificate Authentication
- OAuth2

Anaplan SDK supports all of them, though Basic Authentication is strictly not recommended for production use. Certificate Authentication is currently the most suitable for production use, since the Anaplan OAuth 2.0 implementation does not support the `client_credentials` grant type. This means you will have to manually manage the refresh Token if you choose to use OAuth2.

## Basic Authentication

Basic Authentication is the simplest way to authenticate with Anaplan. It is unsuitable for Production. Anaplan password policies force password changes every 30, 60 or 90 days, depending on tenant settings, making this approach annoying to maintain and error-prone.

```
import anaplan_sdk

anaplan = anaplan_sdk.Client(
    workspace_id="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    model_id="11111111111111111111111111111111",
    user_email="admin@company.com",
    password="my_super_secret_password",
)
```

```
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

Requires Extra

If you want to use certificate authentication, you need to install the `cert` extra:

```
pip install anaplan-sdk[cert]
```

```
uv add anaplan-sdk[cert]
```

```
poetry add anaplan-sdk[cert]
```

This will install [cryptography](https://github.com/pyca/cryptography) to securely construct the authentication request.

```
import anaplan_sdk

anaplan = anaplan_sdk.Client(
    workspace_id="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    model_id="11111111111111111111111111111111",
    certificate="~/certs/anaplan.pem",
    private_key="~/keys/anaplan.pem",
    private_key_password="my_super_secret_password", # Optional
)
```

```
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

If you are building a Web Application and intend to have your users authenticate with Anaplan, you can use the `Oauth` or `AsyncOauth` classes. These classes provide the necessary utilities to handle the Oauth2 `authorization_code` grant, in which the authentication flow must occur outside the SDK for the user to log in.

These Classes exist for convenience only, and you can use any other Library to handle the Oauth2 flow.

A minimal, illustrative example for FastAPI is shown below, but you can use any other Web Framework. This will not run until you implement the TODOs in a suitable way for your purpose.

Requires Extra

If you want to use OAuth2 authentication, you need to install the `oauth` extra:

```
pip install anaplan-sdk[oauth]
```

```
uv add anaplan-sdk[oauth]
```

```
poetry add anaplan-sdk[oauth]
```

This will install [OAuthLib](https://oauthlib.readthedocs.io/en/latest/index.html) to securely construct the authentication request.

```
import os
from typing import Annotated

from fastapi import FastAPI, HTTPException, Request, Security
from fastapi.responses import RedirectResponse

from anaplan_sdk import AsyncClient, AsyncOauth, exceptions

_oauth = AsyncOauth(
    client_id=os.environ["OAUTH_CLIENT_ID"],
    client_secret=os.environ["OAUTH_CLIENT_SECRET"],
    redirect_uri="https://vinzenzklass.github.io/anaplan-sdk/oauth/callback",
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
    # TODO: Refresh the token if it is expired.
    token = await _oauth.refresh_token(token["refresh_token"])
    await _oauth.validate_token(token["access_token"])
    return AsyncClient(token=token["access_token"])


@app.get("/profile")
async def profile(anaplan: Annotated[AsyncClient, Security(_validate_session)]):
    return await anaplan.audit.get_user("me")


@app.exception_handler(exceptions.InvalidCredentialsException)
async def invalid_credentials_exception_handler(_, __):
    raise HTTPException(
        status_code=401, detail="Invalid or expired Credentials."
    )
```

Note that we're only passing the `access_token` to the `AsyncClient`. This is the recommended way to instantiate short-lived instances such as in this example, since it has virtually no overhead. It will however not handle token expiration or refresh, so you will need to handle that yourself. If you expect long-lived instances, you can pass an instance of `AnaplanRefreshTokenAuth`. This will use the existing token to authenticate and will refresh the token when it expires.

```
anaplan = Client(
    auth=AnaplanRefreshTokenAuth(
        token=token,
        client_id=os.environ["OAUTH_CLIENT_ID"],
        client_secret=os.environ["OAUTH_CLIENT_SECRET"],
        redirect_uri="https://vinzenzklass.github.io/anaplan-sdk",
    )
)
```

```
anaplan = AsyncClient(
    auth=AnaplanRefreshTokenAuth(
        token=token,
        client_id=os.environ["OAUTH_CLIENT_ID"],
        client_secret=os.environ["OAUTH_CLIENT_SECRET"],
        redirect_uri="https://vinzenzklass.github.io/anaplan-sdk",
    )
)
```

## OAuth for Local Applications

For local applications, you can use `AnaplanLocalOAuth` Class to handle the initial Oauth2 `authorization_code` flow and the subsequent token refreshes.

Requires Extra

If you want to use OAuth2 authentication, you need to install the `oauth` extra:

```
pip install anaplan-sdk[oauth]
```

```
uv add anaplan-sdk[oauth]
```

```
poetry add anaplan-sdk[oauth]
```

This will install [OAuthLib](https://oauthlib.readthedocs.io/en/latest/index.html) to securely construct the authentication request.

```
anaplan = Client(
    auth=AnaplanLocalOAuth(
        client_id=os.environ["OAUTH_CLIENT_ID"],
        client_secret=os.environ["OAUTH_CLIENT_SECRET"],
        redirect_uri="https://vinzenzklass.github.io/anaplan-sdk",
    )
)
```

```
anaplan = AsyncClient(
    auth=AnaplanLocalOAuth(
        client_id=os.environ["OAUTH_CLIENT_ID"],
        client_secret=os.environ["OAUTH_CLIENT_SECRET"],
        redirect_uri="https://vinzenzklass.github.io/anaplan-sdk",
    )
)
```

The SDK will prompt you to open the login URI in your browser. After you have logged in, you will need to copy the entire redirect URI from your browser and paste it into the terminal.

Why do I need to copy the redirect URL?

Unfortunately, registering localhost redirect URIs is not supported by Anaplan. This means we cannot intercept the redirect URI and extract the `authorization_code` automatically. This is a limitation of Anaplan's OAuth2 implementation. See [this Community Note](https://community.anaplan.com/discussion/156599/oauth-rediredt-url-port-for-desktop-apps).

## Persisting OAuth Tokens

The SDK provides the ability to persist OAuth refresh tokens between sessions using the system's secure keyring for local applications. This allows you to avoid having to re-authenticate every time you run your application while using OAuth2.

Requires Extras

If you want to use persisting Tokens, you need to additionally install the `keyring` extra:

```
pip install anaplan-sdk[oauth,keyring]
```

```
uv add anaplan-sdk[oauth,keyring]
```

```
poetry add anaplan-sdk[oauth,keyring]
```

This will install [Keyring](https://github.com/jaraco/keyring) to securely store refresh tokens.

To enable token persistence, set the `persist_token=True` parameter when creating an `AnaplanLocalOAuth` instance:

```
anaplan = Client(
    auth=AnaplanLocalOAuth(
        client_id=os.environ["OAUTH_CLIENT_ID"],
        client_secret=os.environ["OAUTH_CLIENT_SECRET"],
        redirect_uri="https://vinzenzklass.github.io/anaplan-sdk",
        persist_token=True,
    )
)
```

```
anaplan = AsyncClient(
    auth=AnaplanLocalOAuth(
        client_id=os.environ["OAUTH_CLIENT_ID"],
        client_secret=os.environ["OAUTH_CLIENT_SECRET"],
        redirect_uri="https://vinzenzklass.github.io/anaplan-sdk",
        persist_token=True,
    )
)
```

When `persist_token` is set to True, the SDK will:

- Look for a stored refresh token in the system's keyring
- If found, use it to obtain a new access token. If also given, this will overwrite the passed `token` parameter.
- If not found or if the token is invalid, prompt the user for authentication
- After authentication, store the new refresh token in the keyring

Keyring Configuration

The keyring library may require additional configuration depending on your environment:

- In headless environments, you may need to explicitely configure a different keyring backend
- Some Linux distributions may require additional packages or configuration

Configuring the keyring backend is your responsibility as it depends on your specific environment.

For example, to use the libsecret file backend:

```
import keyring
from keyring.backends import libsecret

keyring.set_keyring(libsecret.Keyring())
```

For more information, refer to the [keyring documentation](https://github.com/jaraco/keyring).

## OAuth Token Ownership

Instances of both `AnaplanLocalOAuth` and `AnaplanRefreshTokenAuth` assert ownership of the token you pass to them for their entire lifetime. This means that you should not use the token outside of these classes, as it may lead to errors when attempting to use the same refresh token in multiple places. You can access the current token by using the `token` property, but you should not use anything other than the `access_token`. You can use this property to reassert control of the OAuth token when the instance is nor longer needed. If you do need to use the token in several places simultaneously, you should use a [custom scheme](#custom-authentication-schemes) to do so and handle all potential conflicts appropriately.

## Custom Authentication Schemes

If you need more control over the authentication process, you can provide your own Subclass of `httpx.Auth` to the `auth` parameter of the `Client` or `AsyncClient`. This allows you to implement any custom authentication strategy you need. If you do so, the **entire** Authentication process is your responsibility. You can read more about the `httpx.Auth` interface in the [httpx documentation](https://www.python-httpx.org/advanced/authentication/#custom-authentication-schemes).

Below is an outline of the simplest variant of the `httpx.Auth` interface that will suffice for Anaplan's authentication. Note the non-standard `AnaplanAuthToken` prefix in the `Authorization` header and the `requires_response_body = True` class attribute.

```
import httpx

class MyCustomAuth(httpx.Auth):
    requires_response_body = True

    def __init__(self, token: str):
        self._token: str = token

    def auth_flow(self, request):
        request.headers["Authorization"] = f"AnaplanAuthToken {self._token}"
        response = yield request
        if response.status_code == 401:
            auth_res = yield httpx.Request(...) # Your implementation
            self._token = auth_res.json()["tokenInfo"]["tokenValue"]
            request.headers["Authorization"] = f"AnaplanAuthToken {self._token}"
            yield request
```

If you believe that your custom authentication scheme may be generally useful, please consider contributing it to the SDK or opening an issue to discuss it.
