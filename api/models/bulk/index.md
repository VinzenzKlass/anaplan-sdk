## Workspace

Parameters:

| Name             | Type   | Description                                                     | Default    |
| ---------------- | ------ | --------------------------------------------------------------- | ---------- |
| `id`             | `str`  | The unique identifier of this workspace.                        | *required* |
| `name`           | `str`  | The name of this workspace that is also displayed to the users. | *required* |
| `active`         | `bool` | Whether this workspace is active or not.                        | *required* |
| `size_allowance` | `int`  | The maximum allowed size of this workspace in bytes.            | *required* |
| `current_size`   | `int`  | The current size of this workspace in bytes.                    | *required* |

## Model

Parameters:

| Name                         | Type                                                                                               | Description                                                             | Default    |
| ---------------------------- | -------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- | ---------- |
| `id`                         | `str`                                                                                              | The unique identifier of this model.                                    | *required* |
| `name`                       | `str`                                                                                              |                                                                         | *required* |
| `active_state`               | `Literal['ARCHIVED', 'UNLOCKED', 'ACTIVE', 'PRODUCTION', 'MAINTENANCE', 'PRODUCTION_MAINTENANCE']` | The current state of this model.                                        | *required* |
| `last_saved_serial_number`   | `int`                                                                                              | The serial number of the last save of this model.                       | *required* |
| `last_modified_by_user_guid` | `str`                                                                                              | The unique identifier of the user who last modified this model.         | *required* |
| `memory_usage`               | `int`                                                                                              | The memory usage of this model in bytes.                                | `0`        |
| `workspace_id`               | `str`                                                                                              | The unique identifier of the workspace that this model is currently in. | *required* |
| `workspace_name`             | `str`                                                                                              | The name of the workspace that this model is currently in.              | *required* |
| `url`                        | `str`                                                                                              | The current URL of this model.                                          | *required* |
| `category_values`            | `list[Any]`                                                                                        | The category values of this model.                                      | *required* |
| `iso_creation_date`          | `str`                                                                                              | The creation date of this model in ISO format.                          | *required* |
| `last_modified`              | `str`                                                                                              | The last modified date of this model.                                   | *required* |

## ModelWithTransactionInfo

Parameters:

| Name                         | Type                                                                                               | Description                                                             | Default    |
| ---------------------------- | -------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- | ---------- |
| `id`                         | `str`                                                                                              | The unique identifier of this model.                                    | *required* |
| `name`                       | `str`                                                                                              |                                                                         | *required* |
| `active_state`               | `Literal['ARCHIVED', 'UNLOCKED', 'ACTIVE', 'PRODUCTION', 'MAINTENANCE', 'PRODUCTION_MAINTENANCE']` | The current state of this model.                                        | *required* |
| `last_saved_serial_number`   | `int`                                                                                              | The serial number of the last save of this model.                       | *required* |
| `last_modified_by_user_guid` | `str`                                                                                              | The unique identifier of the user who last modified this model.         | *required* |
| `memory_usage`               | `int`                                                                                              | The memory usage of this model in bytes.                                | `0`        |
| `workspace_id`               | `str`                                                                                              | The unique identifier of the workspace that this model is currently in. | *required* |
| `workspace_name`             | `str`                                                                                              | The name of the workspace that this model is currently in.              | *required* |
| `url`                        | `str`                                                                                              | The current URL of this model.                                          | *required* |
| `category_values`            | `list[Any]`                                                                                        | The category values of this model.                                      | *required* |
| `iso_creation_date`          | `str`                                                                                              | The creation date of this model in ISO format.                          | *required* |
| `last_modified`              | `str`                                                                                              | The last modified date of this model.                                   | *required* |
| `model_transaction_running`  | `bool`                                                                                             | Whether a transaction is currently running on this model.               | *required* |

## File

Parameters:

| Name             | Type  | Description                                        | Default                          |
| ---------------- | ----- | -------------------------------------------------- | -------------------------------- |
| `id`             | `int` | The unique identifier of this file.                | *required*                       |
| `name`           | `str` | The name of this file.                             | *required*                       |
| `chunk_count`    | `int` | The number of chunks this file is split into.      | *required*                       |
| `delimiter`      | \`str | None\`                                             | The delimiter used in this file. |
| `encoding`       | \`str | None\`                                             | The encoding of this file.       |
| `first_data_row` | `int` | The row number of the first data row in this file. | *required*                       |
| `format`         | \`str | None\`                                             | The format of this file.         |
| `header_row`     | `int` | The row number of the header row in this file.     | *required*                       |
| `separator`      | \`str | None\`                                             | The separator used in this file. |

## List

Parameters:

| Name   | Type  | Description                         | Default    |
| ------ | ----- | ----------------------------------- | ---------- |
| `id`   | `int` | The unique identifier of this list. | *required* |
| `name` | `str` | The name of this list.              | *required* |

## ListMetadata

Parameters:

| Name                            | Type        | Description                                               | Default                                  |
| ------------------------------- | ----------- | --------------------------------------------------------- | ---------------------------------------- |
| `id`                            | `int`       | The unique identifier of this list.                       | *required*                               |
| `name`                          | `str`       | The name of this list.                                    | *required*                               |
| `has_selective_access`          | `bool`      | Whether this list has selective access or not.            | *required*                               |
| `properties`                    | `list[Any]` | The properties of this list.                              | `[]`                                     |
| `production_data`               | `bool`      | Whether this list is production data or not.              | *required*                               |
| `managed_by`                    | `str`       | The user who manages this list.                           | *required*                               |
| `numbered_list`                 | `bool`      | Whether this list is a numbered list or not.              | *required*                               |
| `use_top_level_as_page_default` | `bool`      | Whether the top level is used as the page default or not. | *required*                               |
| `item_count`                    | `int`       | The number of items in this list.                         | *required*                               |
| `next_item_index`               | \`int       | None\`                                                    | The index of the next item in this list. |
| `workflow_enabled`              | `bool`      | Whether the workflow is enabled for this list or not.     | *required*                               |
| `permitted_items`               | `int`       | The number of permitted items in this list.               | *required*                               |
| `used_in_applies_to`            | \`str       | None\`                                                    | The applies to value of this list.       |

## Action

Parameters:

| Name   | Type  | Description                                                                   | Default                  |
| ------ | ----- | ----------------------------------------------------------------------------- | ------------------------ |
| `id`   | `int` | The unique identifier of this action.                                         | *required*               |
| `name` | `str` | The name of this Action. This is the same as the one displayed in the Web UI. | *required*               |
| `type` | \`str | None\`                                                                        | The type of this action. |

## Process

Parameters:

| Name   | Type  | Description                            | Default    |
| ------ | ----- | -------------------------------------- | ---------- |
| `id`   | `int` | The unique identifier of this process. | *required* |
| `name` | `str` | The name of this process.              | *required* |

## Import

Parameters:

| Name      | Type                                                                                    | Description                           | Default                                                                                                                         |
| --------- | --------------------------------------------------------------------------------------- | ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `id`      | `int`                                                                                   | The unique identifier of this import. | *required*                                                                                                                      |
| `name`    | `str`                                                                                   | The name of this import.              | *required*                                                                                                                      |
| `type`    | `Literal['MODULE_DATA', 'HIERARCHY_DATA', 'LINE_ITEM_DEFINITION', 'USERS', 'VERSIONS']` | The type of this import.              | *required*                                                                                                                      |
| `file_id` | \`int                                                                                   | None\`                                | The unique identifier of the data source of this import. If it is absent, it means that the import does not read from any file. |

## Export

Parameters:

| Name       | Type                                                                                                                                                | Description                                                           | Default                      |
| ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- | ---------------------------- |
| `id`       | `int`                                                                                                                                               | The unique identifier of this export.                                 | *required*                   |
| `name`     | `str`                                                                                                                                               | The name of this export.                                              | *required*                   |
| `type`     | `Literal['TABULAR_MULTI_COLUMN', 'TABULAR_SINGLE_COLUMN', 'GRID_CURRENT_PAGE', 'AUDIT_LOG', 'TABULAR_ALL_LINE_ITEMS', 'TABULAR_CURRENT_LINE_ITEM']` | The type of this export.                                              | *required*                   |
| `format`   | `str`                                                                                                                                               | The format of this export.                                            | *required*                   |
| `encoding` | \`str                                                                                                                                               | None\`                                                                | The encoding of this export. |
| `layout`   | `Literal['TABULAR_MULTI_COLUMN', 'TABULAR_SINGLE_COLUMN', 'GRID_CURRENT_PAGE', 'AUDIT_LOG', 'TABULAR_ALL_LINE_ITEMS', 'TABULAR_CURRENT_LINE_ITEM']` | The layout of this export, representing the Anaplan Export Structure. | *required*                   |

## DeletionFailure

Parameters:

| Name       | Type  | Description                                               | Default    |
| ---------- | ----- | --------------------------------------------------------- | ---------- |
| `model_id` | `str` | The unique identifier of the model that failed to delete. | *required* |
| `message`  | `str` | The error message explaining why the deletion failed.     | *required* |

## ModelDeletionResult

Parameters:

| Name             | Type                    | Description                                                     | Default    |
| ---------------- | ----------------------- | --------------------------------------------------------------- | ---------- |
| `models_deleted` | `int`                   | The number of models that were successfully deleted.            | *required* |
| `failures`       | `list[DeletionFailure]` | List of models that failed to delete with their error messages. | `[]`       |
