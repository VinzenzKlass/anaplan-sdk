import asyncio
import os
from uuid import uuid4

import pytest

import anaplan_sdk
from anaplan_sdk.models import ListMetadata, ModelStatus, InsertionResult

client = anaplan_sdk.AsyncClient(
    workspace_id=os.getenv("ANAPLAN_SDK_TEST_WORKSPACE_ID"),
    model_id=os.getenv("ANAPLAN_SDK_TEST_MODEL_ID"),
    certificate=os.getenv("ANAPLAN_SDK_TEST_CERT"),
    private_key=os.getenv("ANAPLAN_SDK_TEST_PK"),
    retry_count=3,
).transactional


@pytest.fixture(scope="session")
def event_loop():
    yield asyncio.get_event_loop()


@pytest.mark.asyncio
async def test_list_workspaces():
    modules = await client.list_modules()
    assert isinstance(modules, list)
    assert len(modules) > 0


@pytest.mark.asyncio
async def test_list_lists():
    lists = await client.list_lists()
    assert isinstance(lists, list)
    assert len(lists) > 0


@pytest.mark.asyncio
async def test_list_line_items():
    items = await client.list_line_items()
    assert isinstance(items, list)
    assert len(items) > 0


@pytest.mark.asyncio
async def test_get_list_items():
    items = await client.get_list_items(101000000009)
    assert isinstance(items, list)
    assert len(items) > 0


@pytest.mark.asyncio
async def test_get_list_meta():
    meta = await client.get_list_metadata(101000000009)
    assert isinstance(meta, ListMetadata)


@pytest.mark.asyncio
async def test_get_model_status():
    status = await client.get_model_status()
    assert isinstance(status, ModelStatus)


@pytest.mark.asyncio
async def test_list_insertion():
    result = await client.add_items_to_list(
        101000000009, [{"code": str(uuid4()), "name": str(uuid4())}]
    )
    assert isinstance(result, InsertionResult)
    assert result.failures == []
    assert result.added == 1
    assert result.ignored == 0
    assert result.total == 1
