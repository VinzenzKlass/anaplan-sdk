from typing import Any

from anaplan_sdk import Client
from anaplan_sdk.models.flows import Flow, FlowInput, FlowSummary
from tests.conftest import PyVersionConfig


def test_list_flows(client: Client) -> None:
    flows = client.cw.flows.get_flows()
    assert isinstance(flows, list)
    assert all(isinstance(f, FlowSummary) for f in flows)


def test_list_flows_current_user(client: Client) -> None:
    flows = client.cw.flows.get_flows(current_user_only=True)
    assert isinstance(flows, list)
    assert all(isinstance(f, FlowSummary) for f in flows)


def test_create_flow_pydantic(
    client: Client, flow_pydantic: FlowInput, registry: dict[str, Any]
) -> None:
    flow_id = client.cw.flows.create_flow(flow_pydantic)
    assert flow_id is not None
    registry["flows"].append(flow_id)


def test_create_flow_dict(
    client: Client, flow_dict: dict[str, Any], registry: dict[str, Any]
) -> None:
    flow_id = client.cw.flows.create_flow(flow_dict)
    assert flow_id is not None
    registry["flows"].append(flow_id)


def test_get_flow(client: Client, registry: dict[str, Any]) -> None:
    flow = client.cw.flows.get_flow(registry["flows"][0])
    assert isinstance(flow, Flow)


def test_run_flow(client: Client, config: PyVersionConfig) -> None:
    run_id = client.cw.flows.run_flow(config.test_flow_sync)
    assert run_id is not None


def test_update_flow_pydantic(
    client: Client, flow_pydantic: FlowInput, registry: dict[str, Any]
) -> None:
    client.cw.flows.update_flow(registry["flows"][0], flow_pydantic)


def test_update_flow_dict(
    client: Client, flow_dict: dict[str, Any], registry: dict[str, Any]
) -> None:
    client.cw.flows.update_flow(registry["flows"][1], flow_dict)


def test_delete_flow(client: Client, registry: dict[str, Any]) -> None:
    _ = (client.cw.flows.delete_flow(f) for f in registry["flows"])
