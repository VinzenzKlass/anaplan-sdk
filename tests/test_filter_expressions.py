from anaplan_sdk import field


def test_active():
    assert field("active") == "active eq true"


def test_not_active():
    assert ~field("active") == "active eq false"


def test_name_truthy():
    assert field("userName") == "name pr"


def test_name_falsy():
    assert ~field("userName") == "name eq null"


def test_eq():
    assert (field("id") == "123") == 'id eq "123"'


def test_ne():
    assert (field("id") != "123") == 'id ne "123"'


def test_gt():
    assert (field("name.givenName") > "zzz") == 'name.givenName gt "zzz"'


def test_ge():
    assert (field("name.givenName") >= "zzz") == 'name.givenName ge "zzz"'


def test_lt():
    assert (field("name.givenName") < "zzz") == 'name.givenName lt "zzz"'


def test_le():
    assert (field("name.givenName") <= "zzz") == 'name.givenName le "zzz"'


def test_and():
    assert (field("active") & (field("id") == "123")) == 'active eq true and id eq "123"'


def test_or():
    assert (field("active") | (field("id") == "123")) == 'active eq true or id eq "123"'


def test_op_order():
    expr = (field("active") & (field("id") == "123")) | ~field("userName")
    assert expr == '((active eq true and id eq "123") or name eq null)'


def test_compose():
    part = field("active") & field("userName") & (field("name.givenName") > "Thomas")
    predicate = (field("userName") == "test.user@valantic.com") | (
        part | (~field("active") & (field("name.givenName") != "Thomas"))
    )
    assert part == 'active eq true and userName pr and name.givenName gt "Thomas"'
    assert predicate == (
        'userName eq "test.user@valantic.com" or (active eq true and userName pr and '
        'name.givenName gt "Thomas") or (active eq false and name.givenName ne "Thomas")'
    )
