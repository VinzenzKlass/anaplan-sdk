from datetime import datetime
from typing import Literal

from pydantic import Field, field_validator

from ._base import AnaplanModel
from ._bulk import TaskResultDetail

ConnectionType = Literal["AmazonS3", "AzureBlob", "GoogleBigQuery"]
IntegrationType = Literal[
    "AmazonS3ToAnaplan",
    "AzureBlobToAnaplan",
    "GoogleBigQueryToAnaplan",
    "AnaplanToAmazonS3",
    "AnaplanToAzureBlob",
    "AnaplanToGoogleBigQuery",
]

Timezone = Literal[
    "Etc/GMT+12",
    "US/Samoa",
    "Pacific/Honolulu",
    "Pacific/Marquesas",
    "US/Aleutian",
    "America/Anchorage",
    "America/Los_Angeles",
    "America/Denver",
    "America/Chicago",
    "America/New_York",
    "America/Sao_Paulo",
    "Canada/Newfoundland",
    "America/Nuuk",
    "Atlantic/Cape_Verde",
    "Greenwich",
    "Europe/London",
    "Europe/Paris",
    "Asia/Tel_Aviv",
    "Europe/Moscow",
    "Asia/Dubai",
    "Asia/Kabul",
    "Asia/Karachi",
    "Asia/Kolkata",
    "Asia/Kathmandu",
    "Asia/Dhaka",
    "Asia/Rangoon",
    "Asia/Jakarta",
    "Asia/Hong_Kong",
    "Australia/Eucla",
    "Asia/Tokyo",
    "Australia/Adelaide",
    "Australia/Brisbane",
    "Australia/Melbourne",
    "Australia/Perth",
    "Australia/Lord_Howe",
    "Pacific/Norfolk",
    "Pacific/Auckland",
    "Pacific/Chatham",
]


class _VersionedBaseModel(AnaplanModel):
    creation_date: datetime = Field(description="The initial creation date.")
    modification_date: datetime = Field(
        description=(
            "The last modification date. If never modified, this is equal to creation_date."
        )
    )
    created_by: str = Field(description="The user who created this.")
    modified_by: str | None = Field(description="The user who last modified this.")


class BaseConnectionInput(AnaplanModel):
    workspace_id: str | None = Field(
        default=None,
        description=(
            "If you are a restricted integration user, add the Workspace ID to which you have "
            "access in the payload."
        ),
    )


class AzureBlobConnectionInfo(AnaplanModel):
    name: str = Field(description="The name of the Azure Blob connection.")
    storage_account_name: str = Field(description="The name of the Azure Storage account.")
    container_name: str = Field(description="The name of the Azure Blob container.")


class AzureBlobConnectionInput(AzureBlobConnectionInfo, BaseConnectionInput):
    sas_token: str = Field(
        description=(
            "The SAS token for the Azure Blob connection. Must be created on the container "
            "directly and not on any child blobs and have at least 'Read' and 'List' permissions."
        )
    )


class AmazonS3ConnectionInfo(AnaplanModel):
    name: str = Field(description="The name of the Amazon S3 connection.")
    bucket_name: str = Field(description="The name of the Amazon S3 bucket.")


class AmazonS3ConnectionInput(AmazonS3ConnectionInfo, BaseConnectionInput):
    access_key_id: str = Field(description="The access key ID for the Amazon S3 connection.")
    secret_access_key: str = Field(
        description="The secret access key for the Amazon S3 connection."
    )


class GoogleBigQueryConnectionInfo(AnaplanModel):
    name: str = Field(description="The name of the Google BigQuery connection.")
    dataset: str = Field(description="The ID of the Google BigQuery dataset.")


class GoogleServiceAccountJson(AnaplanModel):
    type: str = Field(description="The type of the service account.")
    project_id: str = Field(description="The project ID of the service account.")
    private_key_id: str = Field(description="The private key ID of the service account.")
    private_key: str = Field(description="The private key of the service account.")
    client_email: str = Field(description="The client email of the service account.")
    client_id: str = Field(description="The client ID of the service account.")
    auth_uri: str = Field(description="The authentication URI of the service account.")
    token_uri: str = Field(description="The token URI of the service account.")
    auth_provider_x509_cert_url: str = Field(
        description="The authentication provider's X.509 certificate URL."
    )
    client_x509_cert_url: str = Field(description="The client's X.509 certificate URL.")


class GoogleBigQueryConnectionInput(GoogleBigQueryConnectionInfo, BaseConnectionInput):
    serviceAccountKey: GoogleServiceAccountJson = Field(
        description="The service account JSON for the Google BigQuery connection."
    )


ConnectionBody = AzureBlobConnectionInput | AmazonS3ConnectionInput | GoogleBigQueryConnectionInput


class ConnectionInput(AnaplanModel):
    type: ConnectionType = Field(description="The type of this connection.")
    body: ConnectionBody = Field(description="Connection information.")


class Connection(_VersionedBaseModel):
    id: str = Field(
        validation_alias="connectionId", description="The unique identifier of this connection."
    )
    connection_type: ConnectionType = Field(description="The type of this connection.")
    body: AzureBlobConnectionInfo | AmazonS3ConnectionInfo | GoogleBigQueryConnectionInfo = Field(
        description="Connection information."
    )
    status: int = Field(
        description=(
            "The status of this connection. 1 indicates a valid connection, 0 indicates an invalid "
            "connection."
        )
    )
    integration_error_code: str | None = Field(
        description="The error code of the connection, if any."
    )
    workspace_id: str | None = Field(
        description="The workspace that was given when creating this connection."
    )


class LatestRun(AnaplanModel):
    triggered_by: str = Field(description="The user who triggered this run.")
    start_date: datetime = Field(description="The start timestamp of this run.")
    end_date: datetime | None = Field(
        default=None,
        description=(
            "The end timestamp of this run. This can be None, if the integration is currently "
            "running."
        ),
    )
    success: bool = Field(description="Whether this run was successful.")
    message: str = Field(description="Result message of this run.")
    execution_error_code: int | None = Field(default=None, description="Error code if run failed.")
    trigger_source: str | None = Field(default=None, description="Source that triggered the run.")


class ScheduleBase(AnaplanModel):
    name: str = Field(description="Name of the schedule.")
    type: Literal[
        "hourly", "daily", "weekly", "monthly_specific_day", "monthly_relative_weekday"
    ] = Field(description="Trigger Frequency")
    timezone: Timezone = Field(description="Timezone for the schedule.")


class ScheduleInput(ScheduleBase):
    time: str | None = Field(default=None, description="Time for scheduled runs in HH:mm format.")
    from_time: str | None = Field(
        default=None, description="Time for scheduled runs in HH:mm format, if type is hourly."
    )
    to_time: str | None = Field(
        default=None, description="Time for scheduled runs in HH:mm format, if type is hourly."
    )
    days_of_week: list[int] = Field(description="Days of week when schedule is active.")
    start_date: str = Field(
        description=(
            "Start date for the schedule in YYYY-MM-DD format. Must be in the Future, i.e. current "
            "day, if the `time` is greater than the current time or any future date. "
        )
    )
    end_date: str | None = Field(
        default=None,
        description=(
            "End date for the schedule in YYYY-MM-DD format. Must be in the Future, i.e. current "
            "day, if the `time` is greater than the current time or any future date. Can also be "
            "omitted to create a schedule that runs indefinitely."
        ),
    )


class Schedule(ScheduleBase):
    time: str | None = Field(default=None, description="Time for scheduled runs in HH:mm format.")
    to_time: str | None = Field(default=None, description="End time for scheduled runs.")
    from_time: str | None = Field(default=None, description="Start time for scheduled runs.")
    start_date: datetime = Field(description="Start date of the schedule.")
    end_date: datetime | None = Field(default=None, description="End date of the schedule, if set.")
    days_of_week: list[int] = Field(default=[], description="Days of week when schedule is active.")
    repeat_every: int | None = Field(default=None, description="Frequency of repetition.")
    status: str = Field(description="Current status of the schedule.")


class _BaseIntegration(_VersionedBaseModel):
    name: str = Field(description="The name of this integration.")
    created_by: str = Field(description="The user who created this integration.")
    notification_id: str | None = Field(
        default=None, description="The ID of the associated notification configuration, if any."
    )
    latest_run: LatestRun | None = Field(
        default=None, description="Details about the latest execution, if any."
    )

    @field_validator("latest_run", mode="before")
    @classmethod
    def _empty_source_is_none(cls, inp: dict):
        return inp if inp else None


class Integration(_BaseIntegration):
    id: str = Field(
        validation_alias="integrationId", description="The unique identifier of this integration."
    )
    integration_type: Literal["Import", "Export", "Process"] = Field(
        description="The type of this integration."
    )
    model_id: str = Field(description="The ID of the model this integration belongs to.")
    workspace_id: str = Field(description="The ID of the workspace this integration belongs to.")
    nux_visible: bool = Field(description="Whether this integration is visible in the UI.")
    process_id: str | None = Field(None, description="The ID of the process (for Process type).")
    schedule: Schedule | None = Field(
        default=None, description="Schedule configuration if defined."
    )


class AnaplanSource(AnaplanModel):
    type: Literal["Anaplan"] = Field(
        default="Anaplan", description="Literal signifying this is an Anaplan source."
    )
    action_id: int = Field(
        description=(
            "The ID of the action to be used as a source. This can be a process, or export."
        )
    )


class FileSourceInput(AnaplanModel):
    connection_id: str = Field(description="The unique identifier of the connection.")
    type: Literal["AmazonS3", "AzureBlob"] = Field(description="The type of this connection.")
    file: str = Field(description="The file path relative to the root of the connection.")


class FileSource(FileSourceInput):
    connection_name: str = Field(description="The name of the connection.")
    is_connection_deleted: bool = Field(description="Whether the connection has been deleted.")
    bucket_name: str | None = Field(
        default=None, description="The name of the bucket, if applicable."
    )


class TableSource(AnaplanModel):
    type: Literal["GoogleBigQuery"] = Field(
        default="GoogleBigQuery", description="The type of this connection."
    )
    connection_id: str = Field(description="The unique identifier of the connection.")
    table: str = Field(description="The table name in the BigQuery dataset in the connection.")


class FileTarget(FileSourceInput):
    overwrite: bool = Field(default=True, description="Whether to overwrite the file if it exists.")


class TableTarget(TableSource):
    overwrite: bool = Field(
        default=False, description="Whether to overwrite the table if it exists."
    )


class AnaplanTarget(AnaplanModel):
    type: Literal["Anaplan"] = Field(
        default="Anaplan", description="Literal signifying this is an Anaplan target."
    )
    action_id: int = Field(
        description=(
            "The ID of the action to be used as a target. This can be a process, or import."
        )
    )
    file_id: int = Field(description="The ID of the file to be used as a target.")


class IntegrationJobs(AnaplanModel):
    type: IntegrationType = Field(description="The type of this integration.")
    sources: list[AnaplanSource | FileSource | TableSource] = Field(
        description="The source of this job."
    )
    targets: list[AnaplanTarget | FileTarget | TableTarget] = Field(
        description="The target of this job."
    )


class SingleIntegration(Integration):
    integration_type: None = Field(
        default=None,
        description=(
            "Sentinel for erroneous implementation of the Anaplan API. This field is not provided "
            "when getting an individual integration by Id."
        ),
    )
    jobs: list[IntegrationJobs] | None = Field(
        default=None,
        description=(
            "The Integration Job details. The source and target can be switched according to "
            "convert imports and exports requirement."
        ),
    )


class IntegrationJobInput(AnaplanModel):
    type: IntegrationType = Field(description="The type of this integration.")
    sources: list[AnaplanSource | FileSourceInput | TableSource] = Field(
        description="The sources of this integration."
    )
    targets: list[AnaplanTarget | FileTarget | TableTarget] = Field(
        description="The targets of this integration."
    )


class IntegrationProcessInput(AnaplanModel):
    name: str = Field(description="The name of this integration process.")
    version: Literal["2.0"] = Field(default="2.0", description="The version of this integration.")
    workspace_id: str = Field(description="The ID of the workspace this integration belongs to.")
    model_id: str = Field(description="The ID of the model this integration belongs to.")
    process_id: int = Field(description="The ID of the process this integration belongs to.")


class IntegrationInput(AnaplanModel):
    name: str = Field(description="The name of this integration.")
    version: Literal["2.0"] = Field(default="2.0", description="The version of this integration.")
    workspace_id: str = Field(description="The ID of the workspace this integration belongs to.")
    model_id: str = Field(description="The ID of the model this integration belongs to.")
    process_id: int | None = Field(
        default=None,
        description=(
            "If given, an integration process will be created, instead of an Import or Export"
        ),
    )
    nux_visible: bool = Field(
        default=False, description="Whether this integration is visible in the UI."
    )
    jobs: list[IntegrationJobInput] = Field(
        description="The jobs in this integration.", min_length=1
    )


class RunSummary(AnaplanModel):
    id: str = Field(description="The unique identifier of this run.")
    triggered_by: str
    last_run: datetime = Field(description="Last Run timestamp.")
    start_date: datetime = Field(description="Start timestamp.")
    end_date: datetime | None = Field(
        default=None,
        description=(
            "The end timestamp of this run. This can be None, if the integration is currently "
            "running."
        ),
    )
    success: bool = Field(description="Whether this run was successful.")
    message: str = Field(description="Result message of this run.")
    execution_error_code: int | None = Field(default=None, description="Error code if run failed.")
    trace_id: str = Field(description="The trace ID for this run.")
    trigger_source: Literal["manual", "scheduled"] = Field(
        description="Source that triggered the run."
    )


class RunStatus(AnaplanModel):
    id: str = Field(description="The unique identifier of this run.")
    integration_id: str = Field(description="The ID of the integration this run belongs to.")
    trace_id: str = Field(description="The trace ID for this run.")
    start_date: datetime = Field(description="The start timestamp of this run.")
    end_date: datetime | None = Field(
        default=None,
        description=(
            "The end timestamp of this run. This can be None, if the integration is currently "
            "running."
        ),
    )
    success: bool = Field(description="Whether this run was successful.")
    message: str = Field(description="Result message of this run.")
    execution_error_code: int | None = Field(default=None, description="Error code if run failed.")
    flow_group_id: str | None = Field(default=None, description="The ID of the flow group, if any.")
    trigger_source: Literal["manual", "scheduled"] = Field(
        description="Source that triggered the run."
    )


class ErrorSummary(AnaplanModel):
    local_message_text: str = Field(description="Error message text.")


class ErrorMessage(AnaplanModel):
    error_message: list[TaskResultDetail | ErrorSummary]
    action_id: str = Field(description="The ID of the action that failed.")
    action_name: str = Field(description="The name of the action that failed.")
    failure_dump_generated: bool = Field(description="Whether a failure dump was generated.")


class RunError(AnaplanModel):
    task_id: str = Field(description="The Task ID of the invoked Anaplan Action.")
    error_messages: list[ErrorMessage] = Field(description="The error messages of the run.")


class NotificationUser(AnaplanModel):
    user_guid: str = Field(description="The unique identifier of the user.")
    first_name: str = Field(description="The user's first name.")
    last_name: str = Field(description="The user's last name.")


class NotificationItem(AnaplanModel):
    type: Literal["success", "partial_failure", "full_failure"] = Field(
        description="The type of notification event that triggers notifications."
    )
    users: list[NotificationUser] = Field(
        description="The list of users who will receive this notification."
    )


class Notification(AnaplanModel):
    config: list[NotificationItem] = Field(
        description="The configuration for different notification types."
    )


class NotificationConfig(AnaplanModel):
    notification_id: str = Field(
        description="The unique identifier of this notification configuration."
    )
    integration_ids: list[str] = Field(
        description="The IDs of the integrations associated with this notification."
    )
    channels: list[Literal["email", "in_app"]] = Field(
        description="The channels through which notifications will be sent."
    )
    notifications: Notification = Field(
        description="The detailed notification configuration settings."
    )


class NotificationItemInput(AnaplanModel):
    type: Literal["success", "partial_failure", "full_failure"] = Field(
        description="The type of notification event that triggers notifications."
    )
    users: list[str] = Field(
        description=(
            "The list of user IDs who will receive this notification. Must not be empty. If you "
            "want nobody to receive notifications for this type, omit the entire config item. If "
            "you want to override an existing list of users with an empty one, you must delete the "
            "notification configuration and create a new one."
        ),
        min_length=1,
        max_length=5,
    )


class NotificationConfigInput(AnaplanModel):
    config: list[NotificationItemInput] = Field(
        description="The configuration for different notification types."
    )


class NotificationInput(AnaplanModel):
    integration_ids: list[str] = Field(
        description="The IDs of the integrations associated with this notification."
    )
    channels: list[Literal["email", "in_app"]] = Field(
        description="The channels through which notifications will be sent."
    )
    notifications: NotificationConfigInput = Field(
        description="The detailed notification configuration settings."
    )
