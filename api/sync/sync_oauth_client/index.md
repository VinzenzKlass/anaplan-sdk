# Oauth

Synchronous Variant of the Anaplan OAuth client for interactive OAuth Flows in Web Applications.

## __init__

```
__init__(
    client_id: str,
    client_secret: str,
    redirect_uri: str,
    authorization_url: str = "https://us1a.app.anaplan.com/auth/prelogin",
    token_url: str = "https://us1a.app.anaplan.com/oauth/token",
    validation_url: str = "https://auth.anaplan.com/token/validate",
    scope: str = "openid profile email offline_access",
    state_generator: Callable[[], str] | None = None,
)
```

Initializes the OAuth Client. This class provides the two utilities needed to implement the OAuth 2.0 authorization code flow for user-facing Web Applications. It differs from the other Authentication Strategies in this SDK in two main ways:

1. You must implement the actual authentication flow in your application. You cannot pass the credentials directly to the `Client` or `AsyncClient`, and this class does not implement the SDK internal authentication flow, i.e. it does not subclass `httpx.Auth`.
1. You then simply pass the resulting token to the `Client` or `AsyncClient`, rather than passing the credentials directly, which will internally construct an `httpx.Auth` instance

Note that this class exist for convenience only, and you can implement the OAuth 2.0 Flow yourself in your preferred library, or bring an existing implementation. For details on the Anaplan OAuth 2.0 Flow, see the [the Docs](https://anaplanoauth2service.docs.apiary.io/#reference/overview-of-the-authorization-code-grant).

Parameters:

| Name                | Type                  | Description                                                                                                                                                   | Default                                                                                                                                                                                      |
| ------------------- | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `client_id`         | `str`                 | The client ID of your Anaplan Oauth 2.0 application. This Application must be an Authorization Code Grant application.                                        | *required*                                                                                                                                                                                   |
| `client_secret`     | `str`                 | The client secret of your Anaplan Oauth 2.0 application.                                                                                                      | *required*                                                                                                                                                                                   |
| `redirect_uri`      | `str`                 | The URL to which the user will be redirected after authorizing the application.                                                                               | *required*                                                                                                                                                                                   |
| `authorization_url` | `str`                 | The URL to which the user will be redirected to authorize the application. Defaults to the Anaplan Prelogin Page, where the user can select the login method. | `'https://us1a.app.anaplan.com/auth/prelogin'`                                                                                                                                               |
| `token_url`         | `str`                 | The URL to post the authorization code to in order to fetch the access token.                                                                                 | `'https://us1a.app.anaplan.com/oauth/token'`                                                                                                                                                 |
| `validation_url`    | `str`                 | The URL to validate the access token.                                                                                                                         | `'https://auth.anaplan.com/token/validate'`                                                                                                                                                  |
| `scope`             | `str`                 | The scope of the access request.                                                                                                                              | `'openid profile email offline_access'`                                                                                                                                                      |
| `state_generator`   | \`Callable\[[], str\] | None\`                                                                                                                                                        | A callable that generates a random state string. You can optionally pass this if you need to customize the state generation logic. If not provided, the state will be generated by oauthlib. |

## authorization_url

```
authorization_url(
    authorization_url: str | None = None, state: str | None = None
) -> tuple[str, str]
```

Generates the authorization URL for the OAuth 2.0 flow.

Parameters:

| Name                | Type  | Description | Default                                                                                                                                                                                                                                  |
| ------------------- | ----- | ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `authorization_url` | \`str | None\`      | You can optionally pass a custom authorization URL. This is useful if you want to redirect i.e. redirect the user directly to the Anaplan login page rather than the Prelogin page in only one scenario, while still reusing the Client. |
| `state`             | \`str | None\`      | You can optionally pass a custom state string. If not provided, a random state string will be generated by the oauthlib library, or by the state_generator callable if provided.                                                         |

Returns:

| Type              | Description                                                    |
| ----------------- | -------------------------------------------------------------- |
| `tuple[str, str]` | A tuple containing the authorization URL and the state string. |

## fetch_token

```
fetch_token(authorization_response: str) -> dict[str, str | int]
```

Fetches the token using the authorization response from the OAuth 2.0 flow.

Parameters:

| Name                     | Type  | Description                                                                                                                             | Default    |
| ------------------------ | ----- | --------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| `authorization_response` | `str` | The full URL that the user was redirected to after authorizing the application. This URL will contain the authorization code and state. | *required* |

Returns:

| Type             | Description |
| ---------------- | ----------- |
| \`dict\[str, str | int\]\`     |
