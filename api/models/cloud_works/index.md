## BaseConnectionInput

Parameters:

| Name           | Type  | Description | Default                                                                                                 |
| -------------- | ----- | ----------- | ------------------------------------------------------------------------------------------------------- |
| `workspace_id` | \`str | None\`      | If you are a restricted integration user, add the Workspace ID to which you have access in the payload. |

## AzureBlobConnectionInfo

Parameters:

| Name                   | Type  | Description                            | Default    |
| ---------------------- | ----- | -------------------------------------- | ---------- |
| `name`                 | `str` | The name of the Azure Blob connection. | *required* |
| `storage_account_name` | `str` | The name of the Azure Storage account. | *required* |
| `container_name`       | `str` | The name of the Azure Blob container.  | *required* |

## AzureBlobConnectionInput

Parameters:

| Name                   | Type  | Description                                                                                                                                                        | Default                                                                                                 |
| ---------------------- | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------- |
| `workspace_id`         | \`str | None\`                                                                                                                                                             | If you are a restricted integration user, add the Workspace ID to which you have access in the payload. |
| `name`                 | `str` | The name of the Azure Blob connection.                                                                                                                             | *required*                                                                                              |
| `storage_account_name` | `str` | The name of the Azure Storage account.                                                                                                                             | *required*                                                                                              |
| `container_name`       | `str` | The name of the Azure Blob container.                                                                                                                              | *required*                                                                                              |
| `sas_token`            | `str` | The SAS token for the Azure Blob connection. Must be created on the container directly and not on any child blobs and have at least 'Read' and 'List' permissions. | *required*                                                                                              |

## AmazonS3ConnectionInfo

Parameters:

| Name          | Type  | Description                           | Default    |
| ------------- | ----- | ------------------------------------- | ---------- |
| `name`        | `str` | The name of the Amazon S3 connection. | *required* |
| `bucket_name` | `str` | The name of the Amazon S3 bucket.     | *required* |

## AmazonS3ConnectionInput

Parameters:

| Name                | Type  | Description                                         | Default                                                                                                 |
| ------------------- | ----- | --------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `workspace_id`      | \`str | None\`                                              | If you are a restricted integration user, add the Workspace ID to which you have access in the payload. |
| `name`              | `str` | The name of the Amazon S3 connection.               | *required*                                                                                              |
| `bucket_name`       | `str` | The name of the Amazon S3 bucket.                   | *required*                                                                                              |
| `access_key_id`     | `str` | The access key ID for the Amazon S3 connection.     | *required*                                                                                              |
| `secret_access_key` | `str` | The secret access key for the Amazon S3 connection. | *required*                                                                                              |

## GoogleBigQueryConnectionInfo

Parameters:

| Name      | Type  | Description                                 | Default    |
| --------- | ----- | ------------------------------------------- | ---------- |
| `name`    | `str` | The name of the Google BigQuery connection. | *required* |
| `dataset` | `str` | The ID of the Google BigQuery dataset.      | *required* |

## GoogleBigQueryConnectionInput

Parameters:

| Name                   | Type             | Description                                                         | Default                                                                                                 |
| ---------------------- | ---------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `workspace_id`         | \`str            | None\`                                                              | If you are a restricted integration user, add the Workspace ID to which you have access in the payload. |
| `name`                 | `str`            | The name of the Google BigQuery connection.                         | *required*                                                                                              |
| `dataset`              | `str`            | The ID of the Google BigQuery dataset.                              | *required*                                                                                              |
| `service_account_json` | `dict[str, str]` | The entire service account JSON for the Google BigQuery connection. | *required*                                                                                              |

## ConnectionInput

Parameters:

| Name   | Type                                                 | Description                  | Default                         |
| ------ | ---------------------------------------------------- | ---------------------------- | ------------------------------- |
| `type` | `Literal['AmazonS3', 'AzureBlob', 'GoogleBigQuery']` | The type of this connection. | *required*                      |
| `body` | \`AzureBlobConnectionInput                           | AmazonS3ConnectionInput      | GoogleBigQueryConnectionInput\` |

## Connection

Parameters:

| Name                     | Type                                                 | Description                                                                                       | Default                                                     |
| ------------------------ | ---------------------------------------------------- | ------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| `creation_date`          | `datetime`                                           | The initial creation date.                                                                        | *required*                                                  |
| `modification_date`      | `datetime`                                           | The last modification date. If never modified, this is equal to creation_date.                    | *required*                                                  |
| `created_by`             | `str`                                                | The user who created this.                                                                        | *required*                                                  |
| `modified_by`            | \`str                                                | None\`                                                                                            | The user who last modified this.                            |
| `id`                     | `str`                                                | The unique identifier of this connection.                                                         | *required*                                                  |
| `connection_type`        | `Literal['AmazonS3', 'AzureBlob', 'GoogleBigQuery']` | The type of this connection.                                                                      | *required*                                                  |
| `body`                   | \`AzureBlobConnectionInfo                            | AmazonS3ConnectionInfo                                                                            | GoogleBigQueryConnectionInfo\`                              |
| `status`                 | `int`                                                | The status of this connection. 1 indicates a valid connection, 0 indicates an invalid connection. | *required*                                                  |
| `integration_error_code` | \`str                                                | None\`                                                                                            | The error code of the connection, if any.                   |
| `workspace_id`           | \`str                                                | None\`                                                                                            | The workspace that was given when creating this connection. |

## LatestRun

Parameters:

| Name                   | Type       | Description                      | Default                                                                                   |
| ---------------------- | ---------- | -------------------------------- | ----------------------------------------------------------------------------------------- |
| `triggered_by`         | `str`      | The user who triggered this run. | *required*                                                                                |
| `start_date`           | `datetime` | The start timestamp of this run. | *required*                                                                                |
| `end_date`             | \`datetime | None\`                           | The end timestamp of this run. This can be None, if the integration is currently running. |
| `success`              | `bool`     | Whether this run was successful. | *required*                                                                                |
| `message`              | `str`      | Result message of this run.      | *required*                                                                                |
| `execution_error_code` | \`int      | None\`                           | Error code if run failed.                                                                 |
| `trigger_source`       | \`str      | None\`                           | Source that triggered the run.                                                            |

## ScheduleBase

Parameters:

| Name       | Type                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | Description                | Default    |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------- | ---------- |
| `name`     | `str`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Name of the schedule.      | *required* |
| `type`     | `Literal['hourly', 'daily', 'weekly', 'monthly_specific_day', 'monthly_relative_weekday']`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Trigger Frequency          | *required* |
| `timezone` | `Literal['Etc/GMT+12', 'US/Samoa', 'Pacific/Honolulu', 'Pacific/Marquesas', 'US/Aleutian', 'America/Anchorage', 'America/Los_Angeles', 'America/Denver', 'America/Chicago', 'America/New_York', 'America/Sao_Paulo', 'Canada/Newfoundland', 'America/Nuuk', 'Atlantic/Cape_Verde', 'Greenwich', 'Europe/London', 'Europe/Paris', 'Asia/Tel_Aviv', 'Europe/Moscow', 'Asia/Dubai', 'Asia/Kabul', 'Asia/Karachi', 'Asia/Kolkata', 'Asia/Kathmandu', 'Asia/Dhaka', 'Asia/Rangoon', 'Asia/Jakarta', 'Asia/Hong_Kong', 'Australia/Eucla', 'Asia/Tokyo', 'Australia/Adelaide', 'Australia/Brisbane', 'Australia/Melbourne', 'Australia/Perth', 'Australia/Lord_Howe', 'Pacific/Norfolk', 'Pacific/Auckland', 'Pacific/Chatham']` | Timezone for the schedule. | *required* |

## ScheduleInput

Parameters:

| Name           | Type                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | Description                                                                                                                                                 | Default                                                                                                                                                                                                                    |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`         | `str`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Name of the schedule.                                                                                                                                       | *required*                                                                                                                                                                                                                 |
| `type`         | `Literal['hourly', 'daily', 'weekly', 'monthly_specific_day', 'monthly_relative_weekday']`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Trigger Frequency                                                                                                                                           | *required*                                                                                                                                                                                                                 |
| `timezone`     | `Literal['Etc/GMT+12', 'US/Samoa', 'Pacific/Honolulu', 'Pacific/Marquesas', 'US/Aleutian', 'America/Anchorage', 'America/Los_Angeles', 'America/Denver', 'America/Chicago', 'America/New_York', 'America/Sao_Paulo', 'Canada/Newfoundland', 'America/Nuuk', 'Atlantic/Cape_Verde', 'Greenwich', 'Europe/London', 'Europe/Paris', 'Asia/Tel_Aviv', 'Europe/Moscow', 'Asia/Dubai', 'Asia/Kabul', 'Asia/Karachi', 'Asia/Kolkata', 'Asia/Kathmandu', 'Asia/Dhaka', 'Asia/Rangoon', 'Asia/Jakarta', 'Asia/Hong_Kong', 'Australia/Eucla', 'Asia/Tokyo', 'Australia/Adelaide', 'Australia/Brisbane', 'Australia/Melbourne', 'Australia/Perth', 'Australia/Lord_Howe', 'Pacific/Norfolk', 'Pacific/Auckland', 'Pacific/Chatham']` | Timezone for the schedule.                                                                                                                                  | *required*                                                                                                                                                                                                                 |
| `time`         | \`str                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | None\`                                                                                                                                                      | Time for scheduled runs in HH:mm format.                                                                                                                                                                                   |
| `from_time`    | \`str                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | None\`                                                                                                                                                      | Time for scheduled runs in HH:mm format, if type is hourly.                                                                                                                                                                |
| `to_time`      | \`str                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | None\`                                                                                                                                                      | Time for scheduled runs in HH:mm format, if type is hourly.                                                                                                                                                                |
| `days_of_week` | `list[int]`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Days of week when schedule is active.                                                                                                                       | *required*                                                                                                                                                                                                                 |
| `start_date`   | `str`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Start date for the schedule in YYYY-MM-DD format. Must be in the Future, i.e. current day, if the time is greater than the current time or any future date. | *required*                                                                                                                                                                                                                 |
| `end_date`     | \`str                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | None\`                                                                                                                                                      | End date for the schedule in YYYY-MM-DD format. Must be in the Future, i.e. current day, if the time is greater than the current time or any future date. Can also be omitted to create a schedule that runs indefinitely. |

## Schedule

Parameters:

| Name           | Type                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | Description                           | Default                                  |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------- | ---------------------------------------- |
| `name`         | `str`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Name of the schedule.                 | *required*                               |
| `type`         | `Literal['hourly', 'daily', 'weekly', 'monthly_specific_day', 'monthly_relative_weekday']`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Trigger Frequency                     | *required*                               |
| `timezone`     | `Literal['Etc/GMT+12', 'US/Samoa', 'Pacific/Honolulu', 'Pacific/Marquesas', 'US/Aleutian', 'America/Anchorage', 'America/Los_Angeles', 'America/Denver', 'America/Chicago', 'America/New_York', 'America/Sao_Paulo', 'Canada/Newfoundland', 'America/Nuuk', 'Atlantic/Cape_Verde', 'Greenwich', 'Europe/London', 'Europe/Paris', 'Asia/Tel_Aviv', 'Europe/Moscow', 'Asia/Dubai', 'Asia/Kabul', 'Asia/Karachi', 'Asia/Kolkata', 'Asia/Kathmandu', 'Asia/Dhaka', 'Asia/Rangoon', 'Asia/Jakarta', 'Asia/Hong_Kong', 'Australia/Eucla', 'Asia/Tokyo', 'Australia/Adelaide', 'Australia/Brisbane', 'Australia/Melbourne', 'Australia/Perth', 'Australia/Lord_Howe', 'Pacific/Norfolk', 'Pacific/Auckland', 'Pacific/Chatham']` | Timezone for the schedule.            | *required*                               |
| `time`         | \`str                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | None\`                                | Time for scheduled runs in HH:mm format. |
| `to_time`      | \`str                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | None\`                                | End time for scheduled runs.             |
| `from_time`    | \`str                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | None\`                                | Start time for scheduled runs.           |
| `start_date`   | `datetime`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Start date of the schedule.           | *required*                               |
| `end_date`     | \`datetime                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | None\`                                | End date of the schedule, if set.        |
| `days_of_week` | `list[int]`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Days of week when schedule is active. | `[]`                                     |
| `repeat_every` | \`int                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | None\`                                | Frequency of repetition.                 |
| `status`       | `str`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Current status of the schedule.       | *required*                               |

## Integration

Parameters:

| Name                | Type                                     | Description                                                                    | Default                                                      |
| ------------------- | ---------------------------------------- | ------------------------------------------------------------------------------ | ------------------------------------------------------------ |
| `creation_date`     | `datetime`                               | The initial creation date.                                                     | *required*                                                   |
| `modification_date` | `datetime`                               | The last modification date. If never modified, this is equal to creation_date. | *required*                                                   |
| `created_by`        | `str`                                    | The user who created this integration.                                         | *required*                                                   |
| `modified_by`       | \`str                                    | None\`                                                                         | The user who last modified this.                             |
| `name`              | `str`                                    | The name of this integration.                                                  | *required*                                                   |
| `notification_id`   | \`str                                    | None\`                                                                         | The ID of the associated notification configuration, if any. |
| `latest_run`        | \`LatestRun                              | None\`                                                                         | Details about the latest execution, if any.                  |
| `id`                | `str`                                    | The unique identifier of this integration.                                     | *required*                                                   |
| `integration_type`  | `Literal['Import', 'Export', 'Process']` | The type of this integration.                                                  | *required*                                                   |
| `model_id`          | `str`                                    | The ID of the model this integration belongs to.                               | *required*                                                   |
| `workspace_id`      | `str`                                    | The ID of the workspace this integration belongs to.                           | *required*                                                   |
| `nux_visible`       | `bool`                                   | Whether this integration is visible in the UI.                                 | *required*                                                   |
| `process_id`        | \`int                                    | None\`                                                                         | The ID of the process (for Process type).                    |
| `schedule`          | \`Schedule                               | None\`                                                                         | Schedule configuration if defined.                           |

## AnaplanSource

Parameters:

| Name        | Type                 | Description                                                                    | Default     |
| ----------- | -------------------- | ------------------------------------------------------------------------------ | ----------- |
| `type`      | `Literal['Anaplan']` | Literal signifying this is an Anaplan source.                                  | `'Anaplan'` |
| `action_id` | `int`                | The ID of the action to be used as a source. This can be a process, or export. | *required*  |

## FileSourceInput

Parameters:

| Name            | Type                               | Description                                           | Default    |
| --------------- | ---------------------------------- | ----------------------------------------------------- | ---------- |
| `connection_id` | `str`                              | The unique identifier of the connection.              | *required* |
| `type`          | `Literal['AmazonS3', 'AzureBlob']` | The type of this connection.                          | *required* |
| `file`          | `str`                              | The file path relative to the root of the connection. | *required* |

## FileSource

Parameters:

| Name                    | Type                               | Description                                           | Default                                |
| ----------------------- | ---------------------------------- | ----------------------------------------------------- | -------------------------------------- |
| `connection_id`         | `str`                              | The unique identifier of the connection.              | *required*                             |
| `type`                  | `Literal['AmazonS3', 'AzureBlob']` | The type of this connection.                          | *required*                             |
| `file`                  | `str`                              | The file path relative to the root of the connection. | *required*                             |
| `connection_name`       | `str`                              | The name of the connection.                           | *required*                             |
| `is_connection_deleted` | `bool`                             | Whether the connection has been deleted.              | *required*                             |
| `bucket_name`           | \`str                              | None\`                                                | The name of the bucket, if applicable. |

## TableSource

Parameters:

| Name            | Type                        | Description                                               | Default            |
| --------------- | --------------------------- | --------------------------------------------------------- | ------------------ |
| `type`          | `Literal['GoogleBigQuery']` | The type of this connection.                              | `'GoogleBigQuery'` |
| `connection_id` | `str`                       | The unique identifier of the connection.                  | *required*         |
| `table`         | `str`                       | The table name in the BigQuery dataset in the connection. | *required*         |

## FileTarget

Parameters:

| Name            | Type                               | Description                                           | Default    |
| --------------- | ---------------------------------- | ----------------------------------------------------- | ---------- |
| `connection_id` | `str`                              | The unique identifier of the connection.              | *required* |
| `type`          | `Literal['AmazonS3', 'AzureBlob']` | The type of this connection.                          | *required* |
| `file`          | `str`                              | The file path relative to the root of the connection. | *required* |
| `overwrite`     | `bool`                             | Whether to overwrite the file if it exists.           | `True`     |

## TableTarget

Parameters:

| Name            | Type                        | Description                                               | Default            |
| --------------- | --------------------------- | --------------------------------------------------------- | ------------------ |
| `type`          | `Literal['GoogleBigQuery']` | The type of this connection.                              | `'GoogleBigQuery'` |
| `connection_id` | `str`                       | The unique identifier of the connection.                  | *required*         |
| `table`         | `str`                       | The table name in the BigQuery dataset in the connection. | *required*         |
| `overwrite`     | `bool`                      | Whether to overwrite the table if it exists.              | `False`            |

## AnaplanTarget

Parameters:

| Name        | Type                 | Description                                                                    | Default     |
| ----------- | -------------------- | ------------------------------------------------------------------------------ | ----------- |
| `type`      | `Literal['Anaplan']` | Literal signifying this is an Anaplan target.                                  | `'Anaplan'` |
| `action_id` | `int`                | The ID of the action to be used as a target. This can be a process, or import. | *required*  |
| `file_id`   | `int`                | The ID of the file to be used as a target.                                     | *required*  |

## IntegrationJob

Parameters:

| Name      | Type                                                                                                                                                  | Description                   | Default    |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- | ---------- |
| `type`    | `Literal['AmazonS3ToAnaplan', 'AzureBlobToAnaplan', 'GoogleBigQueryToAnaplan', 'AnaplanToAmazonS3', 'AnaplanToAzureBlob', 'AnaplanToGoogleBigQuery']` | The type of this integration. | *required* |
| `sources` | `list[Union[AnaplanSource, FileSource, TableSource]]`                                                                                                 | The source of this job.       | *required* |
| `targets` | `list[Union[AnaplanTarget, FileTarget, TableTarget]]`                                                                                                 | The target of this job.       | *required* |

## SingleIntegration

Parameters:

| Name                | Type                   | Description                                                                                                                        | Default                                                                                                                  |
| ------------------- | ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `creation_date`     | `datetime`             | The initial creation date.                                                                                                         | *required*                                                                                                               |
| `modification_date` | `datetime`             | The last modification date. If never modified, this is equal to creation_date.                                                     | *required*                                                                                                               |
| `created_by`        | `str`                  | The user who created this integration.                                                                                             | *required*                                                                                                               |
| `modified_by`       | \`str                  | None\`                                                                                                                             | The user who last modified this.                                                                                         |
| `name`              | `str`                  | The name of this integration.                                                                                                      | *required*                                                                                                               |
| `notification_id`   | \`str                  | None\`                                                                                                                             | The ID of the associated notification configuration, if any.                                                             |
| `latest_run`        | \`LatestRun            | None\`                                                                                                                             | Details about the latest execution, if any.                                                                              |
| `id`                | `str`                  | The unique identifier of this integration.                                                                                         | *required*                                                                                                               |
| `integration_type`  | `None`                 | Sentinel for erroneous implementation of the Anaplan API. This field is not provided when getting an individual integration by Id. | `None`                                                                                                                   |
| `model_id`          | `str`                  | The ID of the model this integration belongs to.                                                                                   | *required*                                                                                                               |
| `workspace_id`      | `str`                  | The ID of the workspace this integration belongs to.                                                                               | *required*                                                                                                               |
| `nux_visible`       | `bool`                 | Whether this integration is visible in the UI.                                                                                     | *required*                                                                                                               |
| `process_id`        | \`int                  | None\`                                                                                                                             | The ID of the process (for Process type).                                                                                |
| `schedule`          | \`Schedule             | None\`                                                                                                                             | Schedule configuration if defined.                                                                                       |
| `jobs`              | \`list[IntegrationJob] | None\`                                                                                                                             | The Integration Job details. The source and target can be switched according to convert imports and exports requirement. |

## IntegrationJobInput

Parameters:

| Name      | Type                                                                                                                                                  | Description                      | Default    |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------- | ---------- |
| `type`    | `Literal['AmazonS3ToAnaplan', 'AzureBlobToAnaplan', 'GoogleBigQueryToAnaplan', 'AnaplanToAmazonS3', 'AnaplanToAzureBlob', 'AnaplanToGoogleBigQuery']` | The type of this integration.    | *required* |
| `sources` | `list[Union[AnaplanSource, FileSourceInput, TableSource]]`                                                                                            | The sources of this integration. | *required* |
| `targets` | `list[Union[AnaplanTarget, FileTarget, TableTarget]]`                                                                                                 | The targets of this integration. | *required* |

## IntegrationProcessInput

Parameters:

| Name           | Type             | Description                                          | Default    |
| -------------- | ---------------- | ---------------------------------------------------- | ---------- |
| `name`         | `str`            | The name of this integration process.                | *required* |
| `version`      | `Literal['2.0']` | The version of this integration.                     | `'2.0'`    |
| `workspace_id` | `str`            | The ID of the workspace this integration belongs to. | *required* |
| `model_id`     | `str`            | The ID of the model this integration belongs to.     | *required* |
| `process_id`   | `int`            | The ID of the process this integration belongs to.   | *required* |

## IntegrationInput

Parameters:

| Name           | Type                        | Description                                          | Default                                                                          |
| -------------- | --------------------------- | ---------------------------------------------------- | -------------------------------------------------------------------------------- |
| `name`         | `str`                       | The name of this integration.                        | *required*                                                                       |
| `version`      | `Literal['2.0']`            | The version of this integration.                     | `'2.0'`                                                                          |
| `workspace_id` | `str`                       | The ID of the workspace this integration belongs to. | *required*                                                                       |
| `model_id`     | `str`                       | The ID of the model this integration belongs to.     | *required*                                                                       |
| `process_id`   | \`int                       | None\`                                               | If given, an integration process will be created, instead of an Import or Export |
| `nux_visible`  | `bool`                      | Whether this integration is visible in the UI.       | `False`                                                                          |
| `jobs`         | `list[IntegrationJobInput]` | The jobs in this integration.                        | *required*                                                                       |

## RunSummary

Parameters:

| Name                   | Type                             | Description                        | Default                                                                                   |
| ---------------------- | -------------------------------- | ---------------------------------- | ----------------------------------------------------------------------------------------- |
| `id`                   | `str`                            | The unique identifier of this run. | *required*                                                                                |
| `triggered_by`         | `str`                            |                                    | *required*                                                                                |
| `last_run`             | `datetime`                       | Last Run timestamp.                | *required*                                                                                |
| `start_date`           | `datetime`                       | Start timestamp.                   | *required*                                                                                |
| `end_date`             | \`datetime                       | None\`                             | The end timestamp of this run. This can be None, if the integration is currently running. |
| `success`              | `bool`                           | Whether this run was successful.   | *required*                                                                                |
| `message`              | `str`                            | Result message of this run.        | *required*                                                                                |
| `execution_error_code` | \`int                            | None\`                             | Error code if run failed.                                                                 |
| `trace_id`             | `str`                            | The trace ID for this run.         | *required*                                                                                |
| `trigger_source`       | `Literal['manual', 'scheduled']` | Source that triggered the run.     | *required*                                                                                |

## RunStatus

Parameters:

| Name                   | Type                             | Description                                    | Default                                                                                   |
| ---------------------- | -------------------------------- | ---------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `id`                   | `str`                            | The unique identifier of this run.             | *required*                                                                                |
| `integration_id`       | `str`                            | The ID of the integration this run belongs to. | *required*                                                                                |
| `trace_id`             | `str`                            | The trace ID for this run.                     | *required*                                                                                |
| `start_date`           | `datetime`                       | The start timestamp of this run.               | *required*                                                                                |
| `end_date`             | \`datetime                       | None\`                                         | The end timestamp of this run. This can be None, if the integration is currently running. |
| `success`              | `bool`                           | Whether this run was successful.               | *required*                                                                                |
| `message`              | `str`                            | Result message of this run.                    | *required*                                                                                |
| `execution_error_code` | \`int                            | None\`                                         | Error code if run failed.                                                                 |
| `flow_group_id`        | \`str                            | None\`                                         | The ID of the flow group, if any.                                                         |
| `trigger_source`       | `Literal['manual', 'scheduled']` | Source that triggered the run.                 | *required*                                                                                |

## ErrorSummary

Parameters:

| Name                 | Type  | Description         | Default    |
| -------------------- | ----- | ------------------- | ---------- |
| `local_message_text` | `str` | Error message text. | *required* |

## ErrorMessage

Parameters:

| Name                     | Type                                          | Description                           | Default    |
| ------------------------ | --------------------------------------------- | ------------------------------------- | ---------- |
| `error_message`          | `list[Union[TaskResultDetail, ErrorSummary]]` |                                       | *required* |
| `action_id`              | `str`                                         | The ID of the action that failed.     | *required* |
| `action_name`            | `str`                                         | The name of the action that failed.   | *required* |
| `failure_dump_generated` | `bool`                                        | Whether a failure dump was generated. | *required* |

## RunError

Parameters:

| Name             | Type                 | Description                                | Default    |
| ---------------- | -------------------- | ------------------------------------------ | ---------- |
| `task_id`        | `str`                | The Task ID of the invoked Anaplan Action. | *required* |
| `error_messages` | `list[ErrorMessage]` | The error messages of the run.             | *required* |

## NotificationUser

Parameters:

| Name         | Type  | Description                        | Default    |
| ------------ | ----- | ---------------------------------- | ---------- |
| `user_guid`  | `str` | The unique identifier of the user. | *required* |
| `first_name` | `str` | The user's first name.             | *required* |
| `last_name`  | `str` | The user's last name.              | *required* |

## NotificationItem

Parameters:

| Name    | Type                                                    | Description                                                 | Default    |
| ------- | ------------------------------------------------------- | ----------------------------------------------------------- | ---------- |
| `type`  | `Literal['success', 'partial_failure', 'full_failure']` | The type of notification event that triggers notifications. | *required* |
| `users` | `list[NotificationUser]`                                | The list of users who will receive this notification.       | *required* |

## Notification

Parameters:

| Name     | Type                     | Description                                         | Default    |
| -------- | ------------------------ | --------------------------------------------------- | ---------- |
| `config` | `list[NotificationItem]` | The configuration for different notification types. | *required* |

## NotificationConfig

Parameters:

| Name              | Type                               | Description                                                    | Default    |
| ----------------- | ---------------------------------- | -------------------------------------------------------------- | ---------- |
| `notification_id` | `str`                              | The unique identifier of this notification configuration.      | *required* |
| `integration_ids` | `list[str]`                        | The IDs of the integrations associated with this notification. | *required* |
| `channels`        | `list[Literal['email', 'in_app']]` | The channels through which notifications will be sent.         | *required* |
| `notifications`   | `Notification`                     | The detailed notification configuration settings.              | *required* |

## NotificationItemInput

Parameters:

| Name    | Type                                                    | Description                                                                                                                                                                                                                                                                                                   | Default    |
| ------- | ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| `type`  | `Literal['success', 'partial_failure', 'full_failure']` | The type of notification event that triggers notifications.                                                                                                                                                                                                                                                   | *required* |
| `users` | `list[str]`                                             | The list of user IDs who will receive this notification. Must not be empty. If you want nobody to receive notifications for this type, omit the entire config item. If you want to override an existing list of users with an empty one, you must delete the notification configuration and create a new one. | *required* |

## NotificationConfigInput

Parameters:

| Name     | Type                          | Description                                         | Default    |
| -------- | ----------------------------- | --------------------------------------------------- | ---------- |
| `config` | `list[NotificationItemInput]` | The configuration for different notification types. | *required* |

## NotificationInput

Parameters:

| Name              | Type                               | Description                                                    | Default    |
| ----------------- | ---------------------------------- | -------------------------------------------------------------- | ---------- |
| `integration_ids` | `list[str]`                        | The IDs of the integrations associated with this notification. | *required* |
| `channels`        | `list[Literal['email', 'in_app']]` | The channels through which notifications will be sent.         | *required* |
| `notifications`   | `NotificationConfigInput`          | The detailed notification configuration settings.              | *required* |
