from calendar import monthrange
from datetime import date
from os import getenv

from anaplan_sdk import AsyncClient
from anaplan_sdk.models import (
    CurrentPeriod,
    FiscalYear,
    InsertionResult,
    ListMetadata,
    Model,
    ModelStatus,
    MonthsQuartersYearsCalendar,
    View,
    ViewInfo,
)


async def test_wake_model(client: AsyncClient):
    await client.transactional.wake_model()


async def test_close_model(client: AsyncClient):
    other = AsyncClient.from_existing(client, model_id="C87EBE934BD442B1A798540E0CA5A877")
    await other.transactional.close_model()


async def test_get_model(client: AsyncClient):
    model_id = getenv("ANAPLAN_SDK_TEST_MODEL_ID")
    model = await client.transactional.get_model_details()
    assert isinstance(model, Model)
    assert model.id == model_id


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


async def test_list_views(client: AsyncClient):
    views = await client.transactional.list_views()
    assert isinstance(views, list)
    assert len(views) > 0
    assert all(isinstance(view, View) for view in views)


async def test_get_view_info(client: AsyncClient):
    info = await client.transactional.get_view_info(102000000015)
    assert isinstance(info, ViewInfo)


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


async def test_get_model_calendar(client: AsyncClient):
    calendar = await client.transactional.get_model_calendar()
    assert isinstance(calendar, MonthsQuartersYearsCalendar)
