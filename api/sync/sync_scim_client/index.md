Note

This Class is not meant to be instantiated directly, but rather accessed through the `scim` Property on an instance of [Client](https://vinzenzklass.github.io/anaplan-sdk/api/sync/sync_client/index.md). For more details, see the [Guide](https://vinzenzklass.github.io/anaplan-sdk/guides/scim/index.md).

## get_service_provider_config

```
get_service_provider_config() -> ServiceProviderConfig
```

Get the SCIM Service Provider Configuration.

Returns:

| Type                    | Description                                                              |
| ----------------------- | ------------------------------------------------------------------------ |
| `ServiceProviderConfig` | The ServiceProviderConfig object describing the available SCIM features. |

## get_resource_types

```
get_resource_types() -> list[Resource]
```

Get the SCIM Resource Types.

Returns:

| Type             | Description                                                    |
| ---------------- | -------------------------------------------------------------- |
| `list[Resource]` | A list of Resource objects describing the SCIM resource types. |

## get_resource_schemas

```
get_resource_schemas() -> list[Schema]
```

Get the SCIM Resource Schemas.

Returns:

| Type           | Description                                                    |
| -------------- | -------------------------------------------------------------- |
| `list[Schema]` | A list of Schema objects describing the SCIM resource schemas. |

## get_users

```
get_users(
    predicate: str | field | None = None, page_size: int = 100
) -> list[User]
```

Get a list of users, optionally filtered by a predicate. Keep in mind that this will only return internal users. To get a list of all users in the tenant, use the `get_users()` in the `audit` namespace instead.

Parameters:

| Name        | Type  | Description                                                         | Default |
| ----------- | ----- | ------------------------------------------------------------------- | ------- |
| `predicate` | \`str | field                                                               | None\`  |
| `page_size` | `int` | The number of users to fetch per page. Values above 100 will error. | `100`   |

Returns:

| Type         | Description                                        |
| ------------ | -------------------------------------------------- |
| `list[User]` | The internal users optionally matching the filter. |

## get_user

```
get_user(user_id: str) -> User
```

Get a user by their ID.

Parameters:

| Name      | Type  | Description                  | Default    |
| --------- | ----- | ---------------------------- | ---------- |
| `user_id` | `str` | The ID of the user to fetch. | *required* |

Returns:

| Type   | Description      |
| ------ | ---------------- |
| `User` | The User object. |

## add_user

```
add_user(user: UserInput | dict[str, Any]) -> User
```

Add a new user to your Anaplan tenant.

Parameters:

| Name   | Type        | Description      | Default                                                                                                                                                                                                                                               |
| ------ | ----------- | ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `user` | \`UserInput | dict[str, Any]\` | The user info to add. Can either be a UserInput object or a dict. If you pass a dict, it will be validated against the UserInput model before sending. If the info you provided is invalid or incomplete, this will raise a pydantic.ValidationError. |

Returns:

| Type   | Description              |
| ------ | ------------------------ |
| `User` | The created User object. |

## replace_user

```
replace_user(user_id: str, user: ReplaceUserInput | dict[str, Any])
```

Replace an existing user with new information. Note that this will replace all fields of the

Parameters:

| Name      | Type               | Description                | Default                                                                                                                                                                                                                                                          |
| --------- | ------------------ | -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `user_id` | `str`              | ID of the user to replace. | *required*                                                                                                                                                                                                                                                       |
| `user`    | \`ReplaceUserInput | dict[str, Any]\`           | The new user info. Can either be a ReplaceUserInput object or a dict. If you pass a dict, it will be validated against the ReplaceUserInput model before sending. If the info you provided is invalid or incomplete, this will raise a pydantic.ValidationError. |

Returns:

| Type | Description              |
| ---- | ------------------------ |
|      | The updated User object. |

## update_user

```
update_user(
    user_id: str, operations: list[Operation] | list[dict[str, Any]]
) -> User
```

Update an existing user with a list of operations. This allows you to update only specific fields of the user without replacing the entire user.

Parameters:

| Name         | Type              | Description                   | Default                                                                                                                                                                                                                                                                                                                                                                                                              |
| ------------ | ----------------- | ----------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `user_id`    | `str`             | The ID of the user to update. | *required*                                                                                                                                                                                                                                                                                                                                                                                                           |
| `operations` | \`list[Operation] | list\[dict[str, Any]\]\`      | A list of operations to perform on the user. Each operation can either be an Operation object or a dict. If you pass a dict, it will be validated against the Operation model before sending. If the operation is invalid, this will raise a pydantic.ValidationError. You can also use the models Replace, Add and Remove which are subclasses of Operation and provide a more convenient way to create operations. |

Returns:

| Type   | Description              |
| ------ | ------------------------ |
| `User` | The updated User object. |
