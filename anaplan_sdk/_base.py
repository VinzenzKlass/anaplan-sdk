"""
Provides Base Classes for this project.
"""

import logging
from gzip import compress
from typing import Any, Callable, Coroutine, Literal

import httpx
from httpx import HTTPError, Response

from anaplan_sdk.exceptions import (
    AnaplanException,
    AnaplanTimeoutException,
    InvalidIdentifierException,
)

logger = logging.getLogger("anaplan_sdk")


class _BaseClient:
    def __init__(self, retry_count: int, client: httpx.Client):
        self._retry_count = retry_count
        self._client = client

    def _get(self, url: str) -> dict[str, float | int | str | list | dict | bool]:
        return self._run_with_retry(self._client.get, url).json()

    def _get_binary(self, url: str) -> bytes:
        return self._run_with_retry(self._client.get, url).content

    def _post(
        self, url: str, json: dict | list
    ) -> dict[str, float | int | str | list | dict | bool]:
        return self._run_with_retry(
            self._client.post, url, headers={"Content-Type": "application/json"}, json=json
        ).json()

    def _post_empty(self, url: str) -> None:
        self._run_with_retry(self._client.post, url)

    def _put_binary_gzip(self, url: str, content: bytes) -> Response:
        return self._run_with_retry(
            self._client.put,
            url,
            headers={"Content-Type": "application/x-gzip"},
            content=compress(content),
        )

    def _run_with_retry(self, func: Callable[..., Response], *args, **kwargs) -> Response:
        for i in range(max(self._retry_count, 1)):
            try:
                response = func(*args, **kwargs)
                response.raise_for_status()
                return response
            except HTTPError as error:
                url = args[0] or kwargs.get("url")
                if i >= self._retry_count - 1:
                    raise_error(error)
                logger.info(f"Retrying for: {url}")


class _AsyncBaseClient:
    def __init__(self, retry_count: int, client: httpx.AsyncClient):
        self._retry_count = retry_count
        self._client = client

    async def _get(self, url: str) -> dict[str, float | int | str | list | dict | bool]:
        return (await self._run_with_retry(self._client.get, url)).json()

    async def _get_binary(self, url: str) -> bytes:
        return (await self._run_with_retry(self._client.get, url)).content

    async def _post(
        self, url: str, json: dict | list
    ) -> dict[str, float | int | str | list | dict | bool]:
        return (
            await self._run_with_retry(
                self._client.post, url, headers={"Content-Type": "application/json"}, json=json
            )
        ).json()

    async def _post_empty(self, url: str) -> None:
        await self._run_with_retry(self._client.post, url)

    async def _put_binary_gzip(self, url: str, content: bytes) -> Response:
        return await self._run_with_retry(
            self._client.put,
            url,
            headers={"Content-Type": "application/x-gzip"},
            content=compress(content),
        )

    async def _run_with_retry(
        self, func: Callable[..., Coroutine[Any, Any, Response]], *args, **kwargs
    ) -> Response:
        for i in range(max(self._retry_count, 1)):
            try:
                response = await func(*args, **kwargs)
                response.raise_for_status()
                return response
            except HTTPError as error:
                if i >= self._retry_count - 1:
                    raise_error(error)


def action_url(action_id: int) -> Literal["imports", "exports", "actions", "processes"]:
    """
    Determine the type of action based on its identifier.
    :param action_id: The identifier of the action.
    :return: The type of action.
    """
    if 12000000000 <= action_id < 113000000000:
        return "imports"
    if 116000000000 <= action_id < 117000000000:
        return "exports"
    if 117000000000 <= action_id < 118000000000:
        return "actions"
    if 118000000000 <= action_id < 119000000000:
        return "processes"
    raise InvalidIdentifierException(f"Action '{action_id}' is not a valid identifier.")


def raise_error(error: HTTPError) -> None:
    """
    Raise an appropriate exception based on the error.
    :param error: The error to raise an exception for.
    """
    if isinstance(error, httpx.TimeoutException):
        raise AnaplanTimeoutException from error
    if isinstance(error, httpx.HTTPStatusError):
        if error.response.status_code == 404:
            raise InvalidIdentifierException from error
    raise AnaplanException from error
