from typing import Literal

from pydantic import Field, field_validator

from ._base import AnaplanModel

ConnectionType = Literal["AmazonS3", "AzureBlob", "GoogleBigQuery"]
IntegrationType = Literal[
    "AmazonS3ToAnaplan",
    "AzureBlobToAnaplan",
    "GoogleBigQueryToAnaplan",
    "AnaplanToAmazonS3",
    "AnaplanToAzureBlob",
    "AnaplanToGoogleBigQuery",
]


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
    bucket_name: str = Field(description="The name of the Amazon S3 bucket.")


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


class ConnectionInput(AnaplanModel):
    type: ConnectionType = Field(description="The type of this connection.")
    body: AzureBlobConnectionInput | AmazonS3ConnectionInput | GoogleBigQueryConnectionInput = (
        Field(description="Connection information.")
    )


class Connection(AnaplanModel):
    connection_id: str = Field(description="The unique identifier of this connection.")
    connection_type: ConnectionType = Field(description="The type of this connection.")
    body: AzureBlobConnectionInfo | AmazonS3ConnectionInfo | GoogleBigQueryConnectionInfo = Field(
        description="Connection information."
    )
    creation_date: str = Field(description="The initial creation date of this connection.")
    modification_date: str = Field(
        description=(
            "The last modification date of this connection. If never modified, this is equal to "
            "creation_date."
        )
    )
    created_by: str = Field(description="The user who created this connection.")
    modified_by: str | None = Field(description="The user who last modified this connection.")
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
    start_date: str = Field(description="The start timestamp of this run.")
    end_date: str = Field(description="The end timestamp of this run.")
    success: bool = Field(description="Whether this run was successful.")
    message: str = Field(description="Result message of this run.")
    execution_error_code: str | None = Field(default=None, description="Error code if run failed.")
    trigger_source: str | None = Field(default=None, description="Source that triggered the run.")


class Schedule(AnaplanModel):
    name: str = Field(description="Name of the schedule.")
    type: str = Field(description="Type of schedule (daily, hourly, etc).")
    to_time: str = Field(description="End time for scheduled runs.")
    from_time: str = Field(description="Start time for scheduled runs.")
    end_date: str = Field(description="End date of the schedule.")
    start_date: str = Field(description="Start date of the schedule.")
    timezone: str = Field(description="Timezone for the schedule.")
    days_of_week: list[int] = Field(description="Days of week when schedule is active (1=Monday).")
    repeat_every: int = Field(description="Frequency of repetition.")
    status: str = Field(description="Current status of the schedule.")


class Integration(AnaplanModel):
    integration_id: str = Field(description="The unique identifier of this integration.")
    name: str = Field(description="The name of this integration.")
    integration_type: Literal["Import", "Export", "Process"] = Field(
        description="The type of this integration."
    )
    created_by: str = Field(description="The user who created this integration.")
    creation_date: str = Field(description="The initial creation date of this integration.")
    modification_date: str = Field(description="The last modification date of this integration.")
    modified_by: str | None = Field(
        None, description="The user who last modified this integration."
    )
    model_id: str = Field(description="The ID of the model this integration belongs to.")
    workspace_id: str = Field(description="The ID of the workspace this integration belongs to.")
    nux_visible: bool = Field(description="Whether this integration is visible in the UI.")
    process_id: str | None = Field(None, description="The ID of the process (for Process type).")
    latest_run: LatestRun | None = Field(
        default=None, description="Details about the latest execution, if any."
    )
    schedule: Schedule | None = Field(
        default=None, description="Schedule configuration if defined."
    )
    notification_id: str = Field(description="The ID of the associated notification.")

    @field_validator("latest_run", mode="before")
    @classmethod
    def _empty_source_is_none(cls, inp: dict):
        return inp if inp else None


class AnaplanSource(AnaplanModel):
    type: Literal["Anaplan"] = Field(
        default="Anaplan", description="Literal signifying this is an Anaplan source."
    )
    action_id: int = Field(
        description=(
            "The ID of the action to be used as a source. This can be a process, or export."
        )
    )


class FileSource(AnaplanModel):
    connection_id: str = Field(description="The unique identifier of the connection.")
    type: Literal["AmazonS3", "AzureBlob"] = Field(description="The type of this connection.")
    file: str = Field(description="The file path relative to the root of the connection.")


class FileTarget(FileSource):
    connection_id: str = Field(description="The unique identifier of the connection.")
    type: Literal["AmazonS3", "AzureBlob"] = Field(description="The type of this connection.")
    overwrite: bool = Field(default=True, description="Whether to overwrite the file if it exists.")


class TableSource(AnaplanModel):
    type: Literal["GoogleBigQuery"] = Field(
        default="GoogleBigQuery", description="The type of this connection."
    )
    connection_id: str = Field(description="The unique identifier of the connection.")
    table: str = Field(description="The table name in the BigQuery dataset in the connection.")


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
        ),
    )
    file_id: int = Field(description="The ID of the file to be used as a target.")


class IntegrationJobInput(AnaplanModel):
    type: IntegrationType = Field(description="The type of this integration.")
    sources: list[AnaplanSource | FileSource | TableSource] = Field(
        description="The sources of this integration."
    )
    targets: list[AnaplanTarget | FileTarget | TableTarget] = Field(
        description="The targets of this integration."
    )


class IntegrationInput(AnaplanModel):
    name: str = Field(description="The name of this integration.")
    version: Literal["2.0"] = Field(default="2.0", description="The version of this integration.")
    workspace_id: str = Field(description="The ID of the workspace this integration belongs to.")
    model_id: str = Field(description="The ID of the model this integration belongs to.")
    nux_visible: bool = Field(
        default=False, description="Whether this integration is visible in the UI."
    )
    jobs: list[IntegrationJobInput] = Field(
        description="The jobs in this integration.", min_length=1
    )
