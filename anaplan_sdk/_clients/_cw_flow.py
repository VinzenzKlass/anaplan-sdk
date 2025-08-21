import logging
from typing import Any

import httpx

from anaplan_sdk._base import _BaseClient, construct_payload
from anaplan_sdk.models.flows import Flow, FlowInput, FlowSummary

logger = logging.getLogger("anaplan_sdk")


class _FlowClient(_BaseClient):
    def __init__(self, client: httpx.Client, retry_count: int, page_size: int) -> None:
        self._url = "https://api.cloudworks.anaplan.com/2/0/integrationflows"
        super().__init__(client, retry_count=retry_count, page_size=page_size)

    def get_flows(self, current_user_only: bool = False) -> list[FlowSummary]:
        """
        List all flows in CloudWorks.
        :param current_user_only: Filters the flows to only those created by the current user.
        :return: A list of FlowSummaries.
        """
        params = {"myIntegrations": 1 if current_user_only else 0}
        return [
            FlowSummary.model_validate(e)
            for e in self._get_paginated(self._url, "integrationFlows", page_size=25, params=params)
        ]

    def get_flow(self, flow_id: str) -> Flow:
        """
        Get a flow by its ID. This returns the full flow object, including the contained steps and
        continuation behavior.
        :param flow_id: The ID of the flow to get.
        :return: The Flow object.
        """
        return Flow.model_validate((self._get(f"{self._url}/{flow_id}"))["integrationFlow"])

    def run_flow(self, flow_id: str, only_steps: list[str] = None) -> str:
        """
        Run a flow by its ID. Make sure that neither the flow nor any of its contained are running.
        If this is the case, the task will error. Anaplan neither schedules these tasks nor can it
        handle concurrent executions.
        :param flow_id: The ID of the flow to run.
        :param only_steps: A list of step IDs to run. If not provided, only these will be run.
        :return: The ID of the run.
        """
        url = f"{self._url}/{flow_id}/run"
        res = (
            self._post(url, json={"stepsToRun": only_steps})
            if only_steps
            else self._post_empty(url)
        )
        run_id = res["run"]["id"]
        logger.info(f"Started flow run '{run_id}' for flow '{flow_id}'.")
        return run_id

    def create_flow(self, flow: FlowInput | dict[str, Any]) -> str:
        """
        Create a new flow in CloudWorks. Be careful not to omit the `depends_on` field. Anaplan
        will accept these values, but an invalid, corrupted flow will be created, as all Flows must
        have at least 2 Steps, and they must always be sequential
        :param flow: The flow to create. This can be a FlowInput object or a dictionary.
        :return: The ID of the created flow.
        """
        res = self._post(self._url, json=construct_payload(FlowInput, flow))
        flow_id = res["integrationFlow"]["integrationFlowId"]
        logger.info(f"Created flow '{flow_id}'.")
        return flow_id

    def update_flow(self, flow_id: str, flow: FlowInput | dict[str, Any]) -> None:
        """
        Update a flow in CloudWorks. You must provide the full flow object, partial updates are not
        supported.
        :param flow_id: The ID of the flow to update.
        :param flow: The flow to update. This can be a FlowInput object or a dictionary.
        """
        self._put(f"{self._url}/{flow_id}", json=construct_payload(FlowInput, flow))
        logger.info(f"Updated flow '{flow_id}'.")

    def delete_flow(self, flow_id: str) -> None:
        """
        Delete a flow in CloudWorks. This will not delete its contained steps. This will fail if
        the flow is running or if it has any running steps.
        :param flow_id: The ID of the flow to delete.
        """
        self._delete(f"{self._url}/{flow_id}")
        logger.info(f"Deleted flow '{flow_id}'.")
