from asyncio import gather

import pytest

from anaplan_sdk import AsyncClient
from anaplan_sdk.exceptions import (
    AnaplanException,
    InvalidCredentialsException,
    InvalidIdentifierException,
)
from anaplan_sdk.models import Model, TaskStatus, TaskSummary, Workspace


async def test_get_workspace(client: AsyncClient):
    workspace = await client.get_workspace()
    assert isinstance(workspace, Workspace)
    assert workspace.id == client._workspace_id


async def test_list_workspaces(client: AsyncClient):
    workspaces, search = await gather(client.get_workspaces(), client.get_workspaces("Demo"))
    assert isinstance(workspaces, list)
    assert all(isinstance(workspace, Workspace) for workspace in workspaces)
    assert all(isinstance(workspace, Workspace) for workspace in search)
    assert len(workspaces) > 0
    assert len(search) > 0
    assert len(search) < len(workspaces)


async def test_broken_list_files_raises_invalid_identifier_error(broken_client):
    with pytest.raises(InvalidIdentifierException):
        await broken_client.get_files()


async def test_unauthenticated_client_raises_exception():
    with pytest.raises(InvalidCredentialsException):
        _ = AsyncClient(user_email="invalid_email", password="pass")


def test_broken_client_alm_raises(broken_client: AsyncClient):
    with pytest.raises(ValueError):
        _ = broken_client.alm


def test_broken_client_transactional_raises(broken_client: AsyncClient):
    with pytest.raises(ValueError):
        _ = broken_client.tr


async def test_file_creation_raises_exception(client: AsyncClient):
    with pytest.raises(InvalidIdentifierException):
        await client.upload_file(115000000000, b"")


async def test_get_model(client: AsyncClient):
    model = await client.get_model()
    assert isinstance(model, Model)
    assert model.id == client._model_id


async def test_list_models(client: AsyncClient):
    models, current_only, search = await gather(
        client.get_models(), client.get_models(True), client.get_models(search_pattern="Demo")
    )
    assert isinstance(models, list)
    assert all(isinstance(model, Model) for model in models)
    assert all(isinstance(model, Model) for model in current_only)
    assert all(isinstance(model, Model) for model in search)
    assert len(models) > len(current_only) > len(search) > 0


async def test_list_models_multi_page(client_small_pages: AsyncClient):
    models = await client_small_pages.get_models()
    assert isinstance(models, list)
    assert len(models) > 0
    assert all(isinstance(model, Model) for model in models)
    assert len(models) == len(set(m.id for m in models))  # Ensure no duplicates when paginating


async def test_list_actions(client: AsyncClient):
    actions = await client.get_actions()
    assert isinstance(actions, list)
    assert len(actions) > 0


async def test_list_files(client: AsyncClient):
    files = await client.get_files()
    assert isinstance(files, list)
    assert len(files) > 0


async def test_list_processes(client: AsyncClient):
    processes = await client.get_processes()
    assert isinstance(processes, list)
    assert len(processes) > 0


async def test_list_imports(client: AsyncClient):
    imports = await client.get_imports()
    assert isinstance(imports, list)
    assert len(imports) > 0


async def test_list_exports(client: AsyncClient):
    exports = await client.get_exports()
    assert isinstance(exports, list)
    assert len(exports) > 0


async def test_upload_file_stream(client: AsyncClient, test_file):
    await client.upload_file_stream(test_file, (str(i) for i in range(10)))
    out = await client.get_file(test_file)
    assert out == b"0123456789"


async def test_upload_file_async_stream(client: AsyncClient, test_file):
    await client.upload_file_stream(test_file, (i async for i in _async_range(10)))
    out = await client.get_file(test_file)
    assert out == b"0123456789"


async def test_get_file_stream(client: AsyncClient, test_file):
    async for chunk in client.get_file_stream(test_file):
        assert isinstance(chunk, bytes)


async def test_upload_and_download_file(client: AsyncClient, test_file):
    await client.upload_file(test_file, "Hi!")
    out = await client.get_file(test_file)
    assert out == b"Hi!"


async def test_run_process(client: AsyncClient, test_action):
    await client.run_action(test_action)


async def test_list_task_statuses(client: AsyncClient, test_action):
    task_statuses = await client.get_task_summaries(test_action)
    assert isinstance(task_statuses, list)
    assert all(isinstance(status, TaskSummary) for status in task_statuses)
    assert len(task_statuses) > 0


async def test_get_task_status(client: AsyncClient, test_action):
    task_status = await client.get_task_status(
        test_action, (await client.run_action(test_action, False)).id
    )
    assert isinstance(task_status, TaskStatus)


async def test_invalid_file_id_raises_exception(client: AsyncClient):
    with pytest.raises(InvalidIdentifierException):
        await client.get_file(1)


async def test_run_nonexistent_action_raises_exception(client: AsyncClient):
    with pytest.raises(InvalidIdentifierException):
        await client.run_action(1)


async def test_upload_empty_file(client: AsyncClient, test_file):
    with pytest.raises(AnaplanException):
        await client.upload_file(test_file, b"")
        # Error occurs here, since the file does not actually exist
        await client.get_file(test_file)


async def test_with_model(client: AsyncClient):
    other_ws_id = other_model_id = "123"
    other_client = client.with_model(other_model_id, other_ws_id)
    assert isinstance(other_client, AsyncClient)
    assert other_client._workspace_id == other_ws_id
    assert other_client._model_id == other_model_id
    assert other_client.alm._model_id == other_model_id
    assert other_client.tr._model_id == other_model_id
    assert other_client.alm._model_id == other_model_id


async def _async_range(count: int):
    for i in range(count):
        yield str(i)
