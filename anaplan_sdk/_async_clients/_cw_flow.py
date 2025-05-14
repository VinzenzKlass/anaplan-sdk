from typing import Any

import httpx

from anaplan_sdk._base import _AsyncBaseClient, construct_payload
from anaplan_sdk.models.flows import Flow, FlowInput, FlowSummary


class _AsyncFlowClient(_AsyncBaseClient):
    def __init__(self, client: httpx.AsyncClient, retry_count: int) -> None:
        self._url = "https://api.cloudworks.anaplan.com/2/0/integrationflows"
        super().__init__(retry_count, client)

    async def list_flows(self, current_user_only: bool = False) -> list[FlowSummary]:
        params = {"myIntegrations": 1 if current_user_only else 0}
        return [
            FlowSummary.model_validate(e)
            for e in await self._get_paginated(
                self._url, "integrationFlows", page_size=25, params=params
            )
        ]

    async def get_flow(self, flow_id: str) -> Flow:
        return Flow.model_validate((await self._get(f"{self._url}/{flow_id}"))["integrationFlow"])

    async def run_flow(self, flow_id: str, only_steps: list[str] = None) -> str:
        url = f"{self._url}/{flow_id}/run"
        res = await (
            self._post(url, json={"stepsToRun": only_steps})
            if only_steps
            else self._post_empty(url)
        )
        return res["run"]["id"]

    async def create_flow(self, flow: FlowInput | dict[str, Any]) -> str:
        res = await self._post(self._url, json=construct_payload(FlowInput, flow))
        return res["integrationFlow"]["integrationFlowId"]

    async def update_flow(self, flow_id: str, flow: FlowInput | dict[str, Any]) -> None:
        await self._put(f"{self._url}/{flow_id}", json=construct_payload(FlowInput, flow))

    async def delete_flow(self, flow_id: str) -> None:
        await self._delete(f"{self._url}/{flow_id}")
