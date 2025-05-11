from typing import Literal

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

ConnectionType = Literal["AmazonS3", "AzureBlob", "GoogleBigQuery"]


class AzureBlobConnectionInfo(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    name: str = Field(description="The name of the Azure Blob connection.")
    storage_account_name: str = Field(description="The name of the Azure Storage account.")
    container_name: str = Field(description="The name of the Azure Blob container.")


class AmazonS3ConnectionInfo(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    name: str = Field(description="The name of the Amazon S3 connection.")
    bucket_name: str = Field(description="The name of the Amazon S3 bucket.")


class GoogleBigQueryConnectionInfo(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    name: str = Field(description="The name of the Google BigQuery connection.")
    dataset: str = Field(description="The ID of the Google BigQuery dataset.")


class Connection(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
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
