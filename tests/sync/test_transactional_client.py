from anaplan_sdk import Client
from anaplan_sdk.models import InsertionResult, ListMetadata, ModelStatus


def test_list_modules(client: Client):
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


def test_get_list_meta(client: Client):
    meta = client.transactional.get_list_metadata(101000000009)
    assert isinstance(meta, ListMetadata)


def test_get_model_status(client: Client):
    status = client.transactional.get_model_status()
    assert isinstance(status, ModelStatus)


def test_long_list_insertion(client: Client, test_list, list_items_long):
    result = client.transactional.insert_list_items(test_list, list_items_long)
    assert isinstance(result, InsertionResult)
    assert result.failures == []
    assert result.added == 200_000
    assert result.total == 200_000


def test_long_list_deletion(client: Client, test_list, list_items_long):
    result = client.transactional.delete_list_items(test_list, list_items_long)
    assert result == 200_000


def test_short_list_insertion(client: Client, test_list, list_items_short):
    result = client.transactional.insert_list_items(test_list, list_items_short)
    assert isinstance(result, InsertionResult)
    assert result.failures == []
    assert result.added == 1_000
    assert result.total == 1_000


def test_get_list_items(client: Client, test_list):
    items = client.transactional.get_list_items(test_list)
    assert isinstance(items, list)
    assert len(items) == 1_000


def test_short_list_deletion(client: Client, test_list, list_items_short):
    result = client.transactional.delete_list_items(test_list, list_items_short)
    assert result == 1_000


def test_reset_list_index(client: Client, test_list):
    client.transactional.reset_list_index(test_list)
