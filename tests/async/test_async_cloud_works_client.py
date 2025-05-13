from asyncio import gather

from anaplan_sdk import AsyncClient
from anaplan_sdk.models.cloud_works import (
    Connection,
    Integration,
    RunSummary,
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
    await client.cw.update_connection(connection_id, az_blob_connection)


async def test_update_connection_dict(client, az_blob_connection_dict, connection_id):
    await client.cw.update_connection(connection_id, az_blob_connection_dict)


async def test_patch_connection(client, connection_id, connection_name):
    await client.cw.patch_connection(connection_id, {"name": connection_name})


async def test_list_integrations(client: AsyncClient):
    integrations_asc, integrations_desc = await gather(
        client.cw.list_integrations(), client.cw.list_integrations(sort_by_name="descending")
    )
    assert isinstance(integrations_asc, list)
    assert isinstance(integrations_desc, list)
    assert all(isinstance(i, Integration) for i in integrations_asc)
    assert all(isinstance(i, Integration) for i in integrations_desc)
    assert len(integrations_asc) == len(integrations_desc)
    assert integrations_asc == list(reversed(integrations_desc))


async def test_run_integration(client: AsyncClient, test_integration_id):
    run_id = await client.cw.run_integration(test_integration_id)
    assert run_id is not None


async def test_get_run_history(client: AsyncClient, test_integration_id):
    history = await client.cw.get_run_history(test_integration_id)
    assert isinstance(history, list)
    assert all((isinstance(i, RunSummary) for i in history))
