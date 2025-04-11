from anaplan_sdk import AsyncClient, models


async def test_list_users(client: AsyncClient):
    users = await client.audit.list_users()
    assert isinstance(users, list)
    assert isinstance(users[0], models.User)


async def test_events(client: AsyncClient):
    events = await client.audit.get_events(1)
    assert isinstance(events, list)
