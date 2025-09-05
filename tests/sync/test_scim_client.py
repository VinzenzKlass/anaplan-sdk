from anaplan_sdk import Client


def test_get_users(client: Client):
    users = client.scim.list_users('name.givenName Eq "Michael"')
    assert isinstance(users, list)
    assert len(users) > 0


def test_get_user(client: Client):
    me = client.audit.get_user()
    user = client.scim.get_user (me.id)
    assert user.user_name == me.email

