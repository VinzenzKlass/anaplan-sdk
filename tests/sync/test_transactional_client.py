from calendar import monthrange
from datetime import date
from os import getenv

from anaplan_sdk import Client
from anaplan_sdk.models import (
    CurrentPeriod,
    Dimension,
    DimensionWithCode,
    FiscalYear,
    InsertionResult,
    ListMetadata,
    Model,
    ModelStatus,
    MonthsQuartersYearsCalendar,
    View,
    ViewInfo,
)


def test_wake_model(client: Client):
    client.transactional.wake_model()


def test_close_model(client: Client):
    other = Client.from_existing(client, model_id="C87EBE934BD442B1A798540E0CA5A877")
    other.transactional.close_model()


def test_get_model(client: Client):
    model_id = getenv("ANAPLAN_SDK_TEST_MODEL_ID")
    model = client.transactional.get_model_details()
    assert isinstance(model, Model)
    assert model.id == model_id


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


def test_get_list_meta(client: Client, test_list):
    meta = client.transactional.get_list_metadata(test_list)
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


def test_list_views(client: Client):
    views = client.transactional.list_views()
    assert isinstance(views, list)
    assert len(views) > 0
    assert all(isinstance(view, View) for view in views)


def test_get_view_info(client: Client):
    info = client.transactional.get_view_info(102000000015)
    assert isinstance(info, ViewInfo)


def test_get_current_period(client: Client):
    period = client.transactional.get_current_period()
    assert isinstance(period, CurrentPeriod)


def test_set_current_period(client: Client):
    today = date.today()
    last_day_of_month = date(today.year, today.month, monthrange(today.year, today.month)[1])
    period = client.transactional.set_current_period(today.strftime("%Y-%m-%d"))
    assert isinstance(period, CurrentPeriod)
    assert period.last_day == last_day_of_month.strftime("%Y-%m-%d")


def test_set_current_fiscal_year(client: Client):
    year = "FY25"
    fiscal_year = client.transactional.set_current_fiscal_year(year)
    assert isinstance(fiscal_year, FiscalYear)
    assert fiscal_year.year == year


def test_get_model_calendar(client: Client):
    calendar = client.transactional.get_model_calendar()
    assert isinstance(calendar, MonthsQuartersYearsCalendar)


def test_get_dimension_items(client: Client):
    items = client.transactional.get_dimension_items(109000000000)
    assert isinstance(items, list)
    assert all(isinstance(item, DimensionWithCode) for item in items)


def test_get_dimension_items_with_list_warns(client: Client, caplog):
    items = client.transactional.get_dimension_items(101000000008)
    assert isinstance(items, list)
    assert all(isinstance(item, DimensionWithCode) for item in items)
    assert any(
        ("warn" in record.levelname.lower() and "is discouraged." in record.msg)
        for record in caplog.records
    )


def test_get_dimension_items_with_users_warns(client: Client, caplog):
    items = client.transactional.get_dimension_items(101999999999)
    assert isinstance(items, list)
    assert all(isinstance(item, DimensionWithCode) for item in items)
    assert any(
        ("warn" in record.levelname.lower() and "is discouraged." in record.msg)
        for record in caplog.records
    )


def test_get_line_item_dimensions(client: Client):
    items = client.transactional.get_line_item_dimensions(284000000077)
    assert isinstance(items, list)
    assert all(isinstance(item, Dimension) for item in items)
