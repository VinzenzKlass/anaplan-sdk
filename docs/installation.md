---
title: Installation
description: How to install Anaplan SDK.
---

Anaplan SDK requires Python 3.10.4 or higher.

=== "pip"
    ```shell
    pip install anaplan-sdk
    ```
===+ "uv"
    ```shell
    uv add anaplan-sdk
    ```
=== "Poetry"
    ```shell
    poetry add anaplan-sdk
    ```


### Dependencies 

By default, Anaplan SDK has just two dependencies:

- [httpx](https://www.python-httpx.org/): HTTP Client.
- [pydantic](https://pypi.org/project/pydantic/): Data Models and validation.


### Certificate Authentication

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



### Oauth2 Authentication

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
