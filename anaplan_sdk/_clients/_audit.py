from typing import Any, Literal

from anaplan_sdk._services import _HttpService, sort_params
from anaplan_sdk.models import User

Event = Literal["all", "byok", "user_activity"]
UserSortBy = Literal["first_name", "last_name", "email", "active", "last_login_date"]


class _AuditClient:
    def __init__(self, http: _HttpService) -> None:
        self._http = http
        self._limit = 10_000
        self._url = "https://audit.anaplan.com/audit/api/1/events"

    def get_users(
        self,
        search_pattern: str | None = None,
        sort_by: UserSortBy = "last_login_date",
        descending: bool = True,
    ) -> list[User]:
        """
        Lists all the Users in the authenticated users default tenant.
        :param search_pattern: Optionally filter for specific users. When provided,
               case-insensitive matches users with emails or names containing this string.
               You can use the wildcards `%` for 0-n characters, and `_` for exactly 1 character.
               When None (default), returns all users.
        :param sort_by: The field to sort the results by.
        :param descending: If True, the results will be sorted in descending order.
        :return: The List of Users.
        """
        params = sort_params(sort_by, descending)
        if search_pattern:
            params["s"] = search_pattern
        res = self._http.get_paginated("https://api.anaplan.com/2/0/users", "users", params=params)
        return [User.model_validate(e) for e in res]

    def get_user(self, user_id: str = "me") -> User:
        """
        Retrieves information about the specified user, or the authenticated user if none specified.
        :return: The requested or currently authenticated User.
        """
        return User.model_validate(
            self._http.get(f"https://api.anaplan.com/2/0/users/{user_id}").get("user")
        )

    def get_events(
        self, days_into_past: int = 30, event_type: Event = "all"
    ) -> list[dict[str, Any]]:
        """
        Get audit events from Anaplan Audit API.
        :param days_into_past: The nuber of days into the past to get events for. The API provides
               data for up to 30 days.
        :param event_type: The type of events to get.
        :return: A list of log entries, each containing a dictionary with event details.
        """
        return list(
            self._http.get_paginated(
                self._url,
                "response",
                params={"type": event_type, "intervalInHours": days_into_past * 24},
            )
        )
