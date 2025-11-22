## TaskResultDetail

Parameters:

| Name                 | Type                  | Description                              | Default             |
| -------------------- | --------------------- | ---------------------------------------- | ------------------- |
| `local_message_text` | \`str                 | None\`                                   | Error message text. |
| `occurrences`        | `int`                 | The number of occurrences of this error. | `0`                 |
| `type`               | `str`                 | The type of this error.                  | *required*          |
| `values`             | `list[Optional[str]]` | Further error information if available.  | `[]`                |

## TaskResult

Parameters:

| Name                     | Type                     | Description                                        | Default    |
| ------------------------ | ------------------------ | -------------------------------------------------- | ---------- |
| `details`                | `list[TaskResultDetail]` | The details of this task result if available.      | `[]`       |
| `successful`             | `bool`                   | Whether this task completed successfully or not.   | *required* |
| `failure_dump_available` | `bool`                   | Whether a failure dump is available for this task. | *required* |
| `nested_results`         | `list[TaskResult]`       | The nested results of this task, if available.     | `[]`       |

## TaskSummary

Parameters:

| Name            | Type                                                | Description                                   | Default    |
| --------------- | --------------------------------------------------- | --------------------------------------------- | ---------- |
| `id`            | `str`                                               | The unique identifier of this task.           | *required* |
| `task_state`    | `Literal['NOT_STARTED', 'IN_PROGRESS', 'COMPLETE']` | The state of this task.                       | *required* |
| `creation_time` | `int`                                               | Unix timestamp of when this task was created. | *required* |

## Task

Parameters:

| Name            | Type                                    | Description                                           | Default                        |
| --------------- | --------------------------------------- | ----------------------------------------------------- | ------------------------------ |
| `id`            | `str`                                   | The unique identifier of this task.                   | *required*                     |
| `task_state`    | `Literal['NOT_STARTED', 'IN_PROGRESS']` | The state of this task.                               | *required*                     |
| `creation_time` | `int`                                   | Unix timestamp of when this task was created.         | *required*                     |
| `progress`      | `float`                                 | The progress of this task as a float between 0 and 1. | *required*                     |
| `current_step`  | \`str                                   | None\`                                                | The current step of this task. |

## CompletedTask

Parameters:

| Name            | Type                  | Description                                           | Default                        |
| --------------- | --------------------- | ----------------------------------------------------- | ------------------------------ |
| `id`            | `str`                 | The unique identifier of this task.                   | *required*                     |
| `task_state`    | `Literal['COMPLETE']` | The state of this task.                               | *required*                     |
| `creation_time` | `int`                 | Unix timestamp of when this task was created.         | *required*                     |
| `progress`      | `float`               | The progress of this task as a float between 0 and 1. | *required*                     |
| `current_step`  | \`str                 | None\`                                                | The current step of this task. |
| `result`        | `TaskResult`          |                                                       | *required*                     |

## SyncTaskResult

Parameters:

| Name                 | Type   | Description                                  | Default    |
| -------------------- | ------ | -------------------------------------------- | ---------- |
| `source_revision_id` | `str`  | The ID of the source revision.               | *required* |
| `target_revision_id` | `str`  | The ID of the target revision.               | *required* |
| `successful`         | `bool` | Whether the sync task was successful or not. | *required* |

## PendingTask

Parameters:

| Name            | Type                                    | Description                                   | Default    |
| --------------- | --------------------------------------- | --------------------------------------------- | ---------- |
| `id`            | `str`                                   | The unique identifier of this task.           | *required* |
| `task_state`    | `Literal['NOT_STARTED', 'IN_PROGRESS']` | The state of this task.                       | *required* |
| `creation_time` | `int`                                   | Unix timestamp of when this task was created. | *required* |
| `current_step`  | `str`                                   | The current step of the sync task.            | *required* |

## CompletedSyncTask

Parameters:

| Name            | Type                  | Description                                   | Default    |
| --------------- | --------------------- | --------------------------------------------- | ---------- |
| `id`            | `str`                 | The unique identifier of this task.           | *required* |
| `task_state`    | `Literal['COMPLETE']` | The state of this task.                       | *required* |
| `creation_time` | `int`                 | Unix timestamp of when this task was created. | *required* |
| `current_step`  | `str`                 | The current step of the sync task.            | *required* |
| `result`        | `SyncTaskResult`      |                                               | *required* |

## ReportTaskResult

Parameters:

| Name                 | Type            | Description                                            | Default    |
| -------------------- | --------------- | ------------------------------------------------------ | ---------- |
| `source_revision_id` | `str`           | The ID of the source revision.                         | *required* |
| `target_revision_id` | `str`           | The ID of the target revision.                         | *required* |
| `successful`         | `Literal[True]` | Whether the sync task was successful or not.           | *required* |
| `report_file_url`    | `str`           | The URL of the report file generated by the sync task. | *required* |

## ReportTaskError

Parameters:

| Name      | Type  | Description               | Default    |
| --------- | ----- | ------------------------- | ---------- |
| `title`   | `str` | The title of the error.   | *required* |
| `message` | `str` | The message of the error. | *required* |

## ReportTaskFailureResult

Parameters:

| Name                 | Type              | Description                                   | Default    |
| -------------------- | ----------------- | --------------------------------------------- | ---------- |
| `source_revision_id` | `str`             | The ID of the source revision.                | *required* |
| `target_revision_id` | `str`             | The ID of the target revision.                | *required* |
| `successful`         | `Literal[False]`  | Whether the sync task was successful or not.  | *required* |
| `error`              | `ReportTaskError` | The error that occurred during the sync task. | *required* |

## CompletedReportTask

Parameters:

| Name            | Type                  | Description                                   | Default    |
| --------------- | --------------------- | --------------------------------------------- | ---------- |
| `id`            | `str`                 | The unique identifier of this task.           | *required* |
| `task_state`    | `Literal['COMPLETE']` | The state of this task.                       | *required* |
| `creation_time` | `int`                 | Unix timestamp of when this task was created. | *required* |
| `current_step`  | `str`                 | The current step of the sync task.            | *required* |
| `result`        | \`ReportTaskResult    | ReportTaskFailureResult\`                     |            |
