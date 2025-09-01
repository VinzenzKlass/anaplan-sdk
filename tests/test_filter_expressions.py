from anaplan_sdk import field


def test_active():
    assert str(field("active")) == "active eq true"


def test_not_active():
    assert str(~field("active")) == "active eq false"


def test_name_truthy():
    assert str(field("userName")) == "userName pr"


def test_name_falsy():
    assert str(~field("userName")) == "userName eq null"


def test_eq():
    assert str(field("id") == "123") == 'id eq "123"'


def test_ne():
    assert str(field("id") != "123") == 'id ne "123"'


def test_gt():
    assert str(field("name.givenName") > "zzz") == 'name.givenName gt "zzz"'


def test_ge():
    assert str(field("name.givenName") >= "zzz") == 'name.givenName ge "zzz"'


def test_lt():
    assert str(field("name.givenName") < "zzz") == 'name.givenName lt "zzz"'


def test_le():
    assert str(field("name.givenName") <= "zzz") == 'name.givenName le "zzz"'


def test_and():
    assert str(field("active") & (field("id") == "123")) == 'active eq true and id eq "123"'


def test_or():
    assert str(field("active") | (field("id") == "123")) == 'active eq true or id eq "123"'


def test_op_order():
    expr = (field("active") & (field("id") == "123")) | ~field("userName")
    assert str(expr) == '(active eq true and id eq "123") or userName eq null'


def test_compose():
    part = field("active") & field("userName") & (field("name.givenName") > "Thomas")
    assert str(part) == 'active eq true and userName pr and name.givenName gt "Thomas"'
    predicate = (field("userName") == "test.user@valantic.com") | (
        part | (~field("active") & (field("name.givenName") != "Thomas"))
    )
    assert str(predicate) == (
        'userName eq "test.user@valantic.com" or ((active eq true and userName pr and '
        'name.givenName gt "Thomas") or (active eq false and name.givenName ne "Thomas"))'
    )
