from typing import Any

import httpx

from anaplan_sdk._base import _AsyncBaseClient
from anaplan_sdk.models import Connection, ConnectionType


class _AsyncCloudWorksClient(_AsyncBaseClient):
    def __init__(self, client: httpx.AsyncClient, retry_count: int) -> None:
        self._client = client
        self._url = "https://api.cloudworks.anaplan.com/2/0/integrations"
        super().__init__(retry_count, client)

    async def list_connections(self) -> list[Connection]:
        return [
            Connection.model_validate(e)
            for e in await self._get_paginated(f"{self._url}/connections", "connections")
        ]

    async def create_connection(self, con_type: ConnectionType, body: dict[str, Any]) -> str:
        """
        Create a new connection in CloudWorks.
        :param con_type: Which of the supported connection types to create.
        :param body: The connection name and details.
        :return: The ID of the new connection.
        """
        return (
            await self._post(f"{self._url}/connections", json={"type": con_type, "body": body})
        )["connections"]["connectionId"]

    async def update_connection(self, con_id: str, body: dict[str, Any]) -> None:
        """
        Update an existing connection in CloudWorks.
        :param con_id: The ID of the connection to update.
        :param body: The name and details of the connection. You must pass all the same details as
               when initially creating the connection again.
        """
        await self._put(f"{self._url}/connections/{con_id}", json=body)

    async def patch_connection(self, con_id: str, body: dict[str, Any]) -> None:
        """
        Update an existing connection in CloudWorks.
        :param con_id: The ID of the connection to update.
        :param body: The name and details of the connection. You can pass all the same details as
               when initially creating the connection again, or just any one of them.
        """
        await self._patch(f"{self._url}/connections/{con_id}", json=body)
