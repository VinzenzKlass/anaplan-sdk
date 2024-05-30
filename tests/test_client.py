import os
import sys

import anaplan_sdk
from anaplan_sdk import InvalidIdentifierException

client = anaplan_sdk.Client(
    workspace_id=os.getenv("ANAPLAN_SDK_TEST_WORKSPACE_ID"),
    model_id=os.getenv("ANAPLAN_SDK_TEST_MODEL_ID"),
    certificate=os.getenv("ANAPLAN_SDK_TEST_CERT"),
    private_key=os.getenv("ANAPLAN_SDK_TEST_PK"),
    retry_count=3,
)

broken_client = anaplan_sdk.Client(
    workspace_id="random",
    model_id="nonsense",
    certificate=os.getenv("ANAPLAN_SDK_TEST_CERT"),
    private_key=os.getenv("ANAPLAN_SDK_TEST_PK"),
    retry_count=1,
)

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


def test_unauthorized_client_raises_value_error():
    try:
        anaplan_sdk.Client()
    except Exception as error:
        assert isinstance(error, ValueError)


def test_list_workspaces():
    workspaces = client.list_workspaces()
    assert isinstance(workspaces, list)
    assert len(workspaces) > 0


def test_broken_list_workspaces_raises_invalid_identifier_error():
    try:
        broken_client.list_workspaces()
    except Exception as error:
        assert isinstance(error, InvalidIdentifierException)


def test_list_models():
    models = client.list_models()
    assert isinstance(models, list)
    assert len(models) > 0


def test_list_actions():
    actions = client.list_actions()
    assert isinstance(actions, list)
    assert len(actions) > 0


def test_list_files():
    files = client.list_files()
    assert isinstance(files, list)
    assert len(files) > 0


def test_list_lists():
    lists = client.list_lists()
    assert isinstance(lists, list)
    assert len(lists) > 0


def test_list_processes():
    processes = client.list_processes()
    assert isinstance(processes, list)
    assert len(processes) > 0


def test_list_imports():
    imports = client.list_imports()
    assert isinstance(imports, list)
    assert len(imports) > 0


def test_list_exports():
    exports = client.list_exports()
    assert isinstance(exports, list)
    assert len(exports) > 0


def test_upload_and_download_file():
    client.upload_file(113000000000, "Hi!")
    out = client.get_file(113000000000)
    assert out == b"Hi!"


def test_run_process():
    client.run_action(118000000004)


def test_invoke_action():
    task_id = client.invoke_action(118000000004)
    assert isinstance(task_id, str)
    assert len(task_id) == 32


def test_get_task_status():
    task_status = client.get_task_status(118000000004, client.invoke_action(118000000004))
    assert isinstance(task_status, dict)
    assert "currentStep" in task_status
    assert "successful" in task_status.get("result")
    assert "nestedResults" in task_status.get("result")
