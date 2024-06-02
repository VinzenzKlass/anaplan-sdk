"""
Provides Base Classes for this project.
"""

import logging
from typing import Callable, Coroutine, Any

from httpx import Response, HTTPError

from anaplan_sdk._exceptions import raise_appropriate_error

logger = logging.getLogger("anaplan_sdk")


class _BaseClient:
    def __init__(self, retry_count: int):
        self._retry_count = retry_count

    def _run_with_retry(self, func: Callable[..., Response], *args, **kwargs) -> Response:
        for i in range(max(self._retry_count, 1)):
            try:
                response = func(*args, **kwargs)
                response.raise_for_status()
                return response
            except HTTPError as error:
                url = args[0] or kwargs.get("url")
                if i >= self._retry_count - 1:
                    raise_appropriate_error(error)
                logger.info(f"Retrying for: {url}")


class _AsyncBaseClient:
    def __init__(self, retry_count: int):
        self._retry_count = retry_count

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
                    raise_appropriate_error(error)
