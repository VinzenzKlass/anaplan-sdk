import pytest

from anaplan_sdk import Client, models
from anaplan_sdk.exceptions import (
    AnaplanException,
    InvalidCredentialsException,
    InvalidIdentifierException,
)

test_file = 113000000074
test_action = 118000000028


def test_get_workspace(client: Client):
    workspace = client.get_workspace()
    assert isinstance(workspace, models.Workspace)
    assert workspace.id == client._workspace_id  # pyright: ignore[reportPrivateUsage]


def test_list_workspaces(client: Client):
    workspaces, search = client.get_workspaces(), client.get_workspaces("Demo")
    assert isinstance(workspaces, list)
    assert all(isinstance(workspace, models.Workspace) for workspace in workspaces)
    assert all(isinstance(workspace, models.Workspace) for workspace in search)
    assert len(workspaces) > 0
    assert len(search) > 0
    assert len(search) < len(workspaces)


def test_broken_list_files_raises_invalid_identifier_error(broken_client: Client):
    with pytest.raises(InvalidIdentifierException):
        broken_client.get_files()


def test_unauthenticated_client_raises_exception():
    with pytest.raises(InvalidCredentialsException):
        _ = Client(user_email="invalid_email", password="pass")


def test_broken_client_alm_raises(broken_client: Client):
    with pytest.raises(ValueError):
        _ = broken_client.alm


def test_broken_client_transactional_raises(broken_client: Client):
    with pytest.raises(ValueError):
        _ = broken_client.tr


def test_file_creation_raises_exception(client: Client):
    with pytest.raises(InvalidIdentifierException):
        client.upload_file(115000000000, b"")


def test_get_model(client: Client):
    model = client.get_model()
    assert isinstance(model, models.ModelWithTransactionInfo)
    assert model.id == client._model_id  # pyright: ignore[reportPrivateUsage]


def test_list_models(client: Client):
    _models, current_only, search = (
        client.get_models(),
        client.get_models(True),
        client.get_models(search_pattern="Demo"),
    )
    assert isinstance(_models, list)
    assert all(isinstance(model, models.Model) for model in _models)
    assert all(isinstance(model, models.Model) for model in current_only)
    assert all(isinstance(model, models.Model) for model in search)
    assert len(_models) > len(current_only) > len(search) > 0


def test_list_models_multi_page(client_small_pages: Client):
    _models = client_small_pages.get_models()
    assert isinstance(_models, list)
    assert len(_models) > 0
    assert all(isinstance(model, models.Model) for model in _models)
    assert len(_models) == len(set(m.id for m in _models))  # Ensure no duplicates when paginating


def test_list_actions(client: Client):
    actions = client.get_actions()
    assert isinstance(actions, list)
    assert all(isinstance(action, models.Action) for action in actions)
    assert len(actions) > 0


def test_list_files(client: Client):
    files = client.get_files()
    assert isinstance(files, list)
    assert all(isinstance(file, models.File) for file in files)
    assert len(files) > 0


def test_list_processes(client: Client):
    processes = client.get_processes()
    assert isinstance(processes, list)
    assert all(isinstance(process, models.Process) for process in processes)
    assert len(processes) > 0


def test_list_imports(client: Client):
    imports = client.get_imports()
    assert isinstance(imports, list)
    assert all(isinstance(i, models.Import) for i in imports)
    assert len(imports) > 0


def test_list_exports(client: Client):
    exports = client.get_exports()
    assert isinstance(exports, list)
    assert all(isinstance(e, models.Export) for e in exports)
    assert len(exports) > 0


def test_upload_file_stream(client: Client):
    client.upload_file_stream(test_file, (str(i) for i in range(10)))
    out = client.get_file(test_file)
    assert out == b"0123456789"


def test_upload_file_async_stream(client: Client):
    client.upload_file_stream(test_file, (i for i in _async_range(10)))
    out = client.get_file(test_file)
    assert out == b"0123456789"


def test_get_file_stream(client: Client):
    for chunk in client.get_file_stream(test_file):
        assert isinstance(chunk, bytes)


def test_upload_and_download_file(client: Client):
    client.upload_file(test_file, "Hi!")
    out = client.get_file(test_file)
    assert out == b"Hi!"


def test_run_process(client: Client):
    client.run_action(test_action)


def test_list_task_statuses(client: Client):
    task_statuses = client.get_task_summaries(test_action)
    assert isinstance(task_statuses, list)
    assert all(isinstance(status, models.TaskSummary) for status in task_statuses)
    assert len(task_statuses) > 0


def test_get_task_status(client: Client):
    task_status = client.get_task_status(test_action, (client.run_action(test_action, False)).id)
    assert isinstance(task_status, models.TaskStatus)


def test_invalid_file_id_raises_exception(client: Client):
    with pytest.raises(InvalidIdentifierException):
        client.get_file(1)


def test_run_nonexistent_action_raises_exception(client: Client):
    with pytest.raises(InvalidIdentifierException):
        client.run_action(1)


def test_upload_empty_file(client: Client):
    with pytest.raises(AnaplanException):
        client.upload_file(test_file, b"")
        # Error occurs here, since the file does not actually exist (only the "address", ID).
        client.get_file(test_file)


def test_with_model(client: Client):
    other_ws_id = other_model_id = "123"
    other_client = client.with_model(other_model_id, other_ws_id)
    assert isinstance(other_client, Client)
    assert other_client._workspace_id == other_ws_id  # pyright: ignore[reportPrivateUsage]
    assert other_client._model_id == other_model_id  # pyright: ignore[reportPrivateUsage]
    assert other_client.alm._model_id == other_model_id  # pyright: ignore[reportPrivateUsage]
    assert other_client.tr._model_id == other_model_id  # pyright: ignore[reportPrivateUsage]
    assert other_client.alm._model_id == other_model_id  # pyright: ignore[reportPrivateUsage]


def _async_range(count: int):
    for i in range(count):
        yield str(i)
