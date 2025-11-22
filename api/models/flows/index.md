## FlowSummary

Parameters:

| Name                | Type        | Description                                                                    | Default                                                      |
| ------------------- | ----------- | ------------------------------------------------------------------------------ | ------------------------------------------------------------ |
| `creation_date`     | `datetime`  | The initial creation date.                                                     | *required*                                                   |
| `modification_date` | `datetime`  | The last modification date. If never modified, this is equal to creation_date. | *required*                                                   |
| `created_by`        | `str`       | The user who created this integration.                                         | *required*                                                   |
| `modified_by`       | \`str       | None\`                                                                         | The user who last modified this.                             |
| `name`              | `str`       | The name of this integration.                                                  | *required*                                                   |
| `notification_id`   | \`str       | None\`                                                                         | The ID of the associated notification configuration, if any. |
| `latest_run`        | \`LatestRun | None\`                                                                         | Details about the latest execution, if any.                  |
| `id`                | `str`       | The unique identifier of this flow.                                            | *required*                                                   |
| `steps_count`       | `int`       | The number of steps in this flow.                                              | *required*                                                   |

## ExceptionBehavior

Parameters:

| Name       | Type                                    | Description                                          | Default    |
| ---------- | --------------------------------------- | ---------------------------------------------------- | ---------- |
| `type`     | `Literal['failure', 'partial_success']` | The type of exception that this behavior applies to. | *required* |
| `strategy` | `Literal['stop', 'continue']`           | The strategy to handle the exception.                | *required* |

## FlowStep

Parameters:

| Name                 | Type                                     | Description                                                  | Default                                     |
| -------------------- | ---------------------------------------- | ------------------------------------------------------------ | ------------------------------------------- |
| `referrer`           | `str`                                    | The unique identifier of the referenced step or integration. | *required*                                  |
| `name`               | `str`                                    | The name of this flow step.                                  | *required*                                  |
| `type`               | `Literal['Process', 'Import', 'Export']` | The type of this flow step.                                  | *required*                                  |
| `created_by`         | `str`                                    | The user who created this step.                              | *required*                                  |
| `created_date`       | `datetime`                               | The initial creation date of this step.                      | *required*                                  |
| `modified_date`      | `datetime`                               | The last modification date of this step.                     | *required*                                  |
| `modified_by`        | \`str                                    | None\`                                                       | The user who last modified this step.       |
| `model_id`           | `str`                                    | The ID of the model this step belongs to.                    | *required*                                  |
| `workspace_id`       | `str`                                    | The ID of the workspace this step belongs to.                | *required*                                  |
| `depends_on`         | \`list[str]                              | None\`                                                       | The IDs of steps that this step depends on. |
| `is_skipped`         | `bool`                                   | Whether this step is skipped during execution.               | *required*                                  |
| `exception_behavior` | `list[ExceptionBehavior]`                | Configuration for handling exceptions during step execution. | *required*                                  |

## Flow

Parameters:

| Name                | Type             | Description                                                                    | Default                                                      |
| ------------------- | ---------------- | ------------------------------------------------------------------------------ | ------------------------------------------------------------ |
| `creation_date`     | `datetime`       | The initial creation date.                                                     | *required*                                                   |
| `modification_date` | `datetime`       | The last modification date. If never modified, this is equal to creation_date. | *required*                                                   |
| `created_by`        | `str`            | The user who created this integration.                                         | *required*                                                   |
| `modified_by`       | \`str            | None\`                                                                         | The user who last modified this.                             |
| `name`              | `str`            | The name of this integration.                                                  | *required*                                                   |
| `notification_id`   | \`str            | None\`                                                                         | The ID of the associated notification configuration, if any. |
| `latest_run`        | \`LatestRun      | None\`                                                                         | Details about the latest execution, if any.                  |
| `id`                | `str`            | The unique identifier of this flow.                                            | *required*                                                   |
| `steps_count`       | `int`            | The number of steps in this flow.                                              | *required*                                                   |
| `version`           | `Literal['2.0']` | The version of this flow.                                                      | `'2.0'`                                                      |
| `nux_visible`       | `bool`           | Whether this integration is visible in the UI.                                 | *required*                                                   |
| `steps`             | `list[FlowStep]` | The steps in this flow.                                                        | `[]`                                                         |

## FlowStepInput

Parameters:

| Name                 | Type                      | Description                                                                                                                     | Default                                                                                                                |
| -------------------- | ------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `type`               | `Literal['Integration']`  | The type of this flow step.                                                                                                     | `'Integration'`                                                                                                        |
| `referrer`           | `str`                     | The unique identifier of the referenced step or integration.                                                                    | *required*                                                                                                             |
| `depends_on`         | \`list[str]               | None\`                                                                                                                          | The IDs of steps that this step depends on.                                                                            |
| `is_skipped`         | `bool`                    | Whether this step is skipped during execution.                                                                                  | `False`                                                                                                                |
| `exception_behavior` | `list[ExceptionBehavior]` | Configuration for handling exceptions during step execution. Defaults to stopping on Failure and continuing on Partial Success. | `[ExceptionBehavior(type='failure', strategy='stop'), ExceptionBehavior(type='partial_success', strategy='continue')]` |

## FlowInput

Parameters:

| Name      | Type                         | Description               | Default             |
| --------- | ---------------------------- | ------------------------- | ------------------- |
| `name`    | `str`                        | The name of this flow.    | *required*          |
| `version` | `Literal['2.0']`             | The version of this flow. | `'2.0'`             |
| `type`    | `Literal['IntegrationFlow']` | The type of this flow.    | `'IntegrationFlow'` |
| `steps`   | `list[FlowStepInput]`        | The steps in this flow.   | *required*          |
