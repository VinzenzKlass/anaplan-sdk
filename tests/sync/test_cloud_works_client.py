from concurrent.futures.thread import ThreadPoolExecutor
from typing import Any, Callable

import anaplan_sdk.models.cloud_works as cwm
from anaplan_sdk import Client
from anaplan_sdk.models.cloud_works import Connection, Integration, RunError, RunStatus, RunSummary
from tests.conftest import PyVersionConfig


def test_list_connections(client: Client) -> None:
    connections = client.cw.get_connections()
    assert isinstance(connections, list)
    assert all(isinstance(c, Connection) for c in connections)


def test_create_connection_pydantic(
    client: Client, az_blob_connection: cwm.ConnectionInput, registry: dict[str, Any]
) -> None:
    con_id = client.cw.create_connection(az_blob_connection)
    assert con_id is not None
    registry["connections"].append(con_id)


def test_create_connection_dict(
    client: Client, az_blob_connection_dict: dict[str, Any], registry: dict[str, Any]
) -> None:
    con_id = client.cw.create_connection(az_blob_connection_dict)
    assert con_id is not None
    registry["connections"].append(con_id)


def test_update_connection_pydantic(
    client: Client, az_blob_connection: cwm.ConnectionInput, registry: dict[str, Any]
) -> None:
    client.cw.update_connection(registry["connections"][0], az_blob_connection.body)


def test_update_connection_dict(
    client: Client, az_blob_connection_dict: dict[str, Any], registry: dict[str, Any]
) -> None:
    client.cw.update_connection(registry["connections"][-1], az_blob_connection_dict["body"])


def test_patch_connection(client: Client, name: str, registry: dict[str, Any]) -> None:
    client.cw.patch_connection(registry["connections"][-1], {"name": name})


def test_get_integration(
    client: Client,
    test_integration_ids: list[str],
    integration_validator: Callable[[list[cwm.SingleIntegration]], None],
) -> None:
    with ThreadPoolExecutor() as executor:
        integrations = list(executor.map(client.cw.get_integration, test_integration_ids))
    integration_validator(integrations)


def test_list_integrations(client: Client) -> None:
    integrations_asc = client.cw.get_integrations()
    assert isinstance(integrations_asc, list)
    assert all(isinstance(i, Integration) for i in integrations_asc)


def test_list_integrations_desc(client: Client) -> None:
    integrations_desc = client.cw.get_integrations(sort_by="name", descending=True)
    assert isinstance(integrations_desc, list)
    assert all(isinstance(i, Integration) for i in integrations_desc)


def test_create_integration_pydantic(
    client: Client, integration_pydantic: cwm.IntegrationInput, registry: dict[str, Any]
) -> None:
    integration_id = client.cw.create_integration(integration_pydantic)
    assert integration_id is not None
    registry["integrations"].append(integration_id)


def test_create_multi_step_integration_pydantic(
    client: Client, multi_step_integration_pydantic: cwm.IntegrationInput, registry: dict[str, Any]
) -> None:
    integration_id = client.cw.create_integration(multi_step_integration_pydantic)
    assert integration_id is not None
    registry["integrations"].append(integration_id)


def test_create_process_integration_pydantic(
    client: Client,
    process_integration_pydantic: cwm.IntegrationProcessInput,
    registry: dict[str, Any],
) -> None:
    integration_id = client.cw.create_integration(process_integration_pydantic)
    assert integration_id is not None
    registry["integrations"].append(integration_id)


def test_update_integration_pydantic(
    client: Client, integration_pydantic: cwm.IntegrationInput, registry: dict[str, Any]
) -> None:
    client.cw.update_integration(registry["integrations"][0], integration_pydantic)


def test_update_multi_step_integration_pydantic(
    client: Client, registry: dict[str, Any], multi_step_integration_pydantic: cwm.IntegrationInput
) -> None:
    client.cw.update_integration(registry["integrations"][1], multi_step_integration_pydantic)


def test_update_process_integration_pydantic(
    client: Client,
    registry: dict[str, Any],
    process_integration_pydantic: cwm.IntegrationProcessInput,
) -> None:
    client.cw.update_integration(registry["integrations"][-1], process_integration_pydantic)


def test_create_integration_dict(
    client: Client, integration_dict: dict[str, Any], registry: dict[str, Any]
) -> None:
    integration_id = client.cw.create_integration(integration_dict)
    assert integration_id is not None
    registry["integrations"].append(integration_id)


def test_create_multi_step_integration_dicts(
    client: Client, multi_step_integration_dict: dict[str, Any], registry: dict[str, Any]
) -> None:
    integration_id = client.cw.create_integration(multi_step_integration_dict)
    assert integration_id is not None
    registry["integrations"].append(integration_id)


def test_create_process_integration_dicts(
    client: Client, multi_step_integration_dict: dict[str, Any], registry: dict[str, Any]
) -> None:
    integration_id = client.cw.create_integration(multi_step_integration_dict)
    assert integration_id is not None
    registry["integrations"].append(integration_id)


def test_update_integration_dict(
    client: Client, integration_dict: dict[str, Any], registry: dict[str, Any]
) -> None:
    client.cw.update_integration(registry["integrations"][-3], integration_dict)


def test_update_multi_step_integration_dict(
    client: Client, registry: dict[str, Any], multi_step_integration_dict: dict[str, Any]
) -> None:
    client.cw.update_integration(registry["integrations"][-2], multi_step_integration_dict)


def test_update_process_integration_dict(
    client: Client,
    registry: dict[str, Any],
    process_integration_pydantic: cwm.IntegrationProcessInput,
) -> None:
    client.cw.update_integration(registry["integrations"][-1], process_integration_pydantic)


def test_run_integration(client: Client, config: PyVersionConfig, registry: dict[str, Any]) -> None:
    run_id = client.cw.run_integration(config.test_integration_sync)
    assert run_id is not None
    registry["run_id"] = run_id


def test_get_run_history(client: Client, registry: dict[str, Any]) -> None:
    history = client.cw.get_run_history(registry["integrations"][-1])
    assert isinstance(history, list)
    assert all((isinstance(i, RunSummary) for i in history))


def test_get_run_status(client: Client, registry: dict[str, Any]) -> None:
    status = client.cw.get_run_status(registry["run_id"])
    assert isinstance(status, RunStatus)


def test_create_schedule_pydantic(
    client: Client, registry: dict[str, Any], schedule_pydantic: cwm.ScheduleInput
) -> None:
    client.cw.create_schedule(registry["integrations"][0], schedule_pydantic)


def test_update_schedule_pydantic(
    client: Client, registry: dict[str, Any], schedule_pydantic: cwm.ScheduleInput
) -> None:
    client.cw.update_schedule(registry["integrations"][0], schedule_pydantic)


def test_set_schedule_enabled(client: Client, registry: dict[str, Any]) -> None:
    client.cw.set_schedule_status(registry["integrations"][0], "enabled")


def test_set_schedule_disabled(client: Client, registry: dict[str, Any]) -> None:
    client.cw.set_schedule_status(registry["integrations"][0], "disabled")


def test_delete_schedule(client: Client, registry: dict[str, Any]) -> None:
    client.cw.delete_schedule(registry["integrations"][0])


def test_create_schedule_dict(
    client: Client, registry: dict[str, Any], schedule_dict: dict[str, Any]
) -> None:
    client.cw.create_schedule(registry["integrations"][0], schedule_dict)


def test_update_schedule_dict(
    client: Client, registry: dict[str, Any], schedule_dict: dict[str, Any]
) -> None:
    client.cw.update_schedule(registry["integrations"][0], schedule_dict)


def test_update_notification_dict(
    client: Client, config: PyVersionConfig, notification_dict: dict[str, Any]
) -> None:
    notification_dict["integrationIds"] = [config.test_integration_sync]
    client.cw.update_notification_config(config.test_notification_sync, notification_dict)


def test_delete_notification(client: Client, registry: dict[str, Any]) -> None:
    client.cw.delete_notification_config(integration_id=registry["integrations"][0])


def test_create_notification_dict(
    client: Client, notification_dict: dict[str, Any], registry: dict[str, Any]
) -> None:
    notification_dict["integrationIds"] = [registry["integrations"][0]]
    client.cw.create_notification_config(notification_dict)


def test_get_run_error(client: Client, config: PyVersionConfig) -> None:
    run_error = client.cw.get_run_error(config.error_run_id)
    assert isinstance(run_error, RunError)


def test_delete_integration(client: Client, registry: dict[str, Any]) -> None:
    _ = (client.cw.delete_integration(i) for i in registry["integrations"])


def test_delete_connection(client: Client, registry: dict[str, Any]) -> None:
    _ = (client.cw.delete_connection(c) for c in registry["connections"])
