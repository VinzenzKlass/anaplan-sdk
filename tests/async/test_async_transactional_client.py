from calendar import monthrange
from datetime import date

from anaplan_sdk import AsyncClient
from anaplan_sdk.models import CurrentPeriod, FiscalYear, InsertionResult, ListMetadata, ModelStatus


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
    assert result.failures == []
    assert result.added == 200_000
    assert result.total == 200_000


async def test_long_list_deletion(client: AsyncClient, test_list, list_items_long):
    result = await client.transactional.delete_list_items(test_list, list_items_long)
    assert result == 200_000


async def test_short_list_insertion(client: AsyncClient, test_list, list_items_short):
    result = await client.transactional.insert_list_items(test_list, list_items_short)
    assert isinstance(result, InsertionResult)
    assert result.failures == []
    assert result.added == 1_000
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


async def test_get_current_period(client: AsyncClient):
    period = await client.transactional.get_current_period()
    assert isinstance(period, CurrentPeriod)


async def test_set_current_period(client: AsyncClient):
    today = date.today()
    last_day_of_month = date(today.year, today.month, monthrange(today.year, today.month)[1])
    period = await client.transactional.set_current_period(today.strftime("%Y-%m-%d"))
    assert isinstance(period, CurrentPeriod)
    assert period.last_day == last_day_of_month.strftime("%Y-%m-%d")


async def test_set_current_fiscal_year(client: AsyncClient):
    year = "FY25"
    fiscal_year = await client.transactional.set_current_fiscal_year(year)
    assert isinstance(fiscal_year, FiscalYear)
    assert fiscal_year.year == year
