import os

import anaplan_sdk
from anaplan_sdk.models import User

client = anaplan_sdk.Client(
    workspace_id=os.getenv("ANAPLAN_SDK_TEST_WORKSPACE_ID"),
    model_id=os.getenv("ANAPLAN_SDK_TEST_MODEL_ID"),
    certificate=os.getenv("ANAPLAN_SDK_TEST_CERT"),
    private_key=os.getenv("ANAPLAN_SDK_TEST_PK"),
    retry_count=3,
).audit


def test_list_users():
    users = client.list_users()
    assert isinstance(users, list)
    assert isinstance(users[0], User)
    assert len(users) > 0


def test_events():
    events = client.get_events(1)
    assert isinstance(events, list)
