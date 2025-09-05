from anaplan_sdk import AsyncClient


async def test_get_users(client: AsyncClient):
    users = await client.scim.list_users('name.givenName Eq "Michael"')
    assert isinstance(users, list)
    assert len(users) > 0


async def test_get_user(client: AsyncClient):
    me = await client.audit.get_user()
    user = await client.scim.get_user (me.id)
    assert user.user_name == me.email

