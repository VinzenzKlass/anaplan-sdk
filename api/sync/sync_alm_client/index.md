Note

This Class is not meant to be instantiated directly, but rather accessed through the `alm` Property on an instance of [Client](https://vinzenzklass.github.io/anaplan-sdk/api/sync/sync_client/index.md). For more details, see the [Guide](https://vinzenzklass.github.io/anaplan-sdk/guides/alm/index.md).

## change_model_status

```
change_model_status(status: Literal['online', 'offline']) -> None
```

Use this call to change the status of a model.

Parameters:

| Name     | Type                           | Description                                                   | Default    |
| -------- | ------------------------------ | ------------------------------------------------------------- | ---------- |
| `status` | `Literal['online', 'offline']` | The status of the model. Can be either "online" or "offline". | *required* |

## get_revisions

```
get_revisions(
    sort_by: Literal["id", "name", "applied_on", "created_on"] | None = None,
    descending: bool = False,
) -> list[Revision]
```

Use this call to return a list of revisions for a specific model.

Parameters:

| Name         | Type                                                | Description                                              | Default                           |
| ------------ | --------------------------------------------------- | -------------------------------------------------------- | --------------------------------- |
| `sort_by`    | \`Literal['id', 'name', 'applied_on', 'created_on'] | None\`                                                   | The field to sort the results by. |
| `descending` | `bool`                                              | If True, the results will be sorted in descending order. | `False`                           |

Returns:

| Type             | Description                               |
| ---------------- | ----------------------------------------- |
| `list[Revision]` | A list of revisions for a specific model. |

## get_latest_revision

```
get_latest_revision() -> Revision | None
```

Use this call to return the latest revision for a specific model. The response is in the same format as in Getting a list of syncable revisions between two models.

If a revision exists, the return list should contain one element only which is the latest revision.

Returns:

| Type       | Description |
| ---------- | ----------- |
| \`Revision | None\`      |

## get_syncable_revisions

```
get_syncable_revisions(source_model_id: str) -> list[Revision]
```

Use this call to return the list of revisions from your source model that can be synchronized to your target model.

The returned list displays in descending order, by creation date and time. This is consistent with how revisions are displayed in the user interface (UI).

Parameters:

| Name              | Type  | Description                 | Default    |
| ----------------- | ----- | --------------------------- | ---------- |
| `source_model_id` | `str` | The ID of the source model. | *required* |

Returns:

| Type             | Description                                                       |
| ---------------- | ----------------------------------------------------------------- |
| `list[Revision]` | A list of revisions that can be synchronized to the target model. |

## create_revision

```
create_revision(name: str, description: str) -> Revision
```

Create a new revision for the model.

Parameters:

| Name          | Type  | Description                       | Default    |
| ------------- | ----- | --------------------------------- | ---------- |
| `name`        | `str` | The name (title) of the revision. | *required* |
| `description` | `str` | The description of the revision.  | *required* |

Returns:

| Type       | Description                |
| ---------- | -------------------------- |
| `Revision` | The created Revision Info. |

## get_sync_tasks

```
get_sync_tasks() -> list[TaskSummary]
```

List the sync tasks for a target mode. The returned the tasks are either in progress, or they completed within the last 48 hours.

Returns:

| Type                | Description                                                |
| ------------------- | ---------------------------------------------------------- |
| `list[TaskSummary]` | A list of sync tasks in descending order of creation time. |

## get_sync_task

```
get_sync_task(task_id: str) -> SyncTask
```

Get the information for a specific sync task.

Parameters:

| Name      | Type  | Description              | Default    |
| --------- | ----- | ------------------------ | ---------- |
| `task_id` | `str` | The ID of the sync task. | *required* |

Returns:

| Type       | Description                |
| ---------- | -------------------------- |
| `SyncTask` | The sync task information. |

## sync_models

```
sync_models(
    source_revision_id: str,
    source_model_id: str,
    target_revision_id: str,
    wait_for_completion: Literal[True] = True,
) -> CompletedSyncTask
```

```
sync_models(
    source_revision_id: str,
    source_model_id: str,
    target_revision_id: str,
    wait_for_completion: Literal[False] = False,
) -> PendingTask
```

```
sync_models(
    source_revision_id: str,
    source_model_id: str,
    target_revision_id: str,
    wait_for_completion: bool = True,
) -> SyncTask
```

Create a synchronization task between two revisions. This will synchronize the source revision of the source model to the target revision of the target model. This will fail if the source revision is incompatible with the target revision.

Parameters:

| Name                  | Type   | Description                                                                                                                                       | Default    |
| --------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| `source_revision_id`  | `str`  | The ID of the source revision.                                                                                                                    | *required* |
| `source_model_id`     | `str`  | The ID of the source model.                                                                                                                       | *required* |
| `target_revision_id`  | `str`  | The ID of the target revision.                                                                                                                    | *required* |
| `wait_for_completion` | `bool` | If True, the method will poll the task status and not return until the task is complete. If False, it will spawn the task and return immediately. | `True`     |

Returns:

| Type       | Description            |
| ---------- | ---------------------- |
| `SyncTask` | The created sync task. |

## get_models_for_revision

```
get_models_for_revision(revision_id: str) -> list[ModelRevision]
```

Use this call when you need a list of the models that had a specific revision applied to them.

Parameters:

| Name          | Type  | Description             | Default    |
| ------------- | ----- | ----------------------- | ---------- |
| `revision_id` | `str` | The ID of the revision. | *required* |

Returns:

| Type                  | Description                                                    |
| --------------------- | -------------------------------------------------------------- |
| `list[ModelRevision]` | A list of models that had a specific revision applied to them. |

## create_comparison_report

```
create_comparison_report(
    source_revision_id: str,
    source_model_id: str,
    target_revision_id: str,
    wait_for_completion: Literal[True] = True,
) -> CompletedReportTask
```

```
create_comparison_report(
    source_revision_id: str,
    source_model_id: str,
    target_revision_id: str,
    wait_for_completion: Literal[False] = False,
) -> PendingTask
```

```
create_comparison_report(
    source_revision_id: str,
    source_model_id: str,
    target_revision_id: str,
    wait_for_completion: bool = True,
) -> ReportTask
```

Generate a full comparison report between two revisions. This will list all the changes made to the source revision compared to the target revision.

Parameters:

| Name                  | Type   | Description                                                                                                                                       | Default    |
| --------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| `source_revision_id`  | `str`  | The ID of the source revision.                                                                                                                    | *required* |
| `source_model_id`     | `str`  | The ID of the source model.                                                                                                                       | *required* |
| `target_revision_id`  | `str`  | The ID of the target revision.                                                                                                                    | *required* |
| `wait_for_completion` | `bool` | If True, the method will poll the task status and not return until the task is complete. If False, it will spawn the task and return immediately. | `True`     |

Returns:

| Type         | Description                      |
| ------------ | -------------------------------- |
| `ReportTask` | The created report task summary. |

## get_comparison_report_task

```
get_comparison_report_task(task_id: str) -> ReportTask
```

Get the task information for a comparison report task.

Parameters:

| Name      | Type  | Description                           | Default    |
| --------- | ----- | ------------------------------------- | ---------- |
| `task_id` | `str` | The ID of the comparison report task. | *required* |

Returns:

| Type         | Description                  |
| ------------ | ---------------------------- |
| `ReportTask` | The report task information. |

## get_comparison_report

```
get_comparison_report(task: ReportTask) -> bytes
```

Get the report for a specific task.

Parameters:

| Name   | Type         | Description                                    | Default    |
| ------ | ------------ | ---------------------------------------------- | ---------- |
| `task` | `ReportTask` | The report task object containing the task ID. | *required* |

Returns:

| Type    | Description                                  |
| ------- | -------------------------------------------- |
| `bytes` | The binary content of the comparison report. |

## create_comparison_summary

```
create_comparison_summary(
    source_revision_id: str,
    source_model_id: str,
    target_revision_id: str,
    wait_for_completion: Literal[True] = True,
) -> SummaryReport
```

```
create_comparison_summary(
    source_revision_id: str,
    source_model_id: str,
    target_revision_id: str,
    wait_for_completion: Literal[False] = False,
) -> ReportTask
```

```
create_comparison_summary(
    source_revision_id: str,
    source_model_id: str,
    target_revision_id: str,
    wait_for_completion: bool = True,
) -> ReportTask | SummaryReport
```

Generate a comparison summary between two revisions.

Parameters:

| Name                  | Type   | Description                                                                                                                                       | Default    |
| --------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| `source_revision_id`  | `str`  | The ID of the source revision.                                                                                                                    | *required* |
| `source_model_id`     | `str`  | The ID of the source model.                                                                                                                       | *required* |
| `target_revision_id`  | `str`  | The ID of the target revision.                                                                                                                    | *required* |
| `wait_for_completion` | `bool` | If True, the method will poll the task status and not return until the task is complete. If False, it will spawn the task and return immediately. | `True`     |

Returns:

| Type         | Description     |
| ------------ | --------------- |
| \`ReportTask | SummaryReport\` |

## get_comparison_summary_task

```
get_comparison_summary_task(task_id: str) -> ReportTask
```

Get the task information for a comparison summary task.

Parameters:

| Name      | Type  | Description                            | Default    |
| --------- | ----- | -------------------------------------- | ---------- |
| `task_id` | `str` | The ID of the comparison summary task. | *required* |

Returns:

| Type         | Description                  |
| ------------ | ---------------------------- |
| `ReportTask` | The report task information. |

## get_comparison_summary

```
get_comparison_summary(task: ReportTask) -> SummaryReport
```

Get the comparison summary for a specific task.

Parameters:

| Name   | Type         | Description                                     | Default    |
| ------ | ------------ | ----------------------------------------------- | ---------- |
| `task` | `ReportTask` | The summary task object containing the task ID. | *required* |

Returns:

| Type            | Description                                   |
| --------------- | --------------------------------------------- |
| `SummaryReport` | The binary content of the comparison summary. |
