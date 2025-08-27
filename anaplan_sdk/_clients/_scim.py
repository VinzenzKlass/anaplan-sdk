from concurrent.futures import ThreadPoolExecutor
from itertools import chain
from typing import Any

from anaplan_sdk._services import _HttpService
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


class _ScimClient:
    def __init__(self, http: _HttpService) -> None:
        self._http = http
        self._url = "https://api.anaplan.com/scim/1/0/v2"

    def get_service_provider_config(self) -> ServiceProviderConfig:
        """
        Get the SCIM Service Provider Configuration.
        :return: The ServiceProviderConfig object describing the available SCIM features.
        """
        res = self._http.get(f"{self._url}/ServiceProviderConfig")
        return ServiceProviderConfig.model_validate(res)

    def get_resource_types(self) -> list[Resource]:
        """
        Get the SCIM Resource Types.
        :return: A list of Resource objects describing the SCIM resource types.
        """
        res = self._http.get(f"{self._url}/ResourceTypes")
        return [Resource.model_validate(e) for e in res.get("Resources", [])]

    def get_resource_schemas(self) -> list[Schema]:
        """
        Get the SCIM Resource Schemas.
        :return: A list of Schema objects describing the SCIM resource schemas.
        """
        res = self._http.get(f"{self._url}/Schemas")
        return [Schema.model_validate(e) for e in res.get("Resources", [])]

    def get_users(self, predicate: str | field = None, page_size: int = 100) -> list[User]:
        """
        Get a list of users, optionally filtered by a predicate. Keep in mind that this will only
        return internal users. To get a list of all users in the tenant, use the `get_users()`
        in the `audit` namespace instead.
        :param predicate: A filter predicate to filter the users. This can either be a string,
               in which case it will be passed as-is, or an expression. Anaplan supports filtering
               on the following fields: "id", "externalId", "userName", "name.familyName",
               "name.givenName" and "active". It supports the operators "eq", "ne", "gt", "ge",
               "lt", "le" and "pr". It supports logical operators "and" and "or", "not" is not
               supported. It supports grouping with parentheses.
        :param page_size: The number of users to fetch per page. Values above 100 will error.
        :return: The internal users optionally matching the filter.
        """
        params: dict[str, int | str] = {"startIndex": 1, "count": page_size}
        if predicate is not None:
            params["filter"] = str(predicate)
        res = self._http.get(f"{self._url}/Users", params=params)
        users = [User.model_validate(e) for e in res.get("Resources", [])]
        if (total := res["totalResults"]) <= page_size:
            return users
        with ThreadPoolExecutor() as executor:
            pages = executor.map(
                lambda i: self._http.get(
                    f"{self._url}/Users", params=(params | {"startIndex": i, "count": page_size})
                ),
                range(page_size + 1, total + 1, page_size),
            )
        for user in chain(*(p.get("Resources", []) for p in pages)):
            users.append(User.model_validate(user))
        return users

    def get_user(self, user_id: str) -> User:
        """
        Get a user by their ID.
        :param user_id: The ID of the user to fetch.
        :return: The User object.
        """
        res = self._http.get(f"{self._url}/Users/{user_id}")
        return User.model_validate(res)

    def add_user(self, user: UserInput | dict[str, Any]) -> User:
        """
        Add a new user to your Anaplan tenant.
        :param user: The user info to add. Can either be a UserInput object or a dict. If you pass
               a dict, it will be validated against the UserInput model before sending. If the info
               you provided is invalid or incomplete, this will raise a pydantic.ValidationError.
        :return: The created User object.
        """
        res = self._http.post(f"{self._url}/Users", json=construct_payload(UserInput, user))
        return User.model_validate(res)

    def replace_user(self, user_id: str, user: ReplaceUserInput | dict[str, Any]):
        """
        Replace an existing user with new information. Note that this will replace all fields of the
        :param user_id: ID of the user to replace.
        :param user: The new user info. Can either be a ReplaceUserInput object or a dict. If you
               pass a dict, it will be validated against the ReplaceUserInput model before sending.
               If the info you provided is invalid or incomplete, this will raise a
               pydantic.ValidationError.
        :return: The updated User object.
        """
        res = self._http.put(
            f"{self._url}/Users/{user_id}", json=construct_payload(ReplaceUserInput, user)
        )
        return User.model_validate(res)

    def update_user(self, user_id: str, operations: list[Operation] | list[dict[str, Any]]) -> User:
        """
        Update an existing user with a list of operations. This allows you to update only specific
        fields of the user without replacing the entire user.
        :param user_id: The ID of the user to update.
        :param operations: A list of operations to perform on the user. Each operation can either be
               an Operation object or a dict. If you pass a dict, it will be validated against
               the Operation model before sending. If the operation is invalid, this will raise a
               pydantic.ValidationError. You can also use the models Replace, Add and Remove which
               are subclasses of Operation and provide a more convenient way to create operations.
        :return: The updated User object.
        """
        res = self._http.patch(
            f"{self._url}/Users/{user_id}",
            json={
                "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
                "Operations": [construct_payload(Operation, e) for e in operations],
            },
        )
        return User.model_validate(res)
