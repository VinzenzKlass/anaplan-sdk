from asyncio import gather
from itertools import chain
from math import ceil
from typing import Literal

import httpx

from anaplan_sdk._base import _AsyncBaseClient

Event = Literal["all", "byok", "user_activity"]


class _AsyncAuditClient(_AsyncBaseClient):
    def __init__(self, client: httpx.AsyncClient, retry_count: int) -> None:
        self._client = client
        self._limit = 10_000
        self._url = "https://audit.anaplan.com/audit/api/1/events"
        super().__init__(retry_count, client)

    async def _get_total(self, days_into_past: int = 60, event_type: Event = "all") -> int:
        return (  # noqa
            await self._get(
                self._url,
                params={
                    "limit": 0,
                    "type": event_type,
                    "intervalInHours": days_into_past * 24,
                },
            )
        )["meta"]["paging"]["totalSize"]  # noqa

    async def _get_result_page(
        self,
        days_into_past: int = 60,
        event_type: Event = "all",
        limit: int = 10_000,
        offset: int = 0,
    ) -> list:
        return (
            await self._get(
                self._url,
                params={
                    "intervalInHours": days_into_past * 24,
                    "limit": limit,
                    "offset": offset,
                    "type": event_type,
                },
            )
        ).get("response", [])

    async def get_events(self, days_into_past: int = 30, event_type: Event = "all") -> list:
        """
        Get audit events from Anaplan Audit API.
        :param days_into_past: The nuber of days into the past to get events for. The API provides
        data for up to 30 days.
        :param event_type: The type of events to get.
        :return: A list of audit events.
        """
        total = await self._get_total(days_into_past, event_type)
        if total == 0:
            return []
        if total <= 10_000:
            return await self._get_result_page(days_into_past, event_type)

        return list(
            chain.from_iterable(
                await gather(
                    *(
                        self._get_result_page(
                            days_into_past, event_type, self._limit, n * self._limit
                        )
                        for n in range(ceil(total / self._limit))
                    )
                )
            )
        )
