# SCIM API

The Anaplan SDK provides access to the SCIM (System for Cross-domain Identity Management) API for managing user identities within your Anaplan tenant. Despite its name, the Anaplan SCIM API is only partially [RFC 7643](https://datatracker.ietf.org/doc/html/rfc7643) & [RFC 7644](https://datatracker.ietf.org/doc/html/rfc7644) compliant.

## Basic Usage

```
from anaplan_sdk import Client

anaplan = Client(
    certificate=getenv("ANAPLAN_CERT"), private_key=getenv("ANAPLAN_PK")
)
# See Available Features
config = anaplan.scim.get_service_provider_config()
resources = anaplan.scim.get_resource_types()  # See Available Resources
schemas = anaplan.scim.get_resource_schemas()  # See Available Schemas
users = anaplan.scim.get_users()  # All internal users
user = anaplan.scim.get_user("123")  # specific user
```

```
from asyncio import gather

from anaplan_sdk import AsyncClient

anaplan = AsyncClient(
    certificate=getenv("ANAPLAN_CERT"), private_key=getenv("ANAPLAN_PK")
)
config, resources, schemas, users, user = await gather(
    anaplan.scim.get_service_provider_config(),  # See Available Features
    anaplan.scim.get_resource_types(),  # See Available Resources
    anaplan.scim.get_resource_schemas(),  # See Available Schemas
    anaplan.scim.get_users(),  # All internal users
    anaplan.scim.get_user("123"),  # specific user
)
```

## Filtering Users

You can filter users based on specific attributes by passing a predicate string as per the RFC, e.g. `active eq true`.

```
users = await anaplan.scim.get_users("active eq true")
```

```
users = await anaplan.scim.get_users("active eq true")
```

Anaplan supports filtering by the following attributes:

`id`, `externalId`, `userName`, `name.givenName`, `name.familyName`, `active`

and the following operators:

`eq`, `ne`, `gt`, `ge`, `lt`, `le` and `pr`. These can be combined with `and` and `or` logical operators and grouped with parentheses `(` and `)`.

As an alternative to manually constructing the filter predicate string, you can use the expression language provided by the SDK to build the filter expression programmatically. This approach can help avoid syntax errors and improve readability, and make is easier to compose more complex expressions. The expression language is heavily inspired by the [polars expression syntax](https://docs.pola.rs/user-guide/expressions/basic-operations/#boolean-and-bitwise-operations).

The expression langauge supports all operators implemented by Anaplan, is fully type-hinted, reducing the risk of referencing fields you cannot filter by. It also supports truthy / falsy values allowing you to avoid explicitly spelling out `== True` comparisons.

```
from anaplan_sdk import field


part = (
    field("active")  # "active eq true"
    & field("userName")  # "userName pr"
    & (field("name.givenName") > "Thomas")
)
predicate = (field("userName") == "test.user@valantic.com") | (
    part | (~field("active") & (field("name.givenName") != "Thomas"))
)
```

Note that we need to wrap `(~field("active")` in parentheses to ensure the correct operator precedence. Anaplan does not support the `not` operator,

`~field("active") & (field("name.givenName") != "Thomas")`

would thus be invalid, since we cannot negate the logical expression and the `&` evaluates before the `~`.

## Updating Users

You can update users by performing partial operations on specific attributes or by replacing the entire user object. You can pass the provided Pydantic models, or a dictionary with the appropriate structure. If you pass a dictionary, it will be validated against the Pydantic models before being sent to Anaplan. This avoids unnecessary requests and gives you more concise error messages.

```
from anaplan_sdk.models.scim import Remove, Replace

user = anaplan.scim.update_user(
    "123",
    [Replace(path="active", value=False), Remove(path="entitlements")],
)
```

```
from anaplan_sdk.models.scim import Remove, Replace

user = await anaplan.scim.update_user(
    "123",
    [Replace(path="active", value=False), Remove(path="entitlements")],
)
```

Both methods return an updated user object.

```
from anaplan_sdk.models.scim import NameInput, ReplaceUserInput

user = anaplan.scim.replace_user(
    "123",
    ReplaceUserInput(
        id="123",
        name=NameInput(given_name="Test", family_name="User"),
        user_name="test.user@valantic.com",
    ),
)
```

```
from anaplan_sdk.models.scim import NameInput, ReplaceUserInput

user = await anaplan.scim.replace_user(
    "123",
    ReplaceUserInput(
        id="123",
        name=NameInput(given_name="Test", family_name="User"),
        user_name="test.user@valantic.com",
    ),
)
```
