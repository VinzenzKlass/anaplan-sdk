from asyncio import gather

from anaplan_sdk.models.flows import Flow, FlowSummary


async def test_list_flows(client):
    flows = await client.cw.flows.get_flows()
    assert isinstance(flows, list)
    assert all(isinstance(f, FlowSummary) for f in flows)


async def test_list_flows_current_user(client):
    flows = await client.cw.flows.get_flows(current_user_only=True)
    assert isinstance(flows, list)
    assert all(isinstance(f, FlowSummary) for f in flows)


async def test_create_flow_pydantic(client, flow_pydantic, registry):
    flow_id = await client.cw.flows.create_flow(flow_pydantic)
    assert flow_id is not None
    registry["flows"].append(flow_id)


async def test_create_flow_dict(client, flow_dict, registry):
    flow_id = await client.cw.flows.create_flow(flow_dict)
    assert flow_id is not None
    registry["flows"].append(flow_id)


async def test_get_flow(client, registry):
    flow = await client.cw.flows.get_flow(registry["flows"][0])
    assert isinstance(flow, Flow)


async def test_run_flow(client, test_flow):
    run_id = await client.cw.flows.run_flow(test_flow)
    assert run_id is not None


async def test_update_flow_pydantic(client, flow_pydantic, registry):
    await client.cw.flows.update_flow(registry["flows"][0], flow_pydantic)


async def test_update_flow_dict(client, flow_dict, registry):
    await client.cw.flows.update_flow(registry["flows"][1], flow_dict)


async def test_delete_flow(client, registry):
    await gather(*(client.cw.flows.delete_flow(f) for f in registry["flows"]))
