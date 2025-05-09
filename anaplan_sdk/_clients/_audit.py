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
            for e in self._get_paginated("https://api.anaplan.com/2/0/users", "users")
        ]

    def get_user(self, user_id: int|str = "me") -> User:
        """
        Retrieves information about the specified user.
        :return: The User.
        """
        return User.model_validate(self._get(f"https://api.anaplan.com/2/0/users/{user_id}").get("user"))

    def get_events(self, days_into_past: int = 30, event_type: Event = "all") -> list:
        """
        Get audit events from Anaplan Audit API.
        :param days_into_past: The nuber of days into the past to get events for. The API provides
               data for up to 30 days.
        :param event_type: The type of events to get.
        :return: A list of audit events.
        """
        return list(
            self._get_paginated(
                self._url,
                "response",
                params={"type": event_type, "intervalInHours": days_into_past * 24},
            )
        )
