import os
from uuid import uuid4

import anaplan_sdk
from anaplan_sdk.models import InsertionResult, ListMetadata, ModelStatus

client = anaplan_sdk.Client(
    workspace_id=os.getenv("ANAPLAN_SDK_TEST_WORKSPACE_ID"),
    model_id=os.getenv("ANAPLAN_SDK_TEST_MODEL_ID"),
    certificate=os.getenv("ANAPLAN_SDK_TEST_CERT"),
    private_key=os.getenv("ANAPLAN_SDK_TEST_PK"),
    retry_count=3,
).transactional


def test_list_workspaces():
    modules = client.list_modules()
    assert isinstance(modules, list)
    assert len(modules) > 0


def test_list_lists():
    lists = client.list_lists()
    assert isinstance(lists, list)
    assert len(lists) > 0


def test_list_line_items():
    items = client.list_line_items()
    assert isinstance(items, list)
    assert len(items) > 0


def test_get_list_items():
    items = client.get_list_items(101000000009)
    assert isinstance(items, list)


def test_get_list_meta():
    meta = client.get_list_metadata(101000000009)
    assert isinstance(meta, ListMetadata)


def test_get_model_status():
    status = client.get_model_status()
    assert isinstance(status, ModelStatus)


def test_list_insertion():
    result = client.add_items_to_list(101000000009, [{"code": str(uuid4()), "name": str(uuid4())}])
    assert isinstance(result, InsertionResult)
    assert result.failures == []
    assert result.added == 1
    assert result.ignored == 0
    assert result.total == 1


def test_delete_list_items():
    code = str(uuid4())
    client.add_items_to_list(101000000009, [{"code": code, "name": str(uuid4())}])
    client.delete_list_items(101000000009, [{"code": code}])


def test_reset_list_index():
    client.reset_list_index(101000000010)
