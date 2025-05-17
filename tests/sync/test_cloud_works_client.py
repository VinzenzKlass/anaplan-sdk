from anaplan_sdk.models.cloud_works import (
    Connection,
    Integration,
    RunError,
    RunStatus,
    RunSummary,
    SingleIntegration,
)


def test_list_connections(client):
    connections = client.cw.list_connections()
    assert isinstance(connections, list)
    assert all(isinstance(c, Connection) for c in connections)


def test_create_connection_pydantic(client, az_blob_connection, registry):
    con_id = client.cw.create_connection(az_blob_connection)
    assert con_id is not None
    registry["connections"].append(con_id)


def test_create_connection_dict(client, az_blob_connection_dict, registry):
    con_id = client.cw.create_connection(az_blob_connection_dict)
    assert con_id is not None
    registry["connections"].append(con_id)


def test_update_connection_pydantic(client, az_blob_connection, registry):
    client.cw.update_connection(registry["connections"][0], az_blob_connection.body)


def test_update_connection_dict(client, az_blob_connection_dict, registry):
    client.cw.update_connection(registry["connections"][-1], az_blob_connection_dict["body"])


def test_patch_connection(client, name, registry):
    client.cw.patch_connection(registry["connections"][-1], {"name": name})


def test_get_integration(client, registry, test_integration):
    assert isinstance(client.cw.get_integration(test_integration), SingleIntegration)


def test_list_integrations(client):
    integrations_asc = client.cw.list_integrations()
    assert isinstance(integrations_asc, list)
    assert all(isinstance(i, Integration) for i in integrations_asc)


def test_list_integrations_desc(client):
    integrations_desc = client.cw.list_integrations(sort_by_name="descending")
    assert isinstance(integrations_desc, list)
    assert all(isinstance(i, Integration) for i in integrations_desc)


def test_create_integration_pydantic(client, integration_pydantic, registry):
    integration_id = client.cw.create_integration(integration_pydantic)
    assert integration_id is not None
    registry["integrations"].append(integration_id)


def test_create_multi_step_integration_pydantic(client, multi_step_integration_pydantic, registry):
    integration_id = client.cw.create_integration(multi_step_integration_pydantic)
    assert integration_id is not None
    registry["integrations"].append(integration_id)


def test_create_process_integration_pydantic(client, process_integration_pydantic, registry):
    integration_id = client.cw.create_integration(process_integration_pydantic)
    assert integration_id is not None
    registry["integrations"].append(integration_id)


def test_update_integration_pydantic(client, integration_pydantic, registry):
    client.cw.update_integration(registry["integrations"][0], integration_pydantic)


def test_update_multi_step_integration_pydantic(client, registry, multi_step_integration_pydantic):
    client.cw.update_integration(registry["integrations"][1], multi_step_integration_pydantic)


def test_update_process_integration_pydantic(client, registry, process_integration_pydantic):
    client.cw.update_integration(registry["integrations"][-1], process_integration_pydantic)


def test_create_integration_dict(client, integration_dict, registry):
    integration_id = client.cw.create_integration(integration_dict)
    assert integration_id is not None
    registry["integrations"].append(integration_id)


def test_create_multi_step_integration_dicts(client, multi_step_integration_dict, registry):
    integration_id = client.cw.create_integration(multi_step_integration_dict)
    assert integration_id is not None
    registry["integrations"].append(integration_id)


def test_create_process_integration_dicts(client, multi_step_integration_dict, registry):
    integration_id = client.cw.create_integration(multi_step_integration_dict)
    assert integration_id is not None
    registry["integrations"].append(integration_id)


def test_update_integration_dict(client, integration_dict, registry):
    client.cw.update_integration(registry["integrations"][-3], integration_dict)


def test_update_multi_step_integration_dict(client, registry, multi_step_integration_dict):
    client.cw.update_integration(registry["integrations"][-2], multi_step_integration_dict)


def test_update_process_integration_dict(client, registry, process_integration_pydantic):
    client.cw.update_integration(registry["integrations"][-1], process_integration_pydantic)


def test_run_integration(client, test_integration, registry):
    run_id = client.cw.run_integration(test_integration)
    assert run_id is not None
    registry["run_id"] = run_id


def test_get_run_history(client, registry):
    history = client.cw.get_run_history(registry["integrations"][-1])
    assert isinstance(history, list)
    assert all((isinstance(i, RunSummary) for i in history))


def test_get_run_status(client, registry):
    status = client.cw.get_run_status(registry["run_id"])
    assert isinstance(status, RunStatus)


def test_create_schedule_pydantic(client, registry, schedule_pydantic):
    client.cw.create_schedule(registry["integrations"][0], schedule_pydantic)


def test_update_schedule_pydantic(client, registry, schedule_pydantic):
    client.cw.update_schedule(registry["integrations"][0], schedule_pydantic)


def test_set_schedule_enabled(client, registry):
    client.cw.set_schedule_status(registry["integrations"][0], "enabled")


def test_set_schedule_disabled(client, registry):
    client.cw.set_schedule_status(registry["integrations"][0], "disabled")


def test_delete_schedule(client, registry):
    client.cw.delete_schedule(registry["integrations"][0])


def test_create_schedule_dict(client, registry, schedule_dict):
    client.cw.create_schedule(registry["integrations"][0], schedule_dict)


def test_update_schedule_dict(client, registry, schedule_dict):
    client.cw.update_schedule(registry["integrations"][0], schedule_dict)


def test_update_notification_dict(client, test_notification, notification_dict, test_integration):
    notification_dict["integrationIds"] = [test_integration]
    client.cw.update_notification_config(test_notification, notification_dict)


def test_delete_notification(client, registry):
    client.cw.delete_notification_config(integration_id=registry["integrations"][0])


def test_create_notification_dict(client, notification_dict, registry):
    notification_dict["integrationIds"] = [registry["integrations"][0]]
    client.cw.create_notification_config(notification_dict)


def test_get_run_error(client, error_run_id):
    run_error = client.cw.get_run_error(error_run_id)
    assert isinstance(run_error, RunError)


def test_delete_integration(client, registry):
    _ = (client.cw.delete_integration(i) for i in registry["integrations"])


def test_delete_connection(client, registry):
    _ = (client.cw.delete_connection(c) for c in registry["connections"])
