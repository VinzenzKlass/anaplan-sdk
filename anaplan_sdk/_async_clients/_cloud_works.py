from typing import Any, Literal

import httpx

from anaplan_sdk._base import (
    _AsyncBaseClient,
    construct_payload,
    integration_payload,
    schedule_payload,
)
from anaplan_sdk.models.cloud_works import (
    Connection,
    ConnectionInput,
    Integration,
    IntegrationInput,
    IntegrationProcessInput,
    RunStatus,
    RunSummary,
    ScheduleInput,
    SingleIntegration,
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
        res = await self._post(
            f"{self._url}/connections", json=construct_payload(ConnectionInput, con_info)
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
        await self._put(
            f"{self._url}/connections/{con_id}", json=construct_payload(ConnectionInput, con_info)
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

    async def get_integration(self, integration_id: str) -> SingleIntegration:
        """
        Get the details of a specific integration in CloudWorks.

        **Note: This will not include the integration type! While present when listing integrations,
        the integration type is not included in the details of a single integration.**
        :param integration_id: The ID of the integration to retrieve.
        :return: The details of the integration, without the integration type.
        """
        return SingleIntegration.model_validate(
            (await self._get(f"{self._url}/{integration_id}"))["integration"]
        )

    async def create_integration(
        self, body: IntegrationInput | IntegrationProcessInput | dict[str, Any]
    ) -> str:
        """
        Create a new integration in CloudWorks. If not specified, the integration type will be
        either "Import" or "Export" based on the source and target you provide.

        If you want to instead create a process Integration, you can do so by specifying
        the `process_id` parameter and passing several jobs. **Be careful to ensure, that all ids
        specified in the job inputs match what is defined in your model and matches the process.**
        If this is not the case, this will error, occasionally with a misleading error message,
        i.e. `XYZ is not defined in your model` even though it is, Anaplan just does not know what
        to do with it in the location you specified.

        You can also use CloudWorks Integrations to simply schedule a process. To do this, you
        can simply pass an IntegrationProcessInput instance with the process_id and no jobs. This
        will create a process integration that will run the process you specified.
        :param body: The integration information. This can be an
                IntegrationInput | IntegrationProcessInput instance or a dictionary as per the
                documentation. If a dictionary is passed, it will be validated against the
                IntegrationInput model before sending the request.
        :return: The ID of the new integration.
        """
        json = integration_payload(body)
        return (await self._post(f"{self._url}", json=json))["integration"]["integrationId"]

    async def update_integration(
        self, integration_id: str, body: IntegrationInput | IntegrationProcessInput | dict[str, Any]
    ) -> None:
        """
        Update an existing integration in CloudWorks.
        :param integration_id: The ID of the integration to update.
        :param body: The name and details of the integration. You must pass all the same details
                as when initially creating the integration again. If you want to update only some
                of the details, use the `patch_integration` method instead.
        """
        json = integration_payload(body)
        await self._put(f"{self._url}/{integration_id}", json=json)

    async def run_integration(self, integration_id: str) -> str:
        """
        Run an integration in CloudWorks.
        :param integration_id: The ID of the integration to run.
        :return: The ID of the run instance.
        """
        return (await self._post_empty(f"{self._url}/{integration_id}/run"))["run"]["id"]

    async def delete_integration(self, integration_id: str) -> None:
        """
        Delete an existing integration in CloudWorks.
        :param integration_id: The ID of the integration to delete.
        """
        await self._delete(f"{self._url}/{integration_id}")

    async def get_run_history(self, integration_id: str) -> list[RunSummary]:
        """
        Get the run history of a specific integration in CloudWorks.
        :param integration_id: The ID of the integration to retrieve the run history for.
        :return: A list of run statuses.
        """
        return [
            RunSummary.model_validate(e)
            for e in (await self._get(f"{self._url}/runs/{integration_id}"))["history_of_runs"].get(
                "runs", []
            )
        ]

    async def get_run_status(self, run_id: str) -> RunStatus:
        """
        Get the status of a specific run in CloudWorks.
        :param run_id: The ID of the run to retrieve.
        :return: The details of the run.
        """
        return RunStatus.model_validate((await self._get(f"{self._url}/run/{run_id}"))["run"])

    async def create_schedule(
        self, integration_id: str, schedule: ScheduleInput | dict[str, Any]
    ) -> None:
        """
        Schedule an integration in CloudWorks.
        :param integration_id: The ID of the integration to schedule.
        :param schedule: The schedule information. This can be a ScheduleInput instance or a
               dictionary as per the documentation. If a dictionary is passed, it will be validated
               against the ScheduleInput model before sending the request.
        """
        await self._post(
            f"{self._url}/{integration_id}/schedule",
            json=schedule_payload(integration_id, schedule),
        )

    async def update_schedule(
        self, integration_id: str, schedule: ScheduleInput | dict[str, Any]
    ) -> None:
        """
        Update an integration Schedule in CloudWorks. A schedule must already exist.
        :param integration_id: The ID of the integration to schedule.
        :param schedule: The schedule information. This can be a ScheduleInput instance or a
               dictionary as per the documentation. If a dictionary is passed, it will be validated
               against the ScheduleInput model before sending the request.
        """
        await self._put(
            f"{self._url}/{integration_id}/schedule",
            json=schedule_payload(integration_id, schedule),
        )

    async def set_schedule_status(
        self, integration_id: str, status: Literal["enabled", "disabled"]
    ) -> None:
        """
        Set the status of an integration schedule in CloudWorks. A schedule must already exist.
        :param integration_id: The ID of the integration to schedule.
        :param status: The status of the schedule. This can be either "enabled" or "disabled".
        """
        await self._post_empty(f"{self._url}/{integration_id}/schedule/status/{status}")

    async def delete_schedule(self, integration_id: str) -> None:
        """
        Delete an integration schedule in CloudWorks. A schedule must already exist.
        :param integration_id: The ID of the integration to schedule.
        """
        await self._delete(f"{self._url}/{integration_id}/schedule")
