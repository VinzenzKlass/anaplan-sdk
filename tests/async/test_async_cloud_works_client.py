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


async def test_create_and_delete_connection_pydantic(client, az_blob_connection):
    con_id = await client.cw.create_connection(az_blob_connection)
    assert con_id is not None
    await client.cw.delete_connection(con_id)


async def test_create_and_delete_connection_dict(client, az_blob_connection_dict):
    con_id = await client.cw.create_connection(az_blob_connection_dict)
    assert con_id is not None
    await client.cw.delete_connection(con_id)


async def test_update_connection_pydantic(client, az_blob_connection, connection_id):
    await client.cw.update_connection(connection_id, az_blob_connection.body)


async def test_update_connection_dict(client, az_blob_connection_dict, connection_id):
    await client.cw.update_connection(connection_id, az_blob_connection_dict["body"])


async def test_patch_connection(client, connection_id, name):
    await client.cw.patch_connection(connection_id, {"name": name})


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


async def test_get_integration(client, integration_id):
    assert isinstance(await client.cw.get_integration(integration_id), SingleIntegration)


async def test_create_integration_pydantic(client, integration_pydantic):
    assert await client.cw.create_integration(integration_pydantic) is not None


async def test_create_multi_step_integration_pydantic(client, multi_step_integration_pydantic):
    assert await client.cw.create_integration(multi_step_integration_pydantic) is not None


async def test_create_process_integration_pydantic(client, process_integration_pydantic):
    assert await client.cw.create_integration(process_integration_pydantic) is not None


async def test_update_integration_pydantic(client, integration_id, integration_pydantic):
    await client.cw.update_integration(integration_id, integration_pydantic)


async def test_update_multi_step_integration_pydantic(
    client, multi_integration_id, multi_step_integration_pydantic
):
    await client.cw.update_integration(multi_integration_id, multi_step_integration_pydantic)


async def test_update_process_integration_pydantic(
    client, process_integration_id, process_integration_pydantic
):
    await client.cw.update_integration(process_integration_id, process_integration_pydantic)


async def test_create_integration_dict(client, integration_dict):
    assert await client.cw.create_integration(integration_dict) is not None


async def test_create_multi_step_integration_dict(client, multi_step_integration_dict):
    assert await client.cw.create_integration(multi_step_integration_dict) is not None


async def test_create_process_integration_dict(client, process_integration_dict):
    assert await client.cw.create_integration(process_integration_dict) is not None


async def test_update_integration_dict(client, integration_id, integration_dict):
    await client.cw.update_integration(integration_id, integration_dict)


async def test_update_multi_step_integration_dict(
    client, multi_integration_id, multi_step_integration_dict
):
    await client.cw.update_integration(multi_integration_id, multi_step_integration_dict)


async def test_update_process_integration_dict(
    client, multi_integration_id, process_integration_dict
):
    await client.cw.update_integration(multi_integration_id, process_integration_dict)


async def test_run_integration(client):
    assert await client.cw.run_integration("44cbd206c8204203b8a0ab5667e0396a") is not None


async def test_get_run_history(client, integration_id):
    history = await client.cw.get_run_history(integration_id)
    assert isinstance(history, list)
    assert all((isinstance(i, RunSummary) for i in history))


async def test_get_run_status(client, run_id):
    status = await client.cw.get_run_status(run_id)
    assert isinstance(status, RunStatus)


async def test_create_schedule_pydantic(client, integration_id, schedule_pydantic):
    await client.cw.create_schedule(integration_id, schedule_pydantic)


async def test_update_schedule_pydantic(client, integration_id, schedule_pydantic):
    await client.cw.update_schedule(integration_id, schedule_pydantic)


async def test_set_schedule_enabled(client, integration_id):
    await client.cw.set_schedule_status(integration_id, "enabled")


async def test_set_schedule_disabled(client, integration_id):
    await client.cw.set_schedule_status(integration_id, "disabled")


async def test_delete_schedule(client, integration_id):
    await client.cw.delete_schedule(integration_id)


async def test_create_schedule_dict(client, integration_id, schedule_dict):
    await client.cw.create_schedule(integration_id, schedule_dict)


async def test_update_schedule_dict(client, integration_id, schedule_dict):
    await client.cw.update_schedule(integration_id, schedule_dict)
    await client.cw.delete_schedule(integration_id)


async def test_notification_pydantic(client, notification_pydantic):
    notification_id = await client.cw.create_notification_config(notification_pydantic)
    await client.cw.update_notification_config(notification_id, notification_pydantic)
    await client.cw.delete_notification_config(notification_id)


async def test_create_notification_dict(client, notification_dict):
    notification_id = await client.cw.create_notification_config(notification_dict)
    await client.cw.update_notification_config(notification_id, notification_dict)
    await client.cw.delete_notification_config(notification_id)
