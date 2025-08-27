from anaplan_sdk import AsyncClient
from anaplan_sdk.models.scim import (
    NameInput,
    Remove,
    Replace,
    ReplaceUserInput,
    Resource,
    Schema,
    ServiceProviderConfig,
    User,
    field,
)


async def test_get_service_provider_config(client: AsyncClient):
    conf = await client.scim.get_service_provider_config()
    assert isinstance(conf, ServiceProviderConfig)


async def test_get_resource_types(client: AsyncClient):
    res_types = await client.scim.get_resource_types()
    assert isinstance(res_types, list)
    assert all(isinstance(r, Resource) for r in res_types)


async def test_get_resource_schemas(client: AsyncClient):
    schemas = await client.scim.get_resource_schemas()
    assert isinstance(schemas, list)
    assert all(isinstance(s, Schema) for s in schemas)


async def test_get_users(client: AsyncClient):
    users = await client.scim.get_users()
    assert isinstance(users, list)
    assert all(isinstance(u, User) for u in users)


async def test_get_user_filtered(client: AsyncClient, name: str = "test.user@valantic.com"):
    users = await client.scim.get_users(field("userName") == name)
    assert isinstance(users, list)
    assert all(isinstance(u, User) for u in users)
    assert all(u.user_name == name for u in users)


async def test_get_user(client: AsyncClient, user_id: str = "38a0546fd5894c1fac87f8fb71566b3f"):
    user = await client.scim.get_user(user_id)
    assert isinstance(user, User)
    assert user.id == user_id


async def test_replace_user(client: AsyncClient, user_id: str = "38a0546fd5894c1fac87f8fb71566b3f"):
    user = await client.scim.replace_user(
        user_id,
        ReplaceUserInput(
            id=user_id,
            name=NameInput(given_name="Test", family_name="User"),
            user_name="test.user@valantic.com",
        ),
    )
    assert isinstance(user, User)
    assert user.id == user_id
    assert user.name.given_name == "Test"
    assert user.name.family_name == "User"


async def test_create_update_user(
    client: AsyncClient, user_id: str = "38a0546fd5894c1fac87f8fb71566b3f"
):
    user = await client.scim.update_user(
        user_id, [Replace(path="active", value=False), Remove(path="entitlements")]
    )
    assert isinstance(user, User)
    assert user.id == user_id
    assert user.active is False
    assert user.entitlements == []
