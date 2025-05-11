from typing import Any, Literal

import httpx

from anaplan_sdk._base import _AsyncBaseClient
from anaplan_sdk.models.cloud_works import (
    Connection,
    ConnectionInput,
    Integration,
    IntegrationInput,
)


class _AsyncCloudWorksClient(_AsyncBaseClient):
    def __init__(self, client: httpx.AsyncClient, retry_count: int) -> None:
        self._url = "https://api.cloudworks.anaplan.com/2/0/integrations"
        super().__init__(retry_count, client)

    async def list_connections(self) -> list[Connection]:
        return [
            Connection.model_validate(e)
            for e in await self._get_paginated(f"{self._url}/connections", "connections")
        ]

    async def create_connection(self, con_info: ConnectionInput | dict[str, Any]) -> str:
        """
        Create a new connection in CloudWorks.
        :param con_info: The connection information. This can be a ConnectionInput instance or a
               dictionary as per the documentation. If a dictionary is passed, it will be validated
               against the ConnectionInput model before sending the request.
        :return: The ID of the new connection.
        """
        if isinstance(con_info, dict):
            con_info = ConnectionInput.model_validate(con_info)
        res = await self._post(
            f"{self._url}/connections", json=con_info.model_dump(exclude_none=True, by_alias=True)
        )
        return res["connections"]["connectionId"]

    async def update_connection(
        self, con_id: str, con_info: ConnectionInput | dict[str, Any]
    ) -> None:
        """
        Update an existing connection in CloudWorks.
        :param con_id: The ID of the connection to update.
        :param con_info: The name and details of the connection. You must pass all the same details
               as when initially creating the connection again. If you want to update only some of
               the details, use the `patch_connection` method instead.
        """
        if isinstance(con_info, dict):
            con_info = ConnectionInput.model_validate(con_info)
        await self._put(
            f"{self._url}/connections/{con_id}",
            json=con_info.model_dump(exclude_none=True, by_alias=True),
        )

    async def patch_connection(self, con_id: str, body: dict[str, Any]) -> None:
        """
        Update an existing connection in CloudWorks.
        :param con_id: The ID of the connection to update.
        :param body: The name and details of the connection. You can pass all the same details as
               when initially creating the connection again, or just any one of them.
        """
        await self._patch(f"{self._url}/connections/{con_id}", json=body)

    async def delete_connection(self, con_id: str) -> None:
        """
        Delete an existing connection in CloudWorks.
        :param con_id: The ID of the connection to delete.
        """
        await self._delete(f"{self._url}/connections/{con_id}")

    async def list_integrations(
        self, sort_by_name: Literal["ascending", "descending"] = "ascending"
    ) -> list[Integration]:
        """
        List all integrations in CloudWorks.
        :param sort_by_name: Sort the integrations by name in ascending or descending order.
        :return: A list of integrations.
        """
        params = {"sortBy": "name" if sort_by_name == "ascending" else "-name"}
        return [
            Integration.model_validate(e)
            for e in await self._get_paginated(f"{self._url}", "integrations", params=params)
        ]

    async def create_integration(self, body: IntegrationInput | dict[str, Any]) -> str:
        """
        Create a new integration in CloudWorks.
        :param body: The integration information. This can be an IntegrationInput instance or a
                dictionary as per the documentation. If a dictionary is passed, it will be validated
                against the IntegrationInput model before sending the request.
        :return: The ID of the new integration.
        """
        if isinstance(body, dict):
            body = IntegrationInput.model_validate(body)
        json = body.model_dump(exclude_none=True, by_alias=True)
        return (await self._post(f"{self._url}", json=json))["integration"]["integrationId"]
