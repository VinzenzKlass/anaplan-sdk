import asyncio
import os

import pytest

import anaplan_sdk
from anaplan_sdk.models import User

client = anaplan_sdk.AsyncClient(
    workspace_id=os.getenv("ANAPLAN_SDK_TEST_WORKSPACE_ID"),
    model_id=os.getenv("ANAPLAN_SDK_TEST_MODEL_ID"),
    certificate=os.getenv("ANAPLAN_SDK_TEST_CERT"),
    private_key=os.getenv("ANAPLAN_SDK_TEST_PK"),
    retry_count=3,
).audit


@pytest.fixture(scope="module")
def event_loop():
    yield asyncio.get_event_loop()


@pytest.mark.asyncio
async def test_list_users():
    users = await client.list_users()
    assert isinstance(users, list)
    assert isinstance(users[0], User)


@pytest.mark.asyncio
async def test_events():
    events = await client.get_events(1)
    assert isinstance(events, list)
