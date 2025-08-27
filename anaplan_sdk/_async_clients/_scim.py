from asyncio import gather
from itertools import chain
from typing import Any

from anaplan_sdk._services import _AsyncHttpService
from anaplan_sdk._utils import construct_payload
from anaplan_sdk.models.scim import (
    Operation,
    ReplaceUserInput,
    Resource,
    Schema,
    ServiceProviderConfig,
    User,
    UserInput,
    field,
)


class _AsyncScimClient:
    def __init__(self, http: _AsyncHttpService) -> None:
        self._http = http
        self._url = "https://api.anaplan.com/scim/1/0/v2"

    async def get_service_provider_config(self) -> ServiceProviderConfig:
        res = await self._http.get(f"{self._url}/ServiceProviderConfig")
        return ServiceProviderConfig.model_validate(res)

    async def get_resource_types(self) -> list[Resource]:
        res = await self._http.get(f"{self._url}/ResourceTypes")
        return [Resource.model_validate(e) for e in res.get("Resources", [])]

    async def get_resource_schemas(self) -> list[Schema]:
        res = await self._http.get(f"{self._url}/Schemas")
        return [Schema.model_validate(e) for e in res.get("Resources", [])]

    async def get_users(self, predicate: str | field = None, page_size: int = 100) -> list[User]:
        params: dict[str, int | str] = {"startIndex": 1, "count": page_size}
        if predicate is not None:
            params["filter"] = str(predicate)
        res = await self._http.get(f"{self._url}/Users", params=params)
        users = [User.model_validate(e) for e in res.get("Resources", [])]
        if (total := res["totalResults"]) <= page_size:
            return users
        pages = await gather(
            *(
                self._http.get(
                    f"{self._url}/Users", params=(params | {"startIndex": i, "count": page_size})
                )
                for i in range(page_size + 1, total + 1, page_size)
            )
        )
        for user in chain(*(p.get("Resources", []) for p in pages)):
            users.append(User.model_validate(user))
        return users

    async def get_user(self, user_id: str) -> User:
        res = await self._http.get(f"{self._url}/Users/{user_id}")
        return User.model_validate(res)

    async def add_user(self, user: UserInput | dict[str, Any]) -> User:
        res = await self._http.post(f"{self._url}/Users", json=construct_payload(UserInput, user))
        return User.model_validate(res)

    async def replace_user(self, user_id: str, user: ReplaceUserInput | dict[str, Any]):
        res = await self._http.put(
            f"{self._url}/Users/{user_id}", json=construct_payload(ReplaceUserInput, user)
        )
        return User.model_validate(res)

    async def update_user(
        self, user_id: str, operations: list[Operation] | list[dict[str, Any]]
    ) -> User:
        res = await self._http.patch(
            f"{self._url}/Users/{user_id}",
            json={
                "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
                "Operations": [construct_payload(Operation, e) for e in operations],
            },
        )
        return User.model_validate(res)
