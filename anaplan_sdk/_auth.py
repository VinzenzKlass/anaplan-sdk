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
from httpx import HTTPError

from .exceptions import InvalidPrivateKeyException, InvalidCredentialsException

logger = logging.getLogger("anaplan_sdk")


class AnaplanBasicAuth(httpx.Auth):
    requires_response_body = True

    def __init__(
        self,
        user_email: str,
        password: str,
    ):
        self._user_email = user_email
        self._password = password
        self._token = self._init_token()

    def auth_flow(self, request):
        request.headers["Authorization"] = f"AnaplanAuthToken {self._token}"
        response = yield request
        if response.status_code == 401:
            logger.info("Token expired, refreshing.")
            response = yield self._basic_auth_request()
            if "tokenInfo" not in response.json():
                raise InvalidCredentialsException
            self._token = response.json().get("tokenInfo").get("tokenValue")
            request.headers["Authorization"] = f"AnaplanAuthToken {self._token}"
            yield request

    def _basic_auth_request(self):
        credentials = b64encode(f"{self._user_email}:{self._password}".encode()).decode()
        return httpx.Request(
            method="post",
            url="https://auth.anaplan.com/token/authenticate",
            headers={"Authorization": f"Basic {credentials}"},
        )

    def _init_token(self) -> str:
        try:
            logger.info("Creating Authentication Token.")
            credentials = b64encode(f"{self._user_email}:{self._password}".encode()).decode()
            return (
                httpx.post(
                    url="https://auth.anaplan.com/token/authenticate",
                    headers={"Authorization": f"Basic {credentials}"},
                )
                .json()
                .get("tokenInfo")
                .get("tokenValue")
            )
        except HTTPError as error:
            raise InvalidCredentialsException from error


class AnaplanCertAuth(httpx.Auth):
    requires_response_body = True
    requires_request_body = True

    def __init__(
        self,
        certificate: bytes,
        private_key: RSAPrivateKey,
    ):
        self._certificate = certificate
        self._private_key = private_key
        self._token = self._init_token()

    def auth_flow(self, request):
        request.headers["Authorization"] = f"AnaplanAuthToken {self._token}"
        response = yield request
        if response.status_code == 401:
            logger.info("Token expired or invalid, refreshing.")
            response = yield self._cert_auth_request()
            if "tokenInfo" not in response.json():
                raise InvalidCredentialsException
            self._token = response.json().get("tokenInfo").get("tokenValue")
            request.headers["Authorization"] = f"AnaplanAuthToken {self._token}"
            yield request

    def _cert_auth_request(self):
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

    def _init_token(self) -> str:
        try:
            logger.info("Creating Authentication Token.")
            encoded_cert, encoded_string, encoded_signed_string = self._prep_credentials()
            return (
                httpx.post(
                    url="https://auth.anaplan.com/token/authenticate",
                    headers={
                        "Authorization": f"CACertificate {encoded_cert}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "encodedData": encoded_string,
                        "encodedSignedData": encoded_signed_string,
                    },
                )
                .json()
                .get("tokenInfo")
                .get("tokenValue")
            )
        except HTTPError as error:
            raise InvalidCredentialsException from error

    def _prep_credentials(self) -> tuple[str, str, str]:
        message = os.urandom(150)
        return (
            b64encode(self._certificate).decode(),
            b64encode(message).decode(),
            b64encode(self._private_key.sign(message, PKCS1v15(), hashes.SHA512())).decode(),
        )


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
