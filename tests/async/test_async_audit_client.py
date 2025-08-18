from asyncio import gather

from anaplan_sdk.models import User


async def test_list_users(client):
    users, search = await gather(client.audit.get_users(), client.audit.get_users("vinzenz"))
    assert isinstance(users, list)
    assert all(isinstance(user, User) for user in users)
    assert all(isinstance(user, User) for user in search)
    assert len(users) > 0
    assert len(search) > 0
    assert len(search) < len(users)


async def test_get_user(client):
    user = await client.audit.get_user()
    assert isinstance(user, User)


async def test_events(client):
    events = await client.audit.get_events(1)
    assert isinstance(events, list)
