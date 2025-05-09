from anaplan_sdk import Client
from anaplan_sdk.models import User


def test_list_users(client: Client):
    users = client.audit.list_users()
    assert isinstance(users, list)
    assert isinstance(users[0], User)
    assert len(users) > 0


def test_get_user (client: Client):
    user = client.audit.get_user()
    assert isinstance (user, User)


def test_events(client: Client):
    events = client.audit.get_events(1)
    assert isinstance(events, list)
