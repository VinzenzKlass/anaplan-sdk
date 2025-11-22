Note

This Class is not meant to be instantiated directly, but rather accessed through the `cw` Property on an instance of [Client](https://vinzenzklass.github.io/anaplan-sdk/api/sync/sync_client/index.md). For more details, see the [Guide](https://vinzenzklass.github.io/anaplan-sdk/guides/cloud_works/index.md).

## flows

```
flows: _AsyncFlowClient
```

Access the Integration Flow APIs.

## get_connections

```
get_connections() -> list[Connection]
```

List all Connections available in CloudWorks.

Returns:

| Type               | Description            |
| ------------------ | ---------------------- |
| `list[Connection]` | A list of connections. |

## create_connection

```
create_connection(con_info: ConnectionInput | dict[str, Any]) -> str
```

Create a new connection in CloudWorks.

Parameters:

| Name       | Type              | Description      | Default                                                                                                                                                                                                                    |
| ---------- | ----------------- | ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `con_info` | \`ConnectionInput | dict[str, Any]\` | The connection information. This can be a ConnectionInput instance or a dictionary as per the documentation. If a dictionary is passed, it will be validated against the ConnectionInput model before sending the request. |

Returns:

| Type  | Description                   |
| ----- | ----------------------------- |
| `str` | The ID of the new connection. |

## update_connection

```
update_connection(
    con_id: str, con_info: ConnectionBody | dict[str, Any]
) -> None
```

Update an existing connection in CloudWorks.

Parameters:

| Name       | Type             | Description                         | Default                                                                                                                                                                                                              |
| ---------- | ---------------- | ----------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `con_id`   | `str`            | The ID of the connection to update. | *required*                                                                                                                                                                                                           |
| `con_info` | \`ConnectionBody | dict[str, Any]\`                    | The name and details of the connection. You must pass all the same details as when initially creating the connection again. If you want to update only some of the details, use the patch_connection method instead. |

## patch_connection

```
patch_connection(con_id: str, body: dict[str, Any]) -> None
```

Update an existing connection in CloudWorks.

Parameters:

| Name     | Type             | Description                                                                                                                                         | Default    |
| -------- | ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| `con_id` | `str`            | The ID of the connection to update.                                                                                                                 | *required* |
| `body`   | `dict[str, Any]` | The name and details of the connection. You can pass all the same details as when initially creating the connection again, or just any one of them. | *required* |

## delete_connection

```
delete_connection(con_id: str) -> None
```

Delete an existing connection in CloudWorks.

Parameters:

| Name     | Type  | Description                         | Default    |
| -------- | ----- | ----------------------------------- | ---------- |
| `con_id` | `str` | The ID of the connection to delete. | *required* |

## get_integrations

```
get_integrations(
    sort_by: Literal["name"] | None = None, descending: bool = False
) -> list[Integration]
```

List all integrations in CloudWorks.

Parameters:

| Name         | Type              | Description                                              | Default                           |
| ------------ | ----------------- | -------------------------------------------------------- | --------------------------------- |
| `sort_by`    | \`Literal['name'] | None\`                                                   | The field to sort the results by. |
| `descending` | `bool`            | If True, the results will be sorted in descending order. | `False`                           |

Returns:

| Type                | Description             |
| ------------------- | ----------------------- |
| `list[Integration]` | A list of integrations. |

## get_integration

```
get_integration(integration_id: str) -> SingleIntegration
```

Get the details of a specific integration in CloudWorks.

**Note: This will not include the integration type! While present when listing integrations, the integration type is not included in the details of a single integration.**

Parameters:

| Name             | Type  | Description                            | Default    |
| ---------------- | ----- | -------------------------------------- | ---------- |
| `integration_id` | `str` | The ID of the integration to retrieve. | *required* |

Returns:

| Type                | Description                                                   |
| ------------------- | ------------------------------------------------------------- |
| `SingleIntegration` | The details of the integration, without the integration type. |

## create_integration

```
create_integration(
    body: IntegrationInput | IntegrationProcessInput | dict[str, Any],
) -> str
```

Create a new integration in CloudWorks. If not specified, the integration type will be either "Import" or "Export" based on the source and target you provide.

If you want to instead create a process Integration, you can do so by specifying the `process_id` parameter and passing several jobs. **Be careful to ensure, that all ids specified in the job inputs match what is defined in your model and matches the process.** If this is not the case, this will error, occasionally with a misleading error message, i.e. `XYZ is not defined in your model` even though it is, Anaplan just does not know what to do with it in the location you specified.

You can also use CloudWorks Integrations to simply schedule a process. To do this, you can simply pass an IntegrationProcessInput instance with the process_id and no jobs. This will create a process integration that will run the process you specified.

Parameters:

| Name   | Type               | Description             | Default          |
| ------ | ------------------ | ----------------------- | ---------------- |
| `body` | \`IntegrationInput | IntegrationProcessInput | dict[str, Any]\` |

Returns:

| Type  | Description                    |
| ----- | ------------------------------ |
| `str` | The ID of the new integration. |

## update_integration

```
update_integration(
    integration_id: str,
    body: IntegrationInput | IntegrationProcessInput | dict[str, Any],
) -> None
```

Update an existing integration in CloudWorks.

Parameters:

| Name             | Type               | Description                          | Default          |
| ---------------- | ------------------ | ------------------------------------ | ---------------- |
| `integration_id` | `str`              | The ID of the integration to update. | *required*       |
| `body`           | \`IntegrationInput | IntegrationProcessInput              | dict[str, Any]\` |

## run_integration

```
run_integration(integration_id: str) -> str
```

Run an integration in CloudWorks.

Parameters:

| Name             | Type  | Description                       | Default    |
| ---------------- | ----- | --------------------------------- | ---------- |
| `integration_id` | `str` | The ID of the integration to run. | *required* |

Returns:

| Type  | Description                 |
| ----- | --------------------------- |
| `str` | The ID of the run instance. |

## delete_integration

```
delete_integration(integration_id: str) -> None
```

Delete an existing integration in CloudWorks.

Parameters:

| Name             | Type  | Description                          | Default    |
| ---------------- | ----- | ------------------------------------ | ---------- |
| `integration_id` | `str` | The ID of the integration to delete. | *required* |

## get_run_history

```
get_run_history(integration_id: str) -> list[RunSummary]
```

Get the run history of a specific integration in CloudWorks.

Parameters:

| Name             | Type  | Description                                                | Default    |
| ---------------- | ----- | ---------------------------------------------------------- | ---------- |
| `integration_id` | `str` | The ID of the integration to retrieve the run history for. | *required* |

Returns:

| Type               | Description             |
| ------------------ | ----------------------- |
| `list[RunSummary]` | A list of run statuses. |

## get_run_status

```
get_run_status(run_id: str) -> RunStatus
```

Get the status of a specific run in CloudWorks.

Parameters:

| Name     | Type  | Description                    | Default    |
| -------- | ----- | ------------------------------ | ---------- |
| `run_id` | `str` | The ID of the run to retrieve. | *required* |

Returns:

| Type        | Description             |
| ----------- | ----------------------- |
| `RunStatus` | The details of the run. |

## get_run_error

```
get_run_error(run_id: str) -> RunError | None
```

Get the error details of a specific run in CloudWorks. This exposes potential underlying errors like the error of the invoked action, failure dumps and other details.

Parameters:

| Name     | Type  | Description                    | Default    |
| -------- | ----- | ------------------------------ | ---------- |
| `run_id` | `str` | The ID of the run to retrieve. | *required* |

Returns:

| Type       | Description |
| ---------- | ----------- |
| \`RunError | None\`      |

## create_schedule

```
create_schedule(
    integration_id: str, schedule: ScheduleInput | dict[str, Any]
) -> None
```

Schedule an integration in CloudWorks.

Parameters:

| Name             | Type            | Description                            | Default                                                                                                                                                                                                              |
| ---------------- | --------------- | -------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `integration_id` | `str`           | The ID of the integration to schedule. | *required*                                                                                                                                                                                                           |
| `schedule`       | \`ScheduleInput | dict[str, Any]\`                       | The schedule information. This can be a ScheduleInput instance or a dictionary as per the documentation. If a dictionary is passed, it will be validated against the ScheduleInput model before sending the request. |

## update_schedule

```
update_schedule(
    integration_id: str, schedule: ScheduleInput | dict[str, Any]
) -> None
```

Update an integration Schedule in CloudWorks. A schedule must already exist.

Parameters:

| Name             | Type            | Description                            | Default                                                                                                                                                                                                              |
| ---------------- | --------------- | -------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `integration_id` | `str`           | The ID of the integration to schedule. | *required*                                                                                                                                                                                                           |
| `schedule`       | \`ScheduleInput | dict[str, Any]\`                       | The schedule information. This can be a ScheduleInput instance or a dictionary as per the documentation. If a dictionary is passed, it will be validated against the ScheduleInput model before sending the request. |

## set_schedule_status

```
set_schedule_status(
    integration_id: str, status: Literal["enabled", "disabled"]
) -> None
```

Set the status of an integration schedule in CloudWorks. A schedule must already exist.

Parameters:

| Name             | Type                             | Description                                                             | Default    |
| ---------------- | -------------------------------- | ----------------------------------------------------------------------- | ---------- |
| `integration_id` | `str`                            | The ID of the integration to schedule.                                  | *required* |
| `status`         | `Literal['enabled', 'disabled']` | The status of the schedule. This can be either "enabled" or "disabled". | *required* |

## delete_schedule

```
delete_schedule(integration_id: str) -> None
```

Delete an integration schedule in CloudWorks. A schedule must already exist.

Parameters:

| Name             | Type  | Description                            | Default    |
| ---------------- | ----- | -------------------------------------- | ---------- |
| `integration_id` | `str` | The ID of the integration to schedule. | *required* |

## get_notification_config

```
get_notification_config(
    notification_id: str | None = None, integration_id: str | None = None
) -> NotificationConfig
```

Get the notification configuration, either by its Id, or the notification configuration for a specific integration. If the integration_id is specified, the notification_id will be ignored.

Parameters:

| Name              | Type  | Description | Default                                                                   |
| ----------------- | ----- | ----------- | ------------------------------------------------------------------------- |
| `notification_id` | \`str | None\`      | The ID of the notification configuration to retrieve.                     |
| `integration_id`  | \`str | None\`      | The ID of the integration to retrieve the notification configuration for. |

Returns:

| Type                 | Description                                    |
| -------------------- | ---------------------------------------------- |
| `NotificationConfig` | The details of the notification configuration. |

## create_notification_config

```
create_notification_config(config: NotificationInput | dict[str, Any]) -> str
```

Create a notification configuration for an integration in CloudWorks. This will error if there is already a notification configuration for the integration, which is also the case by default. In this case, you will want to use the `update_notification_config` method instead, to partially update the existing configuration or overwrite it.

Parameters:

| Name     | Type                | Description      | Default                                                                                                                                                                                                                             |
| -------- | ------------------- | ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `config` | \`NotificationInput | dict[str, Any]\` | The notification configuration. This can be a NotificationInput instance or a dictionary as per the documentation. If a dictionary is passed, it will be validated against the NotificationConfig model before sending the request. |

Returns:

| Type  | Description                                   |
| ----- | --------------------------------------------- |
| `str` | The ID of the new notification configuration. |

## update_notification_config

```
update_notification_config(
    notification_id: str, config: NotificationInput | dict[str, Any]
) -> None
```

Update a notification configuration for an integration in CloudWorks. You cannot pass empty values or nulls to any of the fields If you want to for e.g. override an existing list of users with an empty one, you must delete the notification configuration and create a new one with only the values you want to keep.

Parameters:

| Name              | Type                | Description                                         | Default                                                                                                                                                                                                                             |
| ----------------- | ------------------- | --------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `notification_id` | `str`               | The ID of the notification configuration to update. | *required*                                                                                                                                                                                                                          |
| `config`          | \`NotificationInput | dict[str, Any]\`                                    | The notification configuration. This can be a NotificationInput instance or a dictionary as per the documentation. If a dictionary is passed, it will be validated against the NotificationConfig model before sending the request. |

## delete_notification_config

```
delete_notification_config(
    notification_id: str | None = None, integration_id: str | None = None
) -> None
```

Delete a notification configuration for an integration in CloudWorks, either by its Id, or the notification configuration for a specific integration. If the integration_id is specified, the notification_id will be ignored.

Parameters:

| Name              | Type  | Description | Default                                                         |
| ----------------- | ----- | ----------- | --------------------------------------------------------------- |
| `notification_id` | \`str | None\`      | The ID of the notification configuration to delete.             |
| `integration_id`  | \`str | None\`      | The ID of the integration to delete the notification config of. |

## get_import_error_dump

```
get_import_error_dump(run_id: str) -> bytes
```

Get the error dump of a specific import run in CloudWorks. Calling this for a run_id that did not generate any failure dumps will produce an error.

**Note that if you need the error dump of an action in a process, you must use the `get_process_error_dump` method instead.**

Parameters:

| Name     | Type  | Description                    | Default    |
| -------- | ----- | ------------------------------ | ---------- |
| `run_id` | `str` | The ID of the run to retrieve. | *required* |

Returns:

| Type    | Description     |
| ------- | --------------- |
| `bytes` | The error dump. |

## get_process_error_dump

```
get_process_error_dump(run_id: str, action_id: int | str) -> bytes
```

Get the error dump of a specific import run in CloudWorks, that is part of a process. Calling this for a run_id that did not generate any failure dumps will produce an error.

Parameters:

| Name        | Type  | Description                    | Default                                                              |
| ----------- | ----- | ------------------------------ | -------------------------------------------------------------------- |
| `run_id`    | `str` | The ID of the run to retrieve. | *required*                                                           |
| `action_id` | \`int | str\`                          | The ID of the action to retrieve. This can be found in the RunError. |

Returns:

| Type    | Description     |
| ------- | --------------- |
| `bytes` | The error dump. |
