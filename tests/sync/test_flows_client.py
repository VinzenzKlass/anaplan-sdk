from anaplan_sdk.models.flows import Flow, FlowSummary


def test_list_flows(client):
    flows = client.cw.flows.get_flows()
    assert isinstance(flows, list)
    assert all(isinstance(f, FlowSummary) for f in flows)


def test_list_flows_current_user(client):
    flows = client.cw.flows.get_flows(current_user_only=True)
    assert isinstance(flows, list)
    assert all(isinstance(f, FlowSummary) for f in flows)


def test_create_flow_pydantic(client, flow_pydantic, registry):
    flow_id = client.cw.flows.create_flow(flow_pydantic)
    assert flow_id is not None
    registry["flows"].append(flow_id)


def test_create_flow_dict(client, flow_dict, registry):
    flow_id = client.cw.flows.create_flow(flow_dict)
    assert flow_id is not None
    registry["flows"].append(flow_id)


def test_get_flow(client, registry):
    flow = client.cw.flows.get_flow(registry["flows"][0])
    assert isinstance(flow, Flow)


def test_run_flow(client, test_flow):
    run_id = client.cw.flows.run_flow(test_flow)
    assert run_id is not None


def test_update_flow_pydantic(client, flow_pydantic, registry):
    client.cw.flows.update_flow(registry["flows"][0], flow_pydantic)


def test_update_flow_dict(client, flow_dict, registry):
    client.cw.flows.update_flow(registry["flows"][1], flow_dict)


def test_delete_flow(client, registry):
    _ = (client.cw.flows.delete_flow(f) for f in registry["flows"])
