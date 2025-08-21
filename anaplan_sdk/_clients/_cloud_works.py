import logging
from typing import Any, Literal

import httpx

from anaplan_sdk._base import (
    _BaseClient,
    connection_body_payload,
    construct_payload,
    integration_payload,
    schedule_payload,
)
from anaplan_sdk.models.cloud_works import (
    Connection,
    ConnectionBody,
    ConnectionInput,
    Integration,
    IntegrationInput,
    IntegrationProcessInput,
    NotificationConfig,
    NotificationInput,
    RunError,
    RunStatus,
    RunSummary,
    ScheduleInput,
    SingleIntegration,
)

from ._cw_flow import _FlowClient

logger = logging.getLogger("anaplan_sdk")


class _CloudWorksClient(_BaseClient):
    def __init__(self, client: httpx.Client, retry_count: int, page_size: int) -> None:
        self._url = "https://api.cloudworks.anaplan.com/2/0/integrations"
        self._flow = _FlowClient(client, retry_count=retry_count, page_size=page_size)
        super().__init__(client, retry_count=retry_count, page_size=page_size)

    @property
    def flows(self) -> _FlowClient:
        """
        Access the Integration Flow APIs.
        """
        return self._flow

    def get_connections(self) -> list[Connection]:
        """
        List all Connections available in CloudWorks.
        :return: A list of connections.
        """
        return [
            Connection.model_validate(e)
            for e in self._get_paginated(f"{self._url}/connections", "connections")
        ]

    def create_connection(self, con_info: ConnectionInput | dict[str, Any]) -> str:
        """
        Create a new connection in CloudWorks.
        :param con_info: The connection information. This can be a ConnectionInput instance or a
               dictionary as per the documentation. If a dictionary is passed, it will be validated
               against the ConnectionInput model before sending the request.
        :return: The ID of the new connection.
        """
        res = self._post(
            f"{self._url}/connections", json=construct_payload(ConnectionInput, con_info)
        )
        connection_id = res["connections"]["connectionId"]
        logger.info(f"Created connection '{connection_id}'.")
        return connection_id

    def update_connection(self, con_id: str, con_info: ConnectionBody | dict[str, Any]) -> None:
        """
        Update an existing connection in CloudWorks.
        :param con_id: The ID of the connection to update.
        :param con_info: The name and details of the connection. You must pass all the same details
               as when initially creating the connection again. If you want to update only some of
               the details, use the `patch_connection` method instead.
        """
        self._put(f"{self._url}/connections/{con_id}", json=connection_body_payload(con_info))

    def patch_connection(self, con_id: str, body: dict[str, Any]) -> None:
        """
        Update an existing connection in CloudWorks.
        :param con_id: The ID of the connection to update.
        :param body: The name and details of the connection. You can pass all the same details as
               when initially creating the connection again, or just any one of them.
        """
        self._patch(f"{self._url}/connections/{con_id}", json=body)

    def delete_connection(self, con_id: str) -> None:
        """
        Delete an existing connection in CloudWorks.
        :param con_id: The ID of the connection to delete.
        """
        self._delete(f"{self._url}/connections/{con_id}")
        logger.info(f"Deleted connection '{con_id}'.")

    def get_integrations(
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
            for e in self._get_paginated(f"{self._url}", "integrations", params=params)
        ]

    def get_integration(self, integration_id: str) -> SingleIntegration:
        """
        Get the details of a specific integration in CloudWorks.

        **Note: This will not include the integration type! While present when listing integrations,
        the integration type is not included in the details of a single integration.**
        :param integration_id: The ID of the integration to retrieve.
        :return: The details of the integration, without the integration type.
        """
        return SingleIntegration.model_validate(
            (self._get(f"{self._url}/{integration_id}"))["integration"]
        )

    def create_integration(
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
        integration_id = (self._post(f"{self._url}", json=json))["integration"]["integrationId"]
        logger.info(f"Created integration '{integration_id}'.")
        return integration_id

    def update_integration(
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
        self._put(f"{self._url}/{integration_id}", json=json)

    def run_integration(self, integration_id: str) -> str:
        """
        Run an integration in CloudWorks.
        :param integration_id: The ID of the integration to run.
        :return: The ID of the run instance.
        """
        run_id = (self._post_empty(f"{self._url}/{integration_id}/run"))["run"]["id"]
        logger.info(f"Started integration run '{run_id}' for integration '{integration_id}'.")
        return run_id

    def delete_integration(self, integration_id: str) -> None:
        """
        Delete an existing integration in CloudWorks.
        :param integration_id: The ID of the integration to delete.
        """
        self._delete(f"{self._url}/{integration_id}")
        logger.info(f"Deleted integration '{integration_id}'.")

    def get_run_history(self, integration_id: str) -> list[RunSummary]:
        """
        Get the run history of a specific integration in CloudWorks.
        :param integration_id: The ID of the integration to retrieve the run history for.
        :return: A list of run statuses.
        """
        return [
            RunSummary.model_validate(e)
            for e in (self._get(f"{self._url}/runs/{integration_id}"))["history_of_runs"].get(
                "runs", []
            )
        ]

    def get_run_status(self, run_id: str) -> RunStatus:
        """
        Get the status of a specific run in CloudWorks.
        :param run_id: The ID of the run to retrieve.
        :return: The details of the run.
        """
        return RunStatus.model_validate((self._get(f"{self._url}/run/{run_id}"))["run"])

    def get_run_error(self, run_id: str) -> RunError | None:
        """
        Get the error details of a specific run in CloudWorks. This exposes potential underlying
        errors like the error of the invoked action, failure dumps and other details.
        :param run_id: The ID of the run to retrieve.
        :return: The details of the run error.
        """
        run = self._get(f"{self._url}/runerror/{run_id}")
        return RunError.model_validate(run["runs"]) if run.get("runs") else None

    def create_schedule(
        self, integration_id: str, schedule: ScheduleInput | dict[str, Any]
    ) -> None:
        """
        Schedule an integration in CloudWorks.
        :param integration_id: The ID of the integration to schedule.
        :param schedule: The schedule information. This can be a ScheduleInput instance or a
               dictionary as per the documentation. If a dictionary is passed, it will be validated
               against the ScheduleInput model before sending the request.
        """
        self._post(
            f"{self._url}/{integration_id}/schedule",
            json=schedule_payload(integration_id, schedule),
        )
        logger.info(f"Created schedule for integration '{integration_id}'.")

    def update_schedule(
        self, integration_id: str, schedule: ScheduleInput | dict[str, Any]
    ) -> None:
        """
        Update an integration Schedule in CloudWorks. A schedule must already exist.
        :param integration_id: The ID of the integration to schedule.
        :param schedule: The schedule information. This can be a ScheduleInput instance or a
               dictionary as per the documentation. If a dictionary is passed, it will be validated
               against the ScheduleInput model before sending the request.
        """
        self._put(
            f"{self._url}/{integration_id}/schedule",
            json=schedule_payload(integration_id, schedule),
        )
        logger.info(f"Updated schedule for integration '{integration_id}'.")

    def set_schedule_status(
        self, integration_id: str, status: Literal["enabled", "disabled"]
    ) -> None:
        """
        Set the status of an integration schedule in CloudWorks. A schedule must already exist.
        :param integration_id: The ID of the integration to schedule.
        :param status: The status of the schedule. This can be either "enabled" or "disabled".
        """
        self._post_empty(f"{self._url}/{integration_id}/schedule/status/{status}")
        logger.info(f"Set schedule status to '{status}' for integration '{integration_id}'.")

    def delete_schedule(self, integration_id: str) -> None:
        """
        Delete an integration schedule in CloudWorks. A schedule must already exist.
        :param integration_id: The ID of the integration to schedule.
        """
        self._delete(f"{self._url}/{integration_id}/schedule")
        logger.info(f"Deleted schedule for integration '{integration_id}'.")

    def get_notification_config(
        self, notification_id: str | None = None, integration_id: str | None = None
    ) -> NotificationConfig:
        """
        Get the notification configuration, either by its Id, or the notification configuration
        for a specific integration. If the integration_id is specified, the notification_id
        will be ignored.
        :param notification_id: The ID of the notification configuration to retrieve.
        :param integration_id: The ID of the integration to retrieve the notification
               configuration for.
        :return: The details of the notification configuration.
        """
        if not (notification_id or integration_id):
            raise ValueError("Either notification_id or integration_id must be specified.")
        if integration_id:
            notification_id = (self.get_integration(integration_id)).notification_id
        return NotificationConfig.model_validate(
            (self._get(f"{self._url}/notification/{notification_id}"))["notifications"]
        )

    def create_notification_config(self, config: NotificationInput | dict[str, Any]) -> str:
        """
        Create a notification configuration for an integration in CloudWorks. This will error if
        there is already a notification configuration for the integration, which is also the case
        by default. In this case, you will want to use the `update_notification_config` method
        instead, to partially update the existing configuration or overwrite it.
        :param config: The notification configuration. This can be a NotificationInput instance or
               a dictionary as per the documentation. If a dictionary is passed, it will be
               validated against the NotificationConfig model before sending the request.
        :return: The ID of the new notification configuration.
        """
        res = self._post(
            f"{self._url}/notification", json=construct_payload(NotificationInput, config)
        )
        notification_id = res["notification"]["notificationId"]
        logger.info(f"Created notification configuration '{notification_id}'.")
        return notification_id

    def update_notification_config(
        self, notification_id: str, config: NotificationInput | dict[str, Any]
    ) -> None:
        """
        Update a notification configuration for an integration in CloudWorks. You cannot pass empty
        values or nulls to any of the fields If you want to for e.g. override  an existing list of
        users with an empty one, you must delete the notification configuration and create a new
        one with only the values you want to keep.
        :param notification_id: The ID of the notification configuration to update.
        :param config: The notification configuration. This can be a NotificationInput instance or
               a dictionary as per the documentation. If a dictionary is passed, it will be
               validated against the NotificationConfig model before sending the request.
        """
        self._put(
            f"{self._url}/notification/{notification_id}",
            json=construct_payload(NotificationInput, config),
        )

    def delete_notification_config(
        self, notification_id: str | None = None, integration_id: str | None = None
    ) -> None:
        """
        Delete a notification configuration for an integration in CloudWorks, either by its Id, or
        the notification configuration for a specific integration. If the integration_id is
        specified, the notification_id will be ignored.
        :param notification_id: The ID of the notification configuration to delete.
        :param integration_id: The ID of the integration to delete the notification config of.
        """
        if not (notification_id or integration_id):
            raise ValueError("Either notification_id or integration_id must be specified.")
        if integration_id:
            notification_id = (self.get_integration(integration_id)).notification_id
        self._delete(f"{self._url}/notification/{notification_id}")
        logger.info(f"Deleted notification configuration '{notification_id}'.")

    def get_import_error_dump(self, run_id: str) -> bytes:
        """
        Get the error dump of a specific import run in CloudWorks. Calling this for a run_id that
        did not generate any failure dumps will produce an error.

        **Note that if you need the error dump of an action in a process, you must use the
        `get_process_error_dump` method instead.**
        :param run_id: The ID of the run to retrieve.
        :return: The error dump.
        """
        return self._get_binary(f"{self._url}/run/{run_id}/dump")

    def get_process_error_dump(self, run_id: str, action_id: int | str) -> bytes:
        """
        Get the error dump of a specific import run in CloudWorks, that is part of a process.
        Calling this for a run_id that did not generate any failure dumps will produce an error.
        :param run_id: The ID of the run to retrieve.
        :param action_id: The ID of the action to retrieve. This can be found in the RunError.
        :return: The error dump.
        """
        return self._get_binary(f"{self._url}/run/{run_id}/process/import/{action_id}/dumps")
