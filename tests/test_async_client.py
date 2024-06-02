import asyncio
import os
import sys

import pytest

import anaplan_sdk
from anaplan_sdk import InvalidIdentifierException

client = anaplan_sdk.AsyncClient(
    workspace_id=os.getenv("ANAPLAN_SDK_TEST_WORKSPACE_ID"),
    model_id=os.getenv("ANAPLAN_SDK_TEST_MODEL_ID"),
    certificate=os.getenv("ANAPLAN_SDK_TEST_CERT"),
    private_key=os.getenv("ANAPLAN_SDK_TEST_PK"),
    retry_count=3,
)

broken_client = anaplan_sdk.AsyncClient(
    workspace_id="random",
    model_id="nonsense",
    certificate=os.getenv("ANAPLAN_SDK_TEST_CERT"),
    private_key=os.getenv("ANAPLAN_SDK_TEST_PK"),
    retry_count=1,
)


pytest_plugins = ("pytest_asyncio",)

py_version = sys.version.split(" ")[0]
if "3.12" in py_version:
    test_file = 113000000031
    test_action = 118000000007

elif "3.11" in py_version:
    test_file = 113000000030
    test_action = 118000000008
else:
    test_file = 113000000029
    test_action = 118000000006


@pytest.fixture(scope="session")
def event_loop():
    yield asyncio.get_event_loop()


def test_unauthorized_client_raises_value_error():
    try:
        anaplan_sdk.Client()
    except Exception as error:
        assert isinstance(error, ValueError)


@pytest.mark.asyncio
async def test_list_workspaces():
    workspaces = await client.list_workspaces()
    assert isinstance(workspaces, list)
    assert len(workspaces) > 0


@pytest.mark.asyncio
async def test_broken_list_workspaces_raises_invalid_identifier_error():
    try:
        await broken_client.list_workspaces()
    except Exception as error:
        assert isinstance(error, InvalidIdentifierException)


@pytest.mark.asyncio
async def test_list_models():
    models = await client.list_models()
    assert isinstance(models, list)
    assert len(models) > 0


@pytest.mark.asyncio
async def test_list_actions():
    actions = await client.list_actions()
    assert isinstance(actions, list)
    assert len(actions) > 0


@pytest.mark.asyncio
async def test_list_files():
    files = await client.list_files()
    assert isinstance(files, list)
    assert len(files) > 0


@pytest.mark.asyncio
async def test_list_processes():
    processes = await client.list_processes()
    assert isinstance(processes, list)
    assert len(processes) > 0


@pytest.mark.asyncio
async def test_list_imports():
    imports = await client.list_imports()
    assert isinstance(imports, list)
    assert len(imports) > 0


@pytest.mark.asyncio
async def test_list_exports():
    exports = await client.list_exports()
    assert isinstance(exports, list)
    assert len(exports) > 0


@pytest.mark.asyncio
async def test_upload_and_download_file():
    await client.upload_file(113000000000, "Hi!")
    out = await client.get_file(113000000000)
    assert out == b"Hi!"


@pytest.mark.asyncio
async def test_run_process():
    await client.run_action(118000000004)


@pytest.mark.asyncio
async def test_invoke_action():
    task_id = await client.invoke_action(118000000004)
    assert isinstance(task_id, str)
    assert len(task_id) == 32


@pytest.mark.asyncio
async def test_get_task_status():
    task_status = await client.get_task_status(
        118000000004, await client.invoke_action(118000000004)
    )
    assert isinstance(task_status, dict)
    assert "currentStep" in task_status
    assert "successful" in task_status.get("result")
    assert "nestedResults" in task_status.get("result")
