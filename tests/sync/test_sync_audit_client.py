from anaplan_sdk import Client
from anaplan_sdk.models import User


def test_list_users(client: Client) -> None:
    users, search = client.audit.get_users(), client.audit.get_users("vinzenz")
    assert isinstance(users, list)
    assert all(isinstance(user, User) for user in users)
    assert all(isinstance(user, User) for user in search)
    assert len(users) > 0
    assert len(search) > 0
    assert len(search) < len(users)


def test_get_user(client: Client) -> None:
    user = client.audit.get_user()
    assert isinstance(user, User)


def test_events(client: Client) -> None:
    events = client.audit.get_events(1)
    assert isinstance(events, list)
