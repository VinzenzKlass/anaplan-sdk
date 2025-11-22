Note

This Class is not meant to be instantiated directly, but rather accessed through the `audit` Property on an instance of [Client](https://vinzenzklass.github.io/anaplan-sdk/api/sync/sync_client/index.md). For more details, see the [Guide](https://vinzenzklass.github.io/anaplan-sdk/guides/audit/index.md).

## get_users

```
get_users(
    search_pattern: str | None = None,
    sort_by: UserSortBy = None,
    descending: bool = False,
) -> list[User]
```

Lists all the Users in the authenticated users default tenant.

Parameters:

| Name             | Type         | Description                                              | Default                                                                                                                                                                                                                                                                                                                                                                                               |
| ---------------- | ------------ | -------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `search_pattern` | \`str        | None\`                                                   | Caution: This is an undocumented Feature and may behave unpredictably. It requires the Tenant Admin role. For non-admin users, it is ignored. Optionally filter for specific users. When provided, case-insensitive matches users with emails or names containing this string. You can use the wildcards % for 0-n characters, and _ for exactly 1 character. When None (default), returns all users. |
| `sort_by`        | `UserSortBy` | The field to sort the results by.                        | `None`                                                                                                                                                                                                                                                                                                                                                                                                |
| `descending`     | `bool`       | If True, the results will be sorted in descending order. | `False`                                                                                                                                                                                                                                                                                                                                                                                               |

Returns:

| Type         | Description        |
| ------------ | ------------------ |
| `list[User]` | The List of Users. |

## get_user

```
get_user(user_id: str = 'me') -> User
```

Retrieves information about the specified user, or the authenticated user if none specified.

Returns:

| Type   | Description                                    |
| ------ | ---------------------------------------------- |
| `User` | The requested or currently authenticated User. |

## get_events

```
get_events(
    days_into_past: int = 30, event_type: Event = "all"
) -> list[dict[str, Any]]
```

Get audit events from Anaplan Audit API.

Parameters:

| Name             | Type    | Description                                                                                 | Default |
| ---------------- | ------- | ------------------------------------------------------------------------------------------- | ------- |
| `days_into_past` | `int`   | The nuber of days into the past to get events for. The API provides data for up to 30 days. | `30`    |
| `event_type`     | `Event` | The type of events to get.                                                                  | `'all'` |

Returns:

| Type                   | Description                                                             |
| ---------------------- | ----------------------------------------------------------------------- |
| `list[dict[str, Any]]` | A list of log entries, each containing a dictionary with event details. |
