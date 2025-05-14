from asyncio import gather

from anaplan_sdk.models.cloud_works import (
    Connection,
    Integration,
    RunStatus,
    RunSummary,
    SingleIntegration,
)


async def test_list_connections(client):
    connections = await client.cw.list_connections()
    assert isinstance(connections, list)
    assert all(isinstance(c, Connection) for c in connections)


async def test_create_connection_pydantic(client, az_blob_connection, registry):
    con_id = await client.cw.create_connection(az_blob_connection)
    assert con_id is not None
    registry["connections"].append(con_id)


async def test_create_connection_dict(client, az_blob_connection_dict, registry):
    con_id = await client.cw.create_connection(az_blob_connection_dict)
    assert con_id is not None
    registry["connections"].append(con_id)


async def test_update_connection_pydantic(client, az_blob_connection, registry):
    await client.cw.update_connection(registry["connections"][0], az_blob_connection.body)


async def test_update_connection_dict(client, az_blob_connection_dict, registry):
    await client.cw.update_connection(registry["connections"][-1], az_blob_connection_dict["body"])


async def test_patch_connection(client, name, registry):
    await client.cw.patch_connection(registry["connections"][-1], {"name": name})


async def test_list_integrations(client):
    integrations_asc, integrations_desc = await gather(
        client.cw.list_integrations(), client.cw.list_integrations(sort_by_name="descending")
    )
    assert isinstance(integrations_asc, list)
    assert isinstance(integrations_desc, list)
    assert all(isinstance(i, Integration) for i in integrations_asc)
    assert all(isinstance(i, Integration) for i in integrations_desc)
    assert len(integrations_asc) == len(integrations_desc)
    assert integrations_asc == list(reversed(integrations_desc))


async def test_create_integration_pydantic(client, integration_pydantic, registry):
    integration_id = await client.cw.create_integration(integration_pydantic)
    assert integration_id is not None
    registry["integrations"].append(integration_id)


async def test_create_multi_step_integration_pydantic(
    client, multi_step_integration_pydantic, registry
):
    integration_id = await client.cw.create_integration(multi_step_integration_pydantic)
    assert integration_id is not None
    registry["integrations"].append(integration_id)


async def test_create_process_integration_pydantic(client, process_integration_pydantic, registry):
    integration_id = await client.cw.create_integration(process_integration_pydantic)
    assert integration_id is not None
    registry["integrations"].append(integration_id)


async def test_update_integration_pydantic(client, integration_pydantic, registry):
    await client.cw.update_integration(registry["integrations"][0], integration_pydantic)


async def test_update_multi_step_integration_pydantic(
    client, registry, multi_step_integration_pydantic
):
    await client.cw.update_integration(registry["integrations"][1], multi_step_integration_pydantic)


async def test_update_process_integration_pydantic(client, registry, process_integration_pydantic):
    await client.cw.update_integration(registry["integrations"][-1], process_integration_pydantic)


async def test_create_integration_dict(client, integration_dict, registry):
    integration_id = await client.cw.create_integration(integration_dict)
    assert integration_id is not None
    registry["integrations"].append(integration_id)


async def test_create_multi_step_integration_dicts(client, multi_step_integration_dict, registry):
    integration_id = await client.cw.create_integration(multi_step_integration_dict)
    assert integration_id is not None
    registry["integrations"].append(integration_id)


async def test_create_process_integration_dicts(client, multi_step_integration_dict, registry):
    integration_id = await client.cw.create_integration(multi_step_integration_dict)
    assert integration_id is not None
    registry["integrations"].append(integration_id)


async def test_update_integration_dict(client, integration_dict, registry):
    await client.cw.update_integration(registry["integrations"][-3], integration_dict)


async def test_update_multi_step_integration_dict(client, registry, multi_step_integration_dict):
    await client.cw.update_integration(registry["integrations"][-2], multi_step_integration_dict)


async def test_update_process_integration_dict(client, registry, process_integration_pydantic):
    await client.cw.update_integration(registry["integrations"][-1], process_integration_pydantic)


async def test_run_integration(client, test_integration, registry):
    run_id = await client.cw.run_integration(test_integration)
    assert run_id is not None
    registry["run_id"] = run_id


async def test_get_run_history(client, registry):
    history = await client.cw.get_run_history(registry["integrations"][-1])
    assert isinstance(history, list)
    assert all((isinstance(i, RunSummary) for i in history))


async def test_get_run_status(client, registry):
    status = await client.cw.get_run_status(registry["run_id"])
    assert isinstance(status, RunStatus)


async def test_create_schedule_pydantic(client, registry, schedule_pydantic):
    await client.cw.create_schedule(registry["integrations"][0], schedule_pydantic)


async def test_update_schedule_pydantic(client, registry, schedule_pydantic):
    await client.cw.update_schedule(registry["integrations"][0], schedule_pydantic)


async def test_set_schedule_enabled(client, registry):
    await client.cw.set_schedule_status(registry["integrations"][0], "enabled")


async def test_set_schedule_disabled(client, registry):
    await client.cw.set_schedule_status(registry["integrations"][0], "disabled")


async def test_delete_schedule(client, registry):
    await client.cw.delete_schedule(registry["integrations"][0])


async def test_create_schedule_dict(client, registry, schedule_dict):
    await client.cw.create_schedule(registry["integrations"][0], schedule_dict)


async def test_update_schedule_dict(client, registry, schedule_dict):
    await client.cw.update_schedule(registry["integrations"][0], schedule_dict)


async def test_get_integration(client, registry):
    integration_id = await client.cw.get_integration(registry["integrations"][-2])
    assert isinstance(integration_id, SingleIntegration)
    registry["notification"] = integration_id.notification_id


async def test_update_notification_pydantic(client, registry, notification_pydantic):
    notification_pydantic.integration_ids = [registry["integrations"][-2]]
    await client.cw.update_notification_config(registry["notification"], notification_pydantic)


async def test_update_notification_dict(client, registry, notification_dict):
    notification_dict["integration_ids"] = [registry["integrations"][-2]]
    await client.cw.update_notification_config(registry["notification"], notification_dict)


async def test_delete_notification(client, registry):
    await gather(
        client.cw.delete_notification_config(registry["notification"]),
        client.cw.delete_notification_config(integration_id=registry["integrations"][-1]),
    )


async def test_create_notification_dict(client, registry, notification_dict):
    notification_dict["integrationIds"] = [registry["integrations"][-2]]
    await client.cw.create_notification_config(notification_dict)


async def test_delete_integration(client, registry):
    await gather(*(client.cw.delete_integration(i) for i in registry["integrations"]))


async def test_delete_connection(client, registry):
    await gather(*(client.cw.delete_connection(c) for c in registry["connections"]))
