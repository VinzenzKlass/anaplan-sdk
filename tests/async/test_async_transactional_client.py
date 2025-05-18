from anaplan_sdk import AsyncClient
from anaplan_sdk.models import InsertionResult, ListMetadata, ModelStatus


async def test_list_modules(client: AsyncClient):
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


async def test_get_list_meta(client: AsyncClient, test_list):
    meta = await client.transactional.get_list_metadata(test_list)
    assert isinstance(meta, ListMetadata)


async def test_get_model_status(client: AsyncClient):
    status = await client.transactional.get_model_status()
    assert isinstance(status, ModelStatus)


async def test_long_list_insertion(client: AsyncClient, test_list, list_items_long):
    result = await client.transactional.insert_list_items(test_list, list_items_long)
    assert isinstance(result, InsertionResult)
    assert result.total == 200_000


async def test_long_list_deletion(client: AsyncClient, test_list, list_items_long):
    result = await client.transactional.delete_list_items(test_list, list_items_long)
    assert result == 200_000


async def test_short_list_insertion(client: AsyncClient, test_list, list_items_short):
    result = await client.transactional.insert_list_items(test_list, list_items_short)
    assert isinstance(result, InsertionResult)
    assert result.total == 1_000


async def test_get_list_items(client: AsyncClient, test_list):
    items = await client.transactional.get_list_items(test_list)
    assert isinstance(items, list)
    assert len(items) == 1_000


async def test_short_list_deletion(client: AsyncClient, test_list, list_items_short):
    result = await client.transactional.delete_list_items(test_list, list_items_short)
    assert result == 1_000


async def test_reset_list_index(client: AsyncClient, test_list):
    await client.transactional.reset_list_index(test_list)
