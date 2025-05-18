from asyncio import gather

import pytest

from anaplan_sdk import AsyncClient
from anaplan_sdk.exceptions import (
    AnaplanException,
    InvalidCredentialsException,
    InvalidIdentifierException,
)
from anaplan_sdk.models import Model, TaskStatus, Workspace


async def test_list_workspaces(client: AsyncClient):
    workspaces, search = await gather(client.list_workspaces(), client.list_workspaces("Demo"))
    assert isinstance(workspaces, list)
    assert all(isinstance(workspace, Workspace) for workspace in workspaces)
    assert all(isinstance(workspace, Workspace) for workspace in search)
    assert len(workspaces) > 0
    assert len(search) > 0
    assert len(search) < len(workspaces)


async def test_broken_list_files_raises_invalid_identifier_error(broken_client):
    with pytest.raises(InvalidIdentifierException):
        await broken_client.list_files()


async def unauthenticated_client_raises_exception():
    with pytest.raises(InvalidCredentialsException):
        _ = AsyncClient(user_email="invalid_email", password="pass")


async def test_list_models(client: AsyncClient):
    models, search = await gather(client.list_models(), client.list_models("Demo"))
    assert isinstance(models, list)
    assert all(isinstance(model, Model) for model in models)
    assert all(isinstance(model, Model) for model in search)
    assert len(models) > 0
    assert len(search) > 0
    assert len(search) < len(models)


async def test_list_actions(client: AsyncClient):
    actions = await client.list_actions()
    assert isinstance(actions, list)
    assert len(actions) > 0


async def test_list_files(client: AsyncClient):
    files = await client.list_files()
    assert isinstance(files, list)
    assert len(files) > 0


async def test_list_processes(client: AsyncClient):
    processes = await client.list_processes()
    assert isinstance(processes, list)
    assert len(processes) > 0


async def test_list_imports(client: AsyncClient):
    imports = await client.list_imports()
    assert isinstance(imports, list)
    assert len(imports) > 0


async def test_list_exports(client: AsyncClient):
    exports = await client.list_exports()
    assert isinstance(exports, list)
    assert len(exports) > 0


async def test_upload_file_stream(client, test_file):
    await client.upload_file_stream(test_file, (i async for i in _async_range(10)))
    out = await client.get_file(test_file)
    assert out == b"0123456789"


async def test_get_file_stream(client, test_file):
    async for chunk in client.get_file_stream(test_file):
        assert isinstance(chunk, bytes)


async def test_upload_and_download_file(client, test_file):
    await client.upload_file(test_file, "Hi!")
    out = await client.get_file(test_file)
    assert out == b"Hi!"


async def test_run_process(client, test_action):
    await client.run_action(test_action)


async def test_invoke_action(client, test_action):
    task_id = await client.invoke_action(test_action)
    assert isinstance(task_id, str)
    assert len(task_id) == 32


async def test_get_task_status(client, test_action):
    task_status = await client.get_task_status(test_action, await client.invoke_action(test_action))
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
        result = await client.get_file(
            test_file
        )  # Error occurs here, since the file does not actually exist
        assert result == b""


async def _async_range(count: int):
    for i in range(count):
        yield str(i)
