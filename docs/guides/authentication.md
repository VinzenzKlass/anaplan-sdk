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


## OAuth2

Anaplan has introduced Oauth2 support, but it does not support the `client_credentials` grant type. This means you will 
have to at least once manually authenticate in the interactive `authorization_code` flow. The Anaplan SDK does support 
this flow, but it does not automatically manage the `refresh_token`. You can however securely store the `refresh_token` 
in your app and use it to repeatedly and authenticate with Anaplan without any interaction.

??? tip "Requires Extra"
    If you want to use Oauth2 authentication, you need to install the `oauth` extra:
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

### Authorization Code

When using OAuth authentication, the default behavior prompts you to manually open a URL, authorize the application, and paste the redirect URL back into your terminal. However, you can customize this flow by providing the `on_auth_code` callback.

The `on_auth_code` callback lets you hook into the Auth Flow to handle the authorization URL programmatically and return the authorization response. `on_auth_code` must be a callable that takes the authorization URL as a single argument of type `str` and returns the redirect URL as a `str`.

=== "Synchronous"
    ```python
    def on_auth_code(redirect_uri: str) -> str:
        return input(f"Go fetch! {redirect_uri}\nPaste here: ")

    anaplan = anaplan_sdk.Client(
        workspace_id="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
        model_id="11111111111111111111111111111111",
        redirect_uri="https://vinzenzklass.github.io/anaplan-sdk",
        client_id="my_anaplan_oauth_client_id",
        client_secret="my_anaplan_oauth_client_secret",
        on_auth_code=on_auth_code,
    )
    ```
=== "Asynchronous"
    ```python
    async def on_auth_code(redirect_uri: str) -> str: # Can be sync or async
        return input(f"Go fetch! {redirect_uri}\nPaste here: ")

    anaplan = anaplan_sdk.AsyncClient(
        workspace_id="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
        model_id="11111111111111111111111111111111",
        redirect_uri="https://vinzenzklass.github.io/anaplan-sdk",
        client_id="my_anaplan_oauth_client_id",
        client_secret="my_anaplan_oauth_client_secret",
        on_auth_code=on_auth_code,
    )
    ```

### Refresh Tokens

You can extend the above example to also pass a `refresh_token` to authenticate without any user interaction, and 
optionally pass a callable to the `on_token_refresh` parameter. This allows you to hook into the token refresh flow and 
store the current `refresh_token` securely in your app. `on_token_refresh` musst be a callable that takes the token as 
a single argument of type `dict[str, str]` and returns `None`.

???+ note "Example"
    The below uses the [pykeepass](https://github.com/libkeepass/pykeepass) library to locally store the token. This is 
    not a recommendation and a purely illustrative example. How you handle the token is entirely up to you.

=== "Synchronous"
    ```python
    import json
    from pykeepass import PyKeePass

    kp = PyKeePass("db.kdbx", password="keepass")
    group = kp.add_group(kp.root_group, "Anaplan")
    
    def on_token_refresh(token: dict[str, str]) -> None:
        kp.add_entry(
            group, title="Anaplan Token", username=None, password=json.dumps(token)
        )
        kp.save()


    anaplan = anaplan_sdk.Client(
        workspace_id="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
        model_id="11111111111111111111111111111111",
        redirect_uri="https://vinzenzklass.github.io/anaplan-sdk",
        client_id="my_anaplan_oauth_client_id",
        client_secret="my_anaplan_oauth_client_secret",
        refresh_token="my_current_refresh_token",
        on_token_refresh=on_token_refresh,
    )
    ```
=== "Asynchronous"
    ```python
    import json
    from pykeepass import PyKeePass
    
    kp = PyKeePass("db.kdbx", password="keepass")
    group = kp.add_group(kp.root_group, "Anaplan")
    
    def on_token_refresh(token: dict[str, str]) -> None: # Can also be async
        kp.add_entry(
            group, title="Anaplan Token", username=None, password=json.dumps(token)
        )
        kp.save()
    

    anaplan = anaplan_sdk.AsyncClient(
        workspace_id="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
        model_id="11111111111111111111111111111111",
        redirect_uri="https://vinzenzklass.github.io/anaplan-sdk",
        client_id="my_anaplan_oauth_client_id",
        client_secret="my_anaplan_oauth_client_secret",
        refresh_token="my_current_refresh_token",
        on_token_refresh=on_token_refresh,
    )
    ```
