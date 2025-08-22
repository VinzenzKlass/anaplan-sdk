import asyncio
import logging
import random
import time
from asyncio import gather, sleep
from concurrent.futures import ThreadPoolExecutor
from gzip import compress
from itertools import chain
from math import ceil
from typing import Any, Awaitable, Callable, Coroutine, Iterator, Literal, Type, TypeVar

import httpx
from httpx import HTTPError, Response
from pydantic.alias_generators import to_camel

from .exceptions import AnaplanException, AnaplanTimeoutException, InvalidIdentifierException
from .models import (
    AnaplanModel,
    InsertionResult,
    ModelCalendar,
    MonthsQuartersYearsCalendar,
    TaskSummary,
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
Task = TypeVar("Task", bound=TaskSummary)


class _HttpService:
    def __init__(self, client: httpx.Client, retry_count: int, page_size: int, poll_delay: int):
        logger.debug(
            f"Initializing HttpService with retry_count={retry_count}, "
            f"page_size={page_size}, poll_delay={poll_delay}."
        )
        self._client = client
        self._retry_count = retry_count
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
        total_items, first_page = res["meta"]["paging"]["totalSize"], res.get(result_key, [])
        actual_page_size = res["meta"]["paging"]["currentPageSize"]
        if actual_page_size < self._page_size and not actual_page_size == total_items:
            logger.warning(
                f"Page size {self._page_size} was silently truncated to {actual_page_size}."
                f"Using the server-side enforced page size {actual_page_size} for further requests."
            )
        logger.debug(f"Found {total_items} total items, retrieved {len(first_page)} in first page.")
        return first_page, total_items, actual_page_size

    def __run_with_retry(self, func: Callable[..., Response], *args, **kwargs) -> Response:
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


class _AsyncHttpService:
    def __init__(
        self, client: httpx.AsyncClient, retry_count: int, page_size: int, poll_delay: int
    ):
        logger.debug(
            f"Initializing AsyncHttpService with retry_count={retry_count}, "
            f"page_size={page_size}, poll_delay={poll_delay}."
        )
        self._client = client
        self._retry_count = retry_count
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
        total_items, first_page = res["meta"]["paging"]["totalSize"], res.get(result_key, [])
        actual_page_size = res["meta"]["paging"]["currentPageSize"]
        if actual_page_size < self._page_size and not actual_page_size == total_items:
            logger.warning(
                f"Page size {self._page_size} was silently truncated to {actual_page_size}."
                f"Using the server-side enforced page size {actual_page_size} for further requests."
            )
        logger.debug(f"Found {total_items} total items, retrieved {len(first_page)} in first page.")
        return first_page, total_items, actual_page_size

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


def sort_params(sort_by: str, descending: bool) -> dict[str, str | bool]:
    """
    Construct search parameters for sorting. This also converts snake_case to camelCase.
    :param sort_by: The field to sort by, optionally in snake_case.
    :param descending: Whether to sort in descending order.
    :return: A dictionary of search parameters in Anaplan's expected format.
    """
    return {"sort": f"{'-' if descending else '+'}{to_camel(sort_by)}"}


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
        logger.warning(msg.format("Users", "get_users"))
    if 101000000000 <= dimension_id < 102000000000:
        logger.warning(msg.format("Lists", "get_list_items"))
    return dimension_id
