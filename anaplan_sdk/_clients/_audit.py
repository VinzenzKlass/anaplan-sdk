from itertools import chain
from math import ceil
from typing import Literal

import httpx

from anaplan_sdk._base import _BaseClient
from anaplan_sdk.models import User

Event = Literal["all", "byok", "user_activity"]


class _AuditClient(_BaseClient):
    def __init__(self, client: httpx.Client, retry_count: int, thread_count: int) -> None:
        self._client = client
        self._limit = 10_000
        self._thread_count = thread_count
        self._url = "https://audit.anaplan.com/audit/api/1/events"
        super().__init__(retry_count, client)

    def list_users(self) -> list[User]:
        """
        Lists all the Users in the authenticated users default tenant.
        :return: The List of Users.
        """
        return [
            User.model_validate(e)
            for e in self._get("https://api.anaplan.com/2/0/users").get("users")
        ]

    def get_events(self, days_into_past: int = 30, event_type: Event = "all") -> list:
        """
        Get audit events from Anaplan Audit API.
        :param days_into_past: The nuber of days into the past to get events for. The API provides
                               data for up to 30 days.
        :param event_type: The type of events to get.
        :return: A list of audit events.
        """
        total = self._get_total(days_into_past, event_type)
        if total == 0:
            return []
        if total <= 10_000:
            return self._get_result_page(days_into_past, event_type)

        from concurrent.futures import ThreadPoolExecutor

        with ThreadPoolExecutor(max_workers=self._thread_count) as executor:
            futures = [
                executor.submit(
                    self._get_result_page, days_into_past, event_type, self._limit, n * self._limit
                )
                for n in range(ceil(total / self._limit))
            ]
            results = [future.result() for future in futures]
            return list(chain.from_iterable(results))

    def _get_total(self, days_into_past: int = 60, event_type: Event = "all") -> int:
        return (  # noqa
            self._get(
                self._url,
                params={
                    "limit": 0,
                    "type": event_type,
                    "intervalInHours": days_into_past * 24,
                },
            )
        )["meta"]["paging"]["totalSize"]  # noqa

    def _get_result_page(
        self,
        days_into_past: int = 60,
        event_type: Event = "all",
        limit: int = 10_000,
        offset: int = 0,
    ) -> list:
        return (
            self._get(
                self._url,
                params={
                    "intervalInHours": days_into_past * 24,
                    "limit": limit,
                    "offset": offset,
                    "type": event_type,
                },
            )
        ).get("response", [])
