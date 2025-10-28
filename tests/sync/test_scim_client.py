from anaplan_sdk import Client
from anaplan_sdk.models.scim import (
    MetaWithDates,
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


def test_get_service_provider_config(client: Client):
    conf = client.scim.get_service_provider_config()
    assert isinstance(conf, ServiceProviderConfig)


def test_get_resource_types(client: Client):
    res_types = client.scim.get_resource_types()
    assert isinstance(res_types, list)
    assert all(isinstance(r, Resource) for r in res_types)


def test_get_resource_schemas(client: Client):
    schemas = client.scim.get_resource_schemas()
    assert isinstance(schemas, list)
    assert all(isinstance(s, Schema) for s in schemas)


def test_get_users(client: Client):
    users = client.scim.get_users()
    assert isinstance(users, list)
    assert all(isinstance(u, User) for u in users)


def test_get_user_filtered(client: Client, name: str = "test.user@valantic.com"):
    users = client.scim.get_users(field("userName") == name)
    assert isinstance(users, list)
    assert all(isinstance(u, User) for u in users)
    assert all(u.user_name == name for u in users)


def test_get_user(client: Client, scim_user_id: str):
    user = client.scim.get_user(scim_user_id)
    assert isinstance(user, User)
    assert user.id == scim_user_id
    assert isinstance(user.meta, MetaWithDates)


def test_replace_user(client: Client, scim_user_id: str):
    user = client.scim.replace_user(
        scim_user_id,
        ReplaceUserInput(
            id=scim_user_id,
            name=NameInput(given_name="Test", family_name="User"),
            user_name="test.user@valantic.com",
        ),
    )
    assert isinstance(user, User)
    assert user.id == scim_user_id
    assert user.name.given_name == "Test"
    assert user.name.family_name == "User"


def test_create_update_user(client: Client, scim_user_id: str):
    user = client.scim.update_user(
        scim_user_id, [Replace(path="active", value=False), Remove(path="entitlements")]
    )
    assert isinstance(user, User)
    assert user.id == scim_user_id
    assert user.active is False
    assert user.entitlements == []
