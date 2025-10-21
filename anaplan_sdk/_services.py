import asyncio
import logging
import time
from asyncio import gather, sleep
from concurrent.futures import ThreadPoolExecutor
from gzip import compress
from itertools import chain
from math import ceil
from typing import Any, Awaitable, Callable, Coroutine, Iterator, TypeVar

import httpx
from httpx import HTTPError, Response

from .exceptions import AnaplanException, AnaplanTimeoutException, InvalidIdentifierException
from .models import TaskSummary

SORT_WARNING = (
    "If you are sorting by a field that is potentially ambiguous (e.g., name), the order of "
    "results is not guaranteed to be internally consistent across multiple requests. This will "
    "lead to wrong results when paginating through result sets where the ambiguous order can cause "
    "records to slip between pages or be duplicated on multiple pages. The only way to ensure "
    "correct results when sorting is to make sure the entire result set fits in one page, or to "
    "sort by a field that is guaranteed to be unique (e.g., id)."
)

logger = logging.getLogger("anaplan_sdk")

_json_header = {"Content-Type": "application/json"}
_gzip_header = {"Content-Type": "application/x-gzip"}

Task = TypeVar("Task", bound=TaskSummary)


class _HttpService:
    def __init__(
        self,
        client: httpx.Client,
        *,
        retry_count: int,
        backoff: float,
        backoff_factor: float,
        page_size: int,
        poll_delay: int,
    ):
        logger.debug(
            f"Initializing HttpService with retry_count={retry_count}, "
            f"page_size={page_size}, poll_delay={poll_delay}."
        )
        self._client = client
        self._retry_count = retry_count
        self._backoff = backoff
        self._backoff_factor = backoff_factor
        self._poll_delay = poll_delay
        self._page_size = min(page_size, 5_000)

    def get(self, url: str, **kwargs) -> dict[str, Any]:
        return self.__run_with_retry(self._client.get, url, **kwargs).json()

    def get_binary(self, url: str) -> bytes:
        return self.__run_with_retry(self._client.get, url).content

    def post(self, url: str, json: dict | list) -> dict[str, Any]:
        return self.__run_with_retry(self._client.post, url, headers=_json_header, json=json).json()

    def put(self, url: str, json: dict | list) -> dict[str, Any]:
        res = self.__run_with_retry(self._client.put, url, headers=_json_header, json=json)
        return res.json() if res.num_bytes_downloaded > 0 else {}

    def patch(self, url: str, json: dict | list) -> dict[str, Any]:
        return (
            self.__run_with_retry(self._client.patch, url, headers=_json_header, json=json)
        ).json()

    def delete(self, url: str) -> dict[str, Any]:
        return (self.__run_with_retry(self._client.delete, url, headers=_json_header)).json()

    def post_empty(self, url: str, **kwargs) -> dict[str, Any]:
        res = self.__run_with_retry(self._client.post, url, **kwargs)
        return res.json() if res.num_bytes_downloaded > 0 else {}

    def put_binary_gzip(self, url: str, content: str | bytes) -> Response:
        content = compress(content.encode() if isinstance(content, str) else content)
        return self.__run_with_retry(self._client.put, url, headers=_gzip_header, content=content)

    def poll_task(self, func: Callable[..., Task], *args) -> Task:
        while (result := func(*args)).task_state != "COMPLETE":
            time.sleep(self._poll_delay)
        return result

    def get_paginated(self, url: str, result_key: str, **kwargs) -> Iterator[dict[str, Any]]:
        logger.debug(f"Starting paginated fetch from {url} with page_size={self._page_size}.")
        first_page, total_items, actual_size = self._get_first_page(url, result_key, **kwargs)
        if total_items <= self._page_size:
            logger.debug("All items fit in first page, no additional requests needed.")
            return iter(first_page)
        if kwargs and (kwargs.get("params") or {}).get("sort", None):
            logger.warning(SORT_WARNING)
        pages_needed = ceil(total_items / actual_size)
        logger.debug(f"Fetching {pages_needed - 1} additional pages with {actual_size} items each.")
        with ThreadPoolExecutor() as executor:
            pages = executor.map(
                lambda n: self._get_page(url, actual_size, n * actual_size, result_key, **kwargs),
                range(1, pages_needed),
            )
        logger.debug(f"Completed paginated fetch of {total_items} total items.")
        return chain(first_page, *pages)

    def _get_page(self, url: str, limit: int, offset: int, result_key: str, **kwargs) -> list:
        logger.debug(f"Fetching page: offset={offset}, limit={limit} from {url}.")
        kwargs["params"] = (kwargs.get("params") or {}) | {"limit": limit, "offset": offset}
        return self.get(url, **kwargs).get(result_key, [])

    def _get_first_page(self, url: str, result_key: str, **kwargs) -> tuple[list, int, int]:
        logger.debug(f"Fetching first page with limit={self._page_size} from {url}.")
        kwargs["params"] = (kwargs.get("params") or {}) | {"limit": self._page_size}
        res = self.get(url, **kwargs)
        return _extract_first_page(res, result_key, self._page_size)

    def __run_with_retry(self, func: Callable[..., Response], *args, **kwargs) -> Response:
        for i in range(max(self._retry_count, 1)):
            try:
                response = func(*args, **kwargs)
                if response.status_code == 429:
                    if i >= self._retry_count - 1:
                        raise AnaplanException("Rate limit exceeded.")
                    backoff_time = self._backoff * (self._backoff_factor if i > 0 else 1)
                    logger.warning(f"Rate limited. Retrying in {backoff_time} seconds.")
                    time.sleep(backoff_time)
                    continue
                response.raise_for_status()
                return response
            except HTTPError as error:
                if i >= self._retry_count - 1:
                    _raise_error(error)
                url = args[0] or kwargs.get("url")
                logger.info(f"Retrying for: {url}")

        raise AnaplanException("Exhausted all retries without a successful response or Error.")


class _AsyncHttpService:
    def __init__(
        self,
        client: httpx.AsyncClient,
        *,
        retry_count: int,
        backoff: float,
        backoff_factor: float,
        page_size: int,
        poll_delay: int,
    ):
        logger.debug(
            f"Initializing AsyncHttpService with retry_count={retry_count}, "
            f"page_size={page_size}, poll_delay={poll_delay}."
        )
        self._client = client
        self._retry_count = retry_count
        self._backoff = backoff
        self._backoff_factor = backoff_factor
        self._poll_delay = poll_delay
        self._page_size = min(page_size, 5_000)

    async def get(self, url: str, **kwargs) -> dict[str, Any]:
        return (await self._run_with_retry(self._client.get, url, **kwargs)).json()

    async def get_binary(self, url: str) -> bytes:
        return (await self._run_with_retry(self._client.get, url)).content

    async def post(self, url: str, json: dict | list) -> dict[str, Any]:
        return (
            await self._run_with_retry(self._client.post, url, headers=_json_header, json=json)
        ).json()

    async def put(self, url: str, json: dict | list) -> dict[str, Any]:
        res = await self._run_with_retry(self._client.put, url, headers=_json_header, json=json)
        return res.json() if res.num_bytes_downloaded > 0 else {}

    async def patch(self, url: str, json: dict | list) -> dict[str, Any]:
        return (
            await self._run_with_retry(self._client.patch, url, headers=_json_header, json=json)
        ).json()

    async def delete(self, url: str) -> dict[str, Any]:
        return (await self._run_with_retry(self._client.delete, url, headers=_json_header)).json()

    async def post_empty(self, url: str, **kwargs) -> dict[str, Any]:
        res = await self._run_with_retry(self._client.post, url, **kwargs)
        return res.json() if res.num_bytes_downloaded > 0 else {}

    async def put_binary_gzip(self, url: str, content: str | bytes) -> Response:
        content = compress(content.encode() if isinstance(content, str) else content)
        return await self._run_with_retry(
            self._client.put, url, headers=_gzip_header, content=content
        )

    async def poll_task(self, func: Callable[..., Awaitable[Task]], *args) -> Task:
        while (result := await func(*args)).task_state != "COMPLETE":
            await sleep(self._poll_delay)
        return result

    async def get_paginated(self, url: str, result_key: str, **kwargs) -> Iterator[dict[str, Any]]:
        logger.debug(f"Starting paginated fetch from {url} with page_size={self._page_size}.")
        first_page, total_items, actual_size = await self._get_first_page(url, result_key, **kwargs)
        if total_items <= self._page_size:
            logger.debug("All items fit in first page, no additional requests needed.")
            return iter(first_page)
        if kwargs and (kwargs.get("params") or {}).get("sort", None):
            logger.warning(SORT_WARNING)
        pages = await gather(
            *(
                self._get_page(url, actual_size, n * actual_size, result_key, **kwargs)
                for n in range(1, ceil(total_items / actual_size))
            )
        )
        logger.debug(f"Completed paginated fetch of {total_items} total items.")
        return chain(first_page, *pages)

    async def _get_page(self, url: str, limit: int, offset: int, result_key: str, **kwargs) -> list:
        logger.debug(f"Fetching page: offset={offset}, limit={limit} from {url}.")
        kwargs["params"] = (kwargs.get("params") or {}) | {"limit": limit, "offset": offset}
        return (await self.get(url, **kwargs)).get(result_key, [])

    async def _get_first_page(self, url: str, result_key: str, **kwargs) -> tuple[list, int, int]:
        logger.debug(f"Fetching first page with limit={self._page_size} from {url}.")
        kwargs["params"] = (kwargs.get("params") or {}) | {"limit": self._page_size}
        res = await self.get(url, **kwargs)
        return _extract_first_page(res, result_key, self._page_size)

    async def _run_with_retry(
        self, func: Callable[..., Coroutine[Any, Any, Response]], *args, **kwargs
    ) -> Response:
        for i in range(max(self._retry_count, 1)):
            try:
                response = await func(*args, **kwargs)
                if response.status_code == 429:
                    if i >= self._retry_count - 1:
                        raise AnaplanException("Rate limit exceeded.")
                    backoff_time = self._backoff * (self._backoff_factor if i > 0 else 1)
                    logger.warning(f"Rate limited. Retrying in {backoff_time} seconds.")
                    await asyncio.sleep(backoff_time)
                    continue
                response.raise_for_status()
                return response
            except HTTPError as error:
                if i >= self._retry_count - 1:
                    _raise_error(error)
                url = args[0] or kwargs.get("url")
                logger.info(f"Retrying for: {url}")

        raise AnaplanException("Exhausted all retries without a successful response or Error.")


def _extract_first_page(
    res: dict[str, Any], result_key: str, page_size: int
) -> tuple[list[dict[str, Any]], int, int]:
    total_items, first_page = res["meta"]["paging"]["totalSize"], res.get(result_key, [])
    actual_page_size = res["meta"]["paging"]["currentPageSize"]
    if actual_page_size < page_size and not actual_page_size == total_items:
        logger.warning(
            f"Page size {page_size} was silently truncated to {actual_page_size}. "
            f"Using the server-side enforced page size {actual_page_size} for further requests."
        )
    logger.debug(f"Found {total_items} total items, retrieved {len(first_page)} in first page.")
    return first_page, total_items, actual_page_size


def _raise_error(error: HTTPError) -> None:
    if isinstance(error, httpx.TimeoutException):
        raise AnaplanTimeoutException from error
    if isinstance(error, httpx.HTTPStatusError):
        if error.response.status_code == 404:
            raise InvalidIdentifierException from error
        logger.error(f"Anaplan Error: [{error.response.status_code}]: {error.response.text}")
        raise AnaplanException(error.response.text) from error

    logger.error(f"Error: {error}")
    raise AnaplanException from error
