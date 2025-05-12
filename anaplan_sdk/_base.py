import asyncio
import logging
import random
import time
from asyncio import gather
from concurrent.futures import ThreadPoolExecutor
from gzip import compress
from itertools import chain
from math import ceil
from typing import Any, Callable, Coroutine, Iterator, Literal, Type, TypeVar

import httpx
from httpx import HTTPError, Response

from .exceptions import (
    AnaplanException,
    AnaplanTimeoutException,
    InvalidIdentifierException,
)
from .models import AnaplanModel
from .models.cloud_works import IntegrationInput, IntegrationProcessInput, ScheduleInput

logger = logging.getLogger("anaplan_sdk")

_json_header = {"Content-Type": "application/json"}
_gzip_header = {"Content-Type": "application/x-gzip"}

T = TypeVar("T", bound=AnaplanModel)


class _BaseClient:
    def __init__(self, retry_count: int, client: httpx.Client):
        self._retry_count = retry_count
        self._client = client

    def _get(self, url: str, **kwargs) -> dict[str, Any]:
        return self._run_with_retry(self._client.get, url, **kwargs).json()

    def _get_binary(self, url: str) -> bytes:
        return self._run_with_retry(self._client.get, url).content

    def _post(self, url: str, json: dict | list) -> dict[str, Any]:
        return self._run_with_retry(self._client.post, url, headers=_json_header, json=json).json()

    def _put(self, url: str, json: dict | list) -> dict[str, Any]:
        return (self._run_with_retry(self._client.put, url, headers=_json_header, json=json)).json()

    def _patch(self, url: str, json: dict | list) -> dict[str, Any]:
        return (self._run_with_retry(self._client.put, url, headers=_json_header, json=json)).json()

    def _delete(self, url: str) -> dict[str, Any]:
        return (self._run_with_retry(self._client.delete, url, headers=_json_header)).json()

    def _post_empty(self, url: str) -> dict[str, Any]:
        res = self._run_with_retry(self._client.post, url)
        return res.json() if res.num_bytes_downloaded > 0 else {}

    def _put_binary_gzip(self, url: str, content: bytes) -> Response:
        return self._run_with_retry(
            self._client.put, url, headers=_gzip_header, content=compress(content)
        )

    def __get_page(self, url: str, limit: int, offset: int, result_key: str, **kwargs) -> list:
        kwargs["params"] = kwargs.get("params") or {} | {"limit": limit, "offset": offset}
        return self._get(url, **kwargs).get(result_key, [])

    def __get_first_page(self, url: str, limit: int, result_key: str, **kwargs) -> tuple[list, int]:
        kwargs["params"] = kwargs.get("params") or {} | {"limit": limit}
        res = self._get(url, **kwargs)
        return res.get(result_key, []), res["meta"]["paging"]["totalSize"]

    def _get_paginated(
        self, url: str, result_key: str, page_size: int = 5_000, **kwargs
    ) -> Iterator[dict[str, Any]]:
        first_page, total_items = self.__get_first_page(url, page_size, result_key, **kwargs)
        if total_items <= page_size:
            return iter(first_page)

        with ThreadPoolExecutor() as executor:
            pages = executor.map(
                lambda n: self.__get_page(url, page_size, n * page_size, result_key, **kwargs),
                range(1, ceil(total_items / page_size)),
            )

        return chain(first_page, *pages)

    def _run_with_retry(self, func: Callable[..., Response], *args, **kwargs) -> Response:
        for i in range(max(self._retry_count, 1)):
            try:
                response = func(*args, **kwargs)
                if response.status_code == 429:
                    if i >= self._retry_count - 1:
                        raise AnaplanException("Rate limit exceeded.")
                    backoff_time = max(i, 1) * random.randint(2, 5)
                    logger.info(f"Rate limited. Retrying in {backoff_time} seconds.")
                    time.sleep(backoff_time)
                    continue
                response.raise_for_status()
                return response
            except HTTPError as error:
                if i >= self._retry_count - 1:
                    raise_error(error)
                url = args[0] or kwargs.get("url")
                logger.info(f"Retrying for: {url}")

        raise AnaplanException("Exhausted all retries without a successful response or Error.")


class _AsyncBaseClient:
    def __init__(self, retry_count: int, client: httpx.AsyncClient):
        self._retry_count = retry_count
        self._client = client

    async def _get(self, url: str, **kwargs) -> dict[str, Any]:
        return (await self._run_with_retry(self._client.get, url, **kwargs)).json()

    async def _get_binary(self, url: str) -> bytes:
        return (await self._run_with_retry(self._client.get, url)).content

    async def _post(self, url: str, json: dict | list) -> dict[str, Any]:
        return (
            await self._run_with_retry(self._client.post, url, headers=_json_header, json=json)
        ).json()

    async def _put(self, url: str, json: dict | list) -> dict[str, Any]:
        return (
            await self._run_with_retry(self._client.put, url, headers=_json_header, json=json)
        ).json()

    async def _patch(self, url: str, json: dict | list) -> dict[str, Any]:
        return (
            await self._run_with_retry(self._client.patch, url, headers=_json_header, json=json)
        ).json()

    async def _delete(self, url: str) -> dict[str, Any]:
        return (await self._run_with_retry(self._client.delete, url, headers=_json_header)).json()

    async def _post_empty(self, url: str) -> dict[str, Any]:
        res = await self._run_with_retry(self._client.post, url)
        return res.json() if res.num_bytes_downloaded > 0 else {}

    async def _put_binary_gzip(self, url: str, content: bytes) -> Response:
        return await self._run_with_retry(
            self._client.put, url, headers=_gzip_header, content=compress(content)
        )

    async def __get_page(
        self, url: str, limit: int, offset: int, result_key: str, **kwargs
    ) -> list:
        kwargs["params"] = kwargs.get("params") or {} | {"limit": limit, "offset": offset}
        return (await self._get(url, **kwargs)).get(result_key, [])

    async def __get_first_page(
        self, url: str, limit: int, result_key: str, **kwargs
    ) -> tuple[list, int]:
        kwargs["params"] = kwargs.get("params") or {} | {"limit": limit}
        res = await self._get(url, **kwargs)
        return res.get(result_key, []), res["meta"]["paging"]["totalSize"]

    async def _get_paginated(
        self, url: str, result_key: str, page_size: int = 5_000, **kwargs
    ) -> Iterator[dict[str, Any]]:
        first_page, total_items = await self.__get_first_page(url, page_size, result_key, **kwargs)
        if total_items <= page_size:
            return iter(first_page)
        pages = await gather(
            *(
                self.__get_page(url, page_size, n * page_size, result_key, **kwargs)
                for n in range(1, ceil(total_items / page_size))
            )
        )
        return chain(first_page, *pages)

    async def _run_with_retry(
        self, func: Callable[..., Coroutine[Any, Any, Response]], *args, **kwargs
    ) -> Response:
        for i in range(max(self._retry_count, 1)):
            try:
                response = await func(*args, **kwargs)
                if response.status_code == 429:
                    if i >= self._retry_count - 1:
                        raise AnaplanException("Rate limit exceeded.")
                    backoff_time = (i + 1) * random.randint(3, 5)
                    logger.info(f"Rate limited. Retrying in {backoff_time} seconds.")
                    await asyncio.sleep(backoff_time)
                    continue
                response.raise_for_status()
                return response
            except HTTPError as error:
                if i >= self._retry_count - 1:
                    raise_error(error)
                url = args[0] or kwargs.get("url")
                logger.info(f"Retrying for: {url}")

        raise AnaplanException("Exhausted all retries without a successful response or Error.")


def construct_payload(model: Type[T], body: T | dict[str, Any]) -> dict[str, Any]:
    if isinstance(body, dict):
        body = model.model_validate(body)
    return body.model_dump(exclude_none=True, by_alias=True)


def integration_payload(
    body: IntegrationInput | IntegrationProcessInput | dict[str, Any],
) -> dict[str, Any]:
    if isinstance(body, dict):
        body = (
            IntegrationInput.model_validate(body)
            if "jobs" in body
            else IntegrationProcessInput.model_validate(body)
        )
    return body.model_dump(exclude_none=True, by_alias=True)


def schedule_payload(
    integration_id: str, schedule: ScheduleInput | dict[str, Any]
) -> dict[str, Any]:
    if isinstance(schedule, dict):
        schedule = ScheduleInput.model_validate(schedule)
    return {
        "integrationId": integration_id,
        "schedule": schedule.model_dump(exclude_none=True, by_alias=True),
    }


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
        logger.error(f"Anaplan Error: [{error.response.status_code}]: {error.response.text}")
        raise AnaplanException(error.response.text) from error

    logger.error(f"Error: {error}")
    raise AnaplanException from error
