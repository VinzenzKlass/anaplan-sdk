from uuid import uuid4

from anaplan_sdk import AsyncClient
from anaplan_sdk.models import InsertionResult, ListMetadata, ModelStatus


async def test_list_workspaces(client: AsyncClient):
    modules = await client.transactional.list_modules()
    assert isinstance(modules, list)
    assert len(modules) > 0


async def test_list_lists(client: AsyncClient):
    lists = await client.transactional.list_lists()
    assert isinstance(lists, list)
    assert len(lists) > 0


async def test_list_line_items(client: AsyncClient):
    items = await client.transactional.list_line_items()
    assert isinstance(items, list)
    assert len(items) > 0


async def test_get_list_items(client: AsyncClient):
    items = await client.transactional.get_list_items(101000000009)
    assert isinstance(items, list)


async def test_get_list_meta(client: AsyncClient):
    meta = await client.transactional.get_list_metadata(101000000009)
    assert isinstance(meta, ListMetadata)


async def test_get_model_status(client: AsyncClient):
    status = await client.transactional.get_model_status()
    assert isinstance(status, ModelStatus)


async def test_list_insertion(client: AsyncClient):
    result = await client.transactional.add_items_to_list(
        101000000009, [{"code": str(uuid4()), "name": str(uuid4())}]
    )
    assert isinstance(result, InsertionResult)
    assert result.failures == []
    assert result.added == 1
    assert result.ignored == 0
    assert result.total == 1


async def test_delete_list_items(client: AsyncClient):
    code = str(uuid4())
    await client.transactional.add_items_to_list(
        101000000009, [{"code": code, "name": str(uuid4())}]
    )
    await client.transactional.delete_list_items(101000000009, [{"code": code}])


async def test_reset_list_index(client: AsyncClient):
    await client.transactional.reset_list_index(101000000010)
