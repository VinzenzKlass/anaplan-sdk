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

from .exceptions import AnaplanException, AnaplanTimeoutException, InvalidIdentifierException
from .models import (
    AnaplanModel,
    InsertionResult,
    ModelCalendar,
    MonthsQuartersYearsCalendar,
    WeeksGeneralCalendar,
    WeeksGroupingCalendar,
    WeeksPeriodsCalendar,
)
from .models.cloud_works import (
    AmazonS3ConnectionInput,
    AzureBlobConnectionInput,
    ConnectionBody,
    GoogleBigQueryConnectionInput,
    IntegrationInput,
    IntegrationProcessInput,
    ScheduleInput,
)

logger = logging.getLogger("anaplan_sdk")

_json_header = {"Content-Type": "application/json"}
_gzip_header = {"Content-Type": "application/x-gzip"}

T = TypeVar("T", bound=AnaplanModel)


class _BaseClient:
    def __init__(self, retry_count: int, client: httpx.Client):
        self._retry_count = retry_count
        self._client = client
        logger.debug(f"Initialized BaseClient with retry_count={retry_count}.")

    def _get(self, url: str, **kwargs) -> dict[str, Any]:
        return self._run_with_retry(self._client.get, url, **kwargs).json()

    def _get_binary(self, url: str) -> bytes:
        return self._run_with_retry(self._client.get, url).content

    def _post(self, url: str, json: dict | list) -> dict[str, Any]:
        return self._run_with_retry(self._client.post, url, headers=_json_header, json=json).json()

    def _put(self, url: str, json: dict | list) -> dict[str, Any]:
        res = self._run_with_retry(self._client.put, url, headers=_json_header, json=json)
        return res.json() if res.num_bytes_downloaded > 0 else {}

    def _patch(self, url: str, json: dict | list) -> dict[str, Any]:
        return (
            self._run_with_retry(self._client.patch, url, headers=_json_header, json=json)
        ).json()

    def _delete(self, url: str) -> dict[str, Any]:
        return (self._run_with_retry(self._client.delete, url, headers=_json_header)).json()

    def _post_empty(self, url: str, **kwargs) -> dict[str, Any]:
        res = self._run_with_retry(self._client.post, url, **kwargs)
        return res.json() if res.num_bytes_downloaded > 0 else {}

    def _put_binary_gzip(self, url: str, content: bytes) -> Response:
        return self._run_with_retry(
            self._client.put, url, headers=_gzip_header, content=compress(content)
        )

    def __get_page(self, url: str, limit: int, offset: int, result_key: str, **kwargs) -> list:
        logger.debug(f"Fetching page: offset={offset}, limit={limit} from {url}.")
        kwargs["params"] = kwargs.get("params") or {} | {"limit": limit, "offset": offset}
        return self._get(url, **kwargs).get(result_key, [])

    def __get_first_page(self, url: str, limit: int, result_key: str, **kwargs) -> tuple[list, int]:
        logger.debug(f"Fetching first page with limit={limit} from {url}.")
        kwargs["params"] = kwargs.get("params") or {} | {"limit": limit}
        res = self._get(url, **kwargs)
        total_items, first_page = res["meta"]["paging"]["totalSize"], res.get(result_key, [])
        logger.debug(f"Found {total_items} total items, retrieved {len(first_page)} in first page.")
        return first_page, total_items

    def _get_paginated(
        self, url: str, result_key: str, page_size: int = 5_000, **kwargs
    ) -> Iterator[dict[str, Any]]:
        logger.debug(f"Starting paginated fetch from {url} with page_size={page_size}.")
        first_page, total_items = self.__get_first_page(url, page_size, result_key, **kwargs)
        if total_items <= page_size:
            logger.debug("All items fit in first page, no additional requests needed.")
            return iter(first_page)

        pages_needed = ceil(total_items / page_size)
        logger.debug(f"Fetching {pages_needed - 1} additional pages with {page_size} items each.")
        with ThreadPoolExecutor() as executor:
            pages = executor.map(
                lambda n: self.__get_page(url, page_size, n * page_size, result_key, **kwargs),
                range(1, pages_needed),
            )
        logger.debug(f"Completed paginated fetch of {total_items} total items.")
        return chain(first_page, *pages)

    def _run_with_retry(self, func: Callable[..., Response], *args, **kwargs) -> Response:
        for i in range(max(self._retry_count, 1)):
            try:
                response = func(*args, **kwargs)
                if response.status_code == 429:
                    if i >= self._retry_count - 1:
                        raise AnaplanException("Rate limit exceeded.")
                    backoff_time = max(i, 1) * random.randint(2, 5)
                    logger.warning(f"Rate limited. Retrying in {backoff_time} seconds.")
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
        logger.debug(f"Initialized AsyncBaseClient with retry_count={retry_count}.")

    async def _get(self, url: str, **kwargs) -> dict[str, Any]:
        return (await self._run_with_retry(self._client.get, url, **kwargs)).json()

    async def _get_binary(self, url: str) -> bytes:
        return (await self._run_with_retry(self._client.get, url)).content

    async def _post(self, url: str, json: dict | list) -> dict[str, Any]:
        return (
            await self._run_with_retry(self._client.post, url, headers=_json_header, json=json)
        ).json()

    async def _put(self, url: str, json: dict | list) -> dict[str, Any]:
        res = await self._run_with_retry(self._client.put, url, headers=_json_header, json=json)
        return res.json() if res.num_bytes_downloaded > 0 else {}

    async def _patch(self, url: str, json: dict | list) -> dict[str, Any]:
        return (
            await self._run_with_retry(self._client.patch, url, headers=_json_header, json=json)
        ).json()

    async def _delete(self, url: str) -> dict[str, Any]:
        return (await self._run_with_retry(self._client.delete, url, headers=_json_header)).json()

    async def _post_empty(self, url: str, **kwargs) -> dict[str, Any]:
        res = await self._run_with_retry(self._client.post, url, **kwargs)
        return res.json() if res.num_bytes_downloaded > 0 else {}

    async def _put_binary_gzip(self, url: str, content: bytes) -> Response:
        return await self._run_with_retry(
            self._client.put, url, headers=_gzip_header, content=compress(content)
        )

    async def __get_page(
        self, url: str, limit: int, offset: int, result_key: str, **kwargs
    ) -> list:
        logger.debug(f"Fetching page: offset={offset}, limit={limit} from {url}.")
        kwargs["params"] = kwargs.get("params") or {} | {"limit": limit, "offset": offset}
        return (await self._get(url, **kwargs)).get(result_key, [])

    async def __get_first_page(
        self, url: str, limit: int, result_key: str, **kwargs
    ) -> tuple[list, int]:
        logger.debug(f"Fetching first page with limit={limit} from {url}.")
        kwargs["params"] = kwargs.get("params") or {} | {"limit": limit}
        res = await self._get(url, **kwargs)
        total_items, first_page = res["meta"]["paging"]["totalSize"], res.get(result_key, [])
        logger.debug(f"Found {total_items} total items, retrieved {len(first_page)} in first page.")
        return first_page, total_items

    async def _get_paginated(
        self, url: str, result_key: str, page_size: int = 5_000, **kwargs
    ) -> Iterator[dict[str, Any]]:
        logger.debug(f"Starting paginated fetch from {url} with page_size={page_size}.")
        first_page, total_items = await self.__get_first_page(url, page_size, result_key, **kwargs)
        if total_items <= page_size:
            logger.debug("All items fit in first page, no additional requests needed.")
            return iter(first_page)
        pages = await gather(
            *(
                self.__get_page(url, page_size, n * page_size, result_key, **kwargs)
                for n in range(1, ceil(total_items / page_size))
            )
        )
        logger.info(f"Completed paginated fetch of {total_items} total items.")
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
                    logger.warning(f"Rate limited. Retrying in {backoff_time} seconds.")
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
    """
    Construct a payload for the given model and body.
    :param model: The model class to use for validation.
    :param body: The body to validate and optionally convert to a dictionary.
    :return: A dictionary representation of the validated body.
    """
    if isinstance(body, dict):
        body = model.model_validate(body)
    return body.model_dump(exclude_none=True, by_alias=True)


def connection_body_payload(body: ConnectionBody | dict[str, Any]) -> dict[str, Any]:
    """
    Construct a payload for the given integration body.
    :param body: The body to validate and optionally convert to a dictionary.
    :return: A dictionary representation of the validated body.
    """
    if isinstance(body, dict):
        if "sasToken" in body:
            body = AzureBlobConnectionInput.model_validate(body)
        elif "secretAccessKey" in body:
            body = AmazonS3ConnectionInput.model_validate(body)
        else:
            body = GoogleBigQueryConnectionInput.model_validate(body)
    return body.model_dump(exclude_none=True, by_alias=True)


def integration_payload(
    body: IntegrationInput | IntegrationProcessInput | dict[str, Any],
) -> dict[str, Any]:
    """
    Construct a payload for the given integration body.
    :param body: The body to validate and optionally convert to a dictionary.
    :return: A dictionary representation of the validated body.
    """
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
    """
    Construct a payload for the given integration ID and schedule.
    :param integration_id: The ID of the integration.
    :param schedule: The schedule to validate and optionally convert to a dictionary.
    :return: A dictionary representation of the validated schedule.
    """
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


def parse_calendar_response(data: dict) -> ModelCalendar:
    """
    Parse calendar response and return appropriate calendar model.
    :param data: The calendar data from the API response.
    :return: The calendar settings of the model based on calendar type.
    """
    calendar_data = data["modelCalendar"]
    cal_type = calendar_data["calendarType"]
    if cal_type == "Calendar Months/Quarters/Years":
        return MonthsQuartersYearsCalendar.model_validate(calendar_data)
    if cal_type == "Weeks: 4-4-5, 4-5-4 or 5-4-4":
        return WeeksGroupingCalendar.model_validate(calendar_data)
    if cal_type == "Weeks: General":
        return WeeksGeneralCalendar.model_validate(calendar_data)
    if cal_type == "Weeks: 13 4-week Periods":
        return WeeksPeriodsCalendar.model_validate(calendar_data)
    raise AnaplanException(
        "Unknown calendar type encountered. Please report this issue: "
        "https://github.com/VinzenzKlass/anaplan-sdk/issues/new"
    )


def parse_insertion_response(data: list[dict]) -> InsertionResult:
    failures, added, ignored, total = [], 0, 0, 0
    for res in data:
        failures.append(res.get("failures", []))
        added += res.get("added", 0)
        total += res.get("total", 0)
        ignored += res.get("ignored", 0)
    return InsertionResult(
        added=added, ignored=ignored, total=total, failures=list(chain.from_iterable(failures))
    )


def validate_dimension_id(dimension_id: int) -> int:
    if not (
        dimension_id == 101999999999
        or 101_000_000_000 <= dimension_id < 102_000_000_000
        or 109_000_000_000 <= dimension_id < 110_000_000_000
        or 114_000_000_000 <= dimension_id < 115_000_000_000
    ):
        raise InvalidIdentifierException(
            "Invalid dimension_id. Must be a List (101xxxxxxxxx), List Subset (109xxxxxxxxx), "
            "Line Item Subset (114xxxxxxxxx), or Users (101999999999)."
        )
    msg = (
        "Using `get_dimension_items` for {} is discouraged. "
        "Prefer `{}` for better performance and more details on the members."
    )
    if dimension_id == 101999999999:
        logger.warning(msg.format("Users", "list_users"))
    if 101000000000 <= dimension_id < 102000000000:
        logger.warning(msg.format("Lists", "get_list_items"))
    return dimension_id
