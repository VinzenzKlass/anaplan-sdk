from concurrent.futures import ThreadPoolExecutor
from itertools import chain
from math import ceil
from typing import Any, Iterator

import httpx

from anaplan_sdk._base import _BaseClient
from anaplan_sdk.models import UserScim


class _ScimClient(_BaseClient):
    def __init__(self, client: httpx.Client, retry_count: int) -> None:
        self._url = "https://api.anaplan.com/scim/1/0/v2/Users"
        super().__init__(retry_count, client)

    def get_user(self, user_id: str) -> UserScim:
        """
        Use this endpoint to retrieve all user information and associated workspaces.
        :return: The requested User and their workspace details.
        """
        return UserScim.model_validate(self._get(f"{self._url}/{user_id}"))

    def list_users(self, filter: str | None = None) -> list[UserScim]:
        """
        Use this endpoint to search for users and associated
        workspaces. Note that the limit is 100 users per call.

        :param filter: Optional filter for users. A filter expression
               to restrict the result set in the form of
               <field> <operator> <value>
               Example: givenName Eq “John”
               Expressions may be separated with and, or or ( )
               Supported filter fields include: id, externalId, userName,
               name.familyName, name.givenName.
               Supproted operators include: Eq, Ne, Pr, Gt, Ge, Lt, Le
        :return: The List of Users and their workspace details.

        """
        params = {"filter": filter} if filter else None
        return [
            UserScim.model_validate(e)
            for e in self._get_paginated(f"{self._url}", "Resources", params=params)
        ]

    def __get_page(self, url: str, limit: int, offset: int, result_key: str, **kwargs) -> list:
        """
        SCIM uses different pagination controls.
        """
        kwargs["params"] = kwargs.get("params") or {} | {"count": limit, "startIndex": offset}
        return self._get(url, **kwargs).get(result_key, [])

    def __get_first_page(self, url: str, limit: int, result_key: str, **kwargs) -> tuple[list, int]:
        kwargs["params"] = kwargs.get("params") or {} | {"count": limit}
        res = self._get(url, **kwargs)
        return res.get(result_key, []), res["totalResults"]

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
