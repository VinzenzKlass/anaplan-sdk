## Revision

Parameters:

| Name              | Type  | Description                                                  | Default                                               |
| ----------------- | ----- | ------------------------------------------------------------ | ----------------------------------------------------- |
| `id`              | `str` | The unique identifier of this revision.                      | *required*                                            |
| `name`            | `str` | The name of this revision.                                   | *required*                                            |
| `description`     | \`str | None\`                                                       | The description of this revision. Not always present. |
| `created_on`      | `str` | The creation date of this revision in ISO format.            | *required*                                            |
| `created_by`      | `str` | The unique identifier of the user who created this revision. | *required*                                            |
| `creation_method` | `str` | The creation method of this revision.                        | *required*                                            |
| `applied_on`      | `str` | The application date of this revision in ISO format.         | *required*                                            |
| `applied_by`      | `str` | The unique identifier of the user who applied this revision. | *required*                                            |

## ModelRevision

Parameters:

| Name             | Type   | Description                                                                                                                                                                    | Default                                                          |
| ---------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------- |
| `id`             | `str`  | The unique identifier of the model this revision belongs to.                                                                                                                   | *required*                                                       |
| `name`           | `str`  | The name of the model this revision belongs to. This can be an empty string, when the calling user does not have access to the model, but is workspace admin in the workspace. | `''`                                                             |
| `workspace_id`   | \`str  | None\`                                                                                                                                                                         | The unique identifier of the workspace this revision belongs to. |
| `applied_by`     | `str`  | The unique identifier of the user who applied this revision.                                                                                                                   | *required*                                                       |
| `applied_on`     | `str`  | The application date of this revision in ISO format.                                                                                                                           | *required*                                                       |
| `applied_method` | `str`  | The application method of this revision.                                                                                                                                       | *required*                                                       |
| `deleted`        | \`bool | None\`                                                                                                                                                                         | Whether the model has been deleted or not.                       |

## SummaryTotals

Parameters:

| Name       | Type  | Description                   | Default |
| ---------- | ----- | ----------------------------- | ------- |
| `modified` | `int` | The number of modified items. | `0`     |
| `deleted`  | `int` | The number of deleted items.  | `0`     |
| `created`  | `int` | The number of created items.  | `0`     |

## SummaryDifferences

Parameters:

| Name             | Type            | Description                | Default                                           |
| ---------------- | --------------- | -------------------------- | ------------------------------------------------- |
| `line_items`     | `SummaryTotals` | Changes in line items.     | `SummaryTotals(modified=0, deleted=0, created=0)` |
| `roles_contents` | `SummaryTotals` | Changes in roles contents. | `SummaryTotals(modified=0, deleted=0, created=0)` |
| `lists`          | `SummaryTotals` | Changes in lists.          | `SummaryTotals(modified=0, deleted=0, created=0)` |
| `modules`        | `SummaryTotals` | Changes in modules.        | `SummaryTotals(modified=0, deleted=0, created=0)` |

## SummaryReport

Parameters:

| Name                 | Type                 | Description                                    | Default    |
| -------------------- | -------------------- | ---------------------------------------------- | ---------- |
| `target_revision_id` | `str`                | The ID of the target revision.                 | *required* |
| `source_revision_id` | `str`                | The ID of the source revision.                 | *required* |
| `totals`             | `SummaryTotals`      | The total counts of changes.                   | *required* |
| `differences`        | `SummaryDifferences` | The detailed breakdown of changes by category. | *required* |
