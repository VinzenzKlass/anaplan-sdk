from uuid import uuid4

from anaplan_sdk import Client
from anaplan_sdk.models import InsertionResult, ListMetadata, ModelStatus


def test_list_workspaces(client: Client):
    modules = client.transactional.list_modules()
    assert isinstance(modules, list)
    assert len(modules) > 0


def test_list_lists(client: Client):
    lists = client.transactional.list_lists()
    assert isinstance(lists, list)
    assert len(lists) > 0


def test_list_line_items(client: Client):
    items = client.transactional.list_line_items()
    assert isinstance(items, list)
    assert len(items) > 0


def test_get_list_items(client: Client):
    items = client.transactional.get_list_items(101000000009)
    assert isinstance(items, list)


def test_get_list_meta(client: Client):
    meta = client.transactional.get_list_metadata(101000000009)
    assert isinstance(meta, ListMetadata)


def test_get_model_status(client: Client):
    status = client.transactional.get_model_status()
    assert isinstance(status, ModelStatus)


def test_list_insertion(client: Client):
    result = client.transactional.add_items_to_list(
        101000000009, [{"code": str(uuid4()), "name": str(uuid4())}]
    )
    assert isinstance(result, InsertionResult)
    assert result.failures == []
    assert result.added == 1
    assert result.ignored == 0
    assert result.total == 1


def test_delete_list_items(client: Client):
    code = str(uuid4())
    client.transactional.add_items_to_list(101000000009, [{"code": code, "name": str(uuid4())}])
    client.transactional.delete_list_items(101000000009, [{"code": code}])


def test_reset_list_index(client: Client):
    client.transactional.reset_list_index(101000000010)
