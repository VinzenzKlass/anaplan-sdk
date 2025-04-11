from anaplan_sdk import Client
from anaplan_sdk.exceptions import InvalidIdentifierException


def test_list_workspaces(client: Client):
    workspaces = client.list_workspaces()
    assert isinstance(workspaces, list)
    assert len(workspaces) > 0


def test_broken_list_workspaces_raises_invalid_identifier_error(broken_client: Client):
    try:
        broken_client.list_workspaces()
    except Exception as error:
        assert isinstance(error, InvalidIdentifierException)


def test_list_models(client: Client):
    models = client.list_models()
    assert isinstance(models, list)
    assert len(models) > 0


def test_list_actions(client: Client):
    actions = client.list_actions()
    assert isinstance(actions, list)
    assert len(actions) > 0


def test_list_files(client: Client):
    files = client.list_files()
    assert isinstance(files, list)
    assert len(files) > 0


def test_list_processes(client: Client):
    processes = client.list_processes()
    assert isinstance(processes, list)
    assert len(processes) > 0


def test_list_imports(client: Client):
    imports = client.list_imports()
    assert isinstance(imports, list)
    assert len(imports) > 0


def test_list_exports(client: Client):
    exports = client.list_exports()
    assert isinstance(exports, list)
    assert len(exports) > 0


def test_upload_file_stream(client: Client, test_file):
    client.upload_file_stream(test_file, (str(i) for i in range(10)))
    out = client.get_file(test_file)
    assert out == b"0123456789"


def test_get_file_stream(client: Client, test_file):
    for chunk in client.get_file_stream(test_file):
        assert isinstance(chunk, bytes)


def test_upload_and_download_file(client: Client, test_file):
    client.upload_file(test_file, "Hi!")
    out = client.get_file(test_file)
    assert out == b"Hi!"


def test_run_process(client: Client, test_action):
    client.run_action(test_action)


def test_invoke_action(client: Client, test_action):
    task_id = client.invoke_action(test_action)
    assert isinstance(task_id, str)
    assert len(task_id) == 32


def test_get_task_status(client: Client, test_action):
    task_status = client.get_task_status(test_action, client.invoke_action(test_action))
    assert isinstance(task_status, dict)
    assert "progress" in task_status
    assert "creationTime" in task_status
    assert "taskState" in task_status
