from asyncio import gather
from typing import Any, Callable

import anaplan_sdk.models.cloud_works as cwm
from anaplan_sdk import AsyncClient
from anaplan_sdk.models.cloud_works import Connection, Integration, RunError, RunStatus, RunSummary
from tests.conftest import PyVersionConfig


async def test_list_connections(client: AsyncClient) -> None:
    connections = await client.cw.get_connections()
    assert isinstance(connections, list)
    assert all(isinstance(c, Connection) for c in connections)


async def test_create_connection_pydantic(
    client: AsyncClient, az_blob_connection: cwm.ConnectionInput, registry: dict[str, Any]
) -> None:
    con_id = await client.cw.create_connection(az_blob_connection)
    assert con_id is not None
    registry["connections"].append(con_id)


async def test_create_connection_dict(
    client: AsyncClient, az_blob_connection_dict: dict[str, Any], registry: dict[str, Any]
) -> None:
    con_id = await client.cw.create_connection(az_blob_connection_dict)
    assert con_id is not None
    registry["connections"].append(con_id)


async def test_update_connection_pydantic(
    client: AsyncClient, az_blob_connection: cwm.ConnectionInput, registry: dict[str, Any]
) -> None:
    await client.cw.update_connection(registry["connections"][0], az_blob_connection.body)


async def test_update_connection_dict(
    client: AsyncClient, az_blob_connection_dict: dict[str, Any], registry: dict[str, Any]
) -> None:
    await client.cw.update_connection(registry["connections"][-1], az_blob_connection_dict["body"])


async def test_patch_connection(client: AsyncClient, name: str, registry: dict[str, Any]) -> None:
    await client.cw.patch_connection(registry["connections"][-1], {"name": name})


async def test_get_integration(
    client: AsyncClient,
    test_integration_ids: list[str],
    integration_validator: Callable[[list[cwm.SingleIntegration]], None],
) -> None:
    integrations = await gather(*(client.cw.get_integration(i) for i in test_integration_ids))
    integration_validator(integrations)


async def test_list_integrations(client: AsyncClient) -> None:
    integrations_asc = await client.cw.get_integrations()
    assert isinstance(integrations_asc, list)
    assert all(isinstance(i, Integration) for i in integrations_asc)


async def test_list_integrations_desc(client: AsyncClient) -> None:
    integrations_desc = await client.cw.get_integrations(sort_by="name", descending=True)
    assert isinstance(integrations_desc, list)
    assert all(isinstance(i, Integration) for i in integrations_desc)


async def test_create_integration_pydantic(
    client: AsyncClient, integration_pydantic: cwm.IntegrationInput, registry: dict[str, Any]
) -> None:
    integration_id = await client.cw.create_integration(integration_pydantic)
    assert integration_id is not None
    registry["integrations"].append(integration_id)


async def test_create_multi_step_integration_pydantic(
    client: AsyncClient,
    multi_step_integration_pydantic: cwm.IntegrationInput,
    registry: dict[str, Any],
) -> None:
    integration_id = await client.cw.create_integration(multi_step_integration_pydantic)
    assert integration_id is not None
    registry["integrations"].append(integration_id)


async def test_create_process_integration_pydantic(
    client: AsyncClient,
    process_integration_pydantic: cwm.IntegrationProcessInput,
    registry: dict[str, Any],
) -> None:
    integration_id = await client.cw.create_integration(process_integration_pydantic)
    assert integration_id is not None
    registry["integrations"].append(integration_id)


async def test_update_integration_pydantic(
    client: AsyncClient, integration_pydantic: cwm.IntegrationInput, registry: dict[str, Any]
) -> None:
    await client.cw.update_integration(registry["integrations"][0], integration_pydantic)


async def test_update_multi_step_integration_pydantic(
    client: AsyncClient,
    registry: dict[str, Any],
    multi_step_integration_pydantic: cwm.IntegrationInput,
) -> None:
    await client.cw.update_integration(registry["integrations"][1], multi_step_integration_pydantic)


async def test_update_process_integration_pydantic(
    client: AsyncClient,
    registry: dict[str, Any],
    process_integration_pydantic: cwm.IntegrationProcessInput,
) -> None:
    await client.cw.update_integration(registry["integrations"][-1], process_integration_pydantic)


async def test_create_integration_dict(
    client: AsyncClient, integration_dict: dict[str, Any], registry: dict[str, Any]
) -> None:
    integration_id = await client.cw.create_integration(integration_dict)
    assert integration_id is not None
    registry["integrations"].append(integration_id)


async def test_create_multi_step_integration_dicts(
    client: AsyncClient, multi_step_integration_dict: dict[str, Any], registry: dict[str, Any]
) -> None:
    integration_id = await client.cw.create_integration(multi_step_integration_dict)
    assert integration_id is not None
    registry["integrations"].append(integration_id)


async def test_create_process_integration_dicts(
    client: AsyncClient, multi_step_integration_dict: dict[str, Any], registry: dict[str, Any]
) -> None:
    integration_id = await client.cw.create_integration(multi_step_integration_dict)
    assert integration_id is not None
    registry["integrations"].append(integration_id)


async def test_update_integration_dict(
    client: AsyncClient, integration_dict: dict[str, Any], registry: dict[str, Any]
) -> None:
    await client.cw.update_integration(registry["integrations"][-3], integration_dict)


async def test_update_multi_step_integration_dict(
    client: AsyncClient, registry: dict[str, Any], multi_step_integration_dict: dict[str, Any]
) -> None:
    await client.cw.update_integration(registry["integrations"][-2], multi_step_integration_dict)


async def test_update_process_integration_dict(
    client: AsyncClient,
    registry: dict[str, Any],
    process_integration_pydantic: cwm.IntegrationProcessInput,
) -> None:
    await client.cw.update_integration(registry["integrations"][-1], process_integration_pydantic)


async def test_run_integration(
    client: AsyncClient, config: PyVersionConfig, registry: dict[str, Any]
) -> None:
    run_id = await client.cw.run_integration(config.test_integration_async)
    assert run_id is not None
    registry["run_id"] = run_id


async def test_get_run_history(client: AsyncClient, registry: dict[str, Any]) -> None:
    history = await client.cw.get_run_history(registry["integrations"][-1])
    assert isinstance(history, list)
    assert all((isinstance(i, RunSummary) for i in history))


async def test_get_run_status(client: AsyncClient, registry: dict[str, Any]) -> None:
    status = await client.cw.get_run_status(registry["run_id"])
    assert isinstance(status, RunStatus)


async def test_create_schedule_pydantic(
    client: AsyncClient, registry: dict[str, Any], schedule_pydantic: cwm.ScheduleInput
) -> None:
    await client.cw.create_schedule(registry["integrations"][0], schedule_pydantic)


async def test_update_schedule_pydantic(
    client: AsyncClient, registry: dict[str, Any], schedule_pydantic: cwm.ScheduleInput
) -> None:
    await client.cw.update_schedule(registry["integrations"][0], schedule_pydantic)


async def test_set_schedule_enabled(client: AsyncClient, registry: dict[str, Any]) -> None:
    await client.cw.set_schedule_status(registry["integrations"][0], "enabled")


async def test_set_schedule_disabled(client: AsyncClient, registry: dict[str, Any]) -> None:
    await client.cw.set_schedule_status(registry["integrations"][0], "disabled")


async def test_delete_schedule(client: AsyncClient, registry: dict[str, Any]) -> None:
    await client.cw.delete_schedule(registry["integrations"][0])


async def test_create_schedule_dict(
    client: AsyncClient, registry: dict[str, Any], schedule_dict: dict[str, Any]
) -> None:
    await client.cw.create_schedule(registry["integrations"][0], schedule_dict)


async def test_update_schedule_dict(
    client: AsyncClient, registry: dict[str, Any], schedule_dict: dict[str, Any]
) -> None:
    await client.cw.update_schedule(registry["integrations"][0], schedule_dict)


async def test_update_notification_dict(
    client: AsyncClient, config: PyVersionConfig, notification_dict: dict[str, Any]
) -> None:
    notification_dict["integrationIds"] = [config.test_integration_async]
    await client.cw.update_notification_config(config.test_notification_async, notification_dict)


async def test_delete_notification(client: AsyncClient, registry: dict[str, Any]) -> None:
    await client.cw.delete_notification_config(integration_id=registry["integrations"][0])


async def test_create_notification_dict(
    client: AsyncClient, notification_dict: dict[str, Any], registry: dict[str, Any]
) -> None:
    notification_dict["integrationIds"] = [registry["integrations"][0]]
    await client.cw.create_notification_config(notification_dict)


async def test_get_run_error(client: AsyncClient, config: PyVersionConfig) -> None:
    run_error = await client.cw.get_run_error(config.error_run_id)
    assert isinstance(run_error, RunError)


async def test_delete_integration(client: AsyncClient, registry: dict[str, Any]) -> None:
    await gather(*(client.cw.delete_integration(i) for i in registry["integrations"]))


async def test_delete_connection(client: AsyncClient, registry: dict[str, Any]) -> None:
    await gather(*(client.cw.delete_connection(c) for c in registry["connections"]))
