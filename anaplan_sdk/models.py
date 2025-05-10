from typing import Literal, TypeAlias

from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic.alias_generators import to_camel

ExportTypes: TypeAlias = Literal[
    "TABULAR_MULTI_COLUMN",
    "TABULAR_SINGLE_COLUMN",
    "GRID_CURRENT_PAGE",
    "AUDIT_LOG",
    "TABULAR_ALL_LINE_ITEMS",
    "TABULAR_CURRENT_LINE_ITEM",
]

ImportTypes: TypeAlias = Literal[
    "MODULE_DATA", "HIERARCHY_DATA", "LINE_ITEM_DEFINITION", "USERS", "VERSIONS"
]
ConnectionType = Literal["AmazonS3", "AzureBlob", "GoogleBigQuery"]


class Workspace(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    id: str = Field(description="The unique identifier of this workspace.")
    name: str = Field(description="The name of this workspace that is also displayed to the users.")
    active: bool = Field(description="Whether this workspace is active or not.")
    size_allowance: int = Field(description="The maximum allowed size of this workspace in bytes.")
    current_size: int = Field(description="The current size of this workspace in bytes.")


class Model(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    id: str = Field(description="The unique identifier of this model.")
    name: str
    active_state: Literal["ARCHIVED", "UNLOCKED", "ACTIVE", "PRODUCTION"] = Field(
        description="The current state of this model."
    )
    last_saved_serial_number: int = Field(
        description="The serial number of the last save of this model."
    )
    last_modified_by_user_guid: str = Field(
        description="The unique identifier of the user who last modified this model."
    )
    memory_usage: int = Field(0, description="The memory usage of this model in bytes.")
    current_workspace_id: str = Field(
        description="The unique identifier of the workspace that this model is currently in."
    )
    current_workspace_name: str = Field(
        description="The name of the workspace that this model is currently in."
    )
    url: str = Field(validation_alias="modelUrl", description="The current URL of this model.")
    category_values: list = Field(description="The category values of this model.")
    iso_creation_date: str = Field(description="The creation date of this model in ISO format.")
    last_modified: str = Field(description="The last modified date of this model.")


class File(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    id: int = Field(description="The unique identifier of this file.")
    name: str = Field(description="The name of this file.")
    chunk_count: int = Field(description="The number of chunks this file is split into.")
    delimiter: str | None = Field(None, description="The delimiter used in this file.")
    encoding: str | None = Field(None, description="The encoding of this file.")
    first_data_row: int = Field(description="The row number of the first data row in this file.")
    format: str | None = Field(None, description="The format of this file.")
    header_row: int = Field(description="The row number of the header row in this file.")
    separator: str | None = Field(None, description="The separator used in this file.")


class List(BaseModel):
    id: int = Field(description="The unique identifier of this list.")
    name: str = Field(description="The name of this list.")


class ListMetadata(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    id: int = Field(description="The unique identifier of this list.")
    name: str = Field(description="The name of this list.")
    has_selective_access: bool = Field(description="Whether this list has selective access or not.")
    properties: list = Field([], description="The properties of this list.")
    production_data: bool = Field(description="Whether this list is production data or not.")
    managed_by: str = Field(description="The user who manages this list.")
    numbered_list: bool = Field(description="Whether this list is a numbered list or not.")
    use_top_level_as_page_default: bool = Field(
        description="Whether the top level is used as the page default or not."
    )
    item_count: int = Field(description="The number of items in this list.")
    next_item_index: int | None = Field(
        None, description="The index of the next item in this list."
    )
    workflow_enabled: bool = Field(
        description="Whether the workflow is enabled for this list or not."
    )
    permitted_items: int = Field(description="The number of permitted items in this list.")
    used_in_applies_to: str | None = Field(None, description="The applies to value of this list.")


class Action(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: int = Field(description="The unique identifier of this action.")
    name: str = Field(
        description="The name of this Action. This is the same as the one displayed in the Web UI."
    )
    type: str | None = Field(
        None, validation_alias="actionType", description="The type of this action."
    )


class ListItem(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    id: int = Field(description="The unique identifier of this list item.")
    name: str = Field(description="The name of this list item.")
    code: str | None = Field(None, description="The code of this list item.")
    properties: dict = Field({}, description="The properties of this list item.")
    subsets: dict = Field({}, description="The subsets of this list item.")
    parent: str | None = Field(None, description="The parent of this list item.")
    parent_id: str | None = Field(
        None, description="The unique identifier of the parent of this list item."
    )


class Process(BaseModel):
    id: int = Field(description="The unique identifier of this process.")
    name: str = Field(description="The name of this process.")


class Import(BaseModel):
    id: int = Field(description="The unique identifier of this import.")
    name: str = Field(description="The name of this import.")
    type: ImportTypes = Field(validation_alias="importType", description="The type of this import.")
    file_id: int | None = Field(
        None,
        validation_alias="importDataSourceId",
        description=(
            "The unique identifier of the data source of this import. If it is absent, it means "
            "that the import is not a file import."
        ),
    )

    # noinspection PyNestedDecorators
    @field_validator("file_id", mode="before")
    @classmethod
    def _empty_source_is_none(cls, inp: str):
        return inp if inp else None


class Export(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: int = Field(description="The unique identifier of this export.")
    name: str = Field(description="The name of this export.")
    type: ExportTypes = Field(validation_alias="exportType", description="The type of this export.")
    format: str = Field(validation_alias="exportFormat", description="The format of this export.")
    encoding: str | None = Field(None, description="The encoding of this export.")
    layout: ExportTypes = Field(
        description="The layout of this export, representing the Anaplan Export Structure."
    )


class Module(BaseModel):
    id: int = Field(description="The unique identifier of this module.")
    name: str = Field(description="The name of this module.")


class ModelStatus(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    peak_memory_usage_estimate: int | None = Field(
        description="The peak memory usage estimate of this model."
    )
    peak_memory_usage_time: int | None = Field(
        description="The peak memory usage time of this model."
    )
    progress: float = Field(description="The progress of this model.")
    current_step: str = Field(description="The current step of this model.")
    tooltip: str | None = Field(description="The tooltip of this model.")
    task_id: str | None = Field(description="The unique identifier of the task of this model.")
    creation_time: int = Field(description="The creation time of this model.")
    export_task_type: str | None = Field(description="The export task type of this model.")


class LineItem(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    id: int = Field(description="The unique identifier of this line item.")
    name: str = Field(description="The name of this line item.")
    module_id: int = Field(
        description="The unique identifier of the module this line item belongs to."
    )
    module_name: str = Field(description="The name of the module this line item belongs to.")
    format: str = Field(description="The format of this line item.")
    format_metadata: dict = Field(description="The format metadata of this line item.")
    summary: str = Field(description="The summary of this line item.")
    applies_to: list[dict] = Field([], description="The applies to value of this line item.")
    time_scale: str = Field(description="The time scale of this line item.")
    time_range: str = Field(description="The time range of this line item.")
    version: dict = Field(description="The version of this line item.")
    style: str = Field(description="The style of this line item.")
    cell_count: int | None = Field(None, description="The cell count of this line item.")
    notes: str = Field(description="The notes of this line item.")
    is_summary: bool = Field(description="Whether this line item is a summary or not.")
    formula: str | None = Field(None, description="The formula of this line item.")
    formula_scope: str = Field(description="The formula scope of this line item.")
    use_switchover: bool = Field(description="Whether the switchover is used or not.")
    breakback: bool = Field(description="Whether the breakback is enabled or not.")
    brought_forward: bool = Field(description="Whether the brought forward is enabled or not.")
    start_of_section: bool = Field(
        description="Whether this line item is the start of a section or not."
    )


class Failure(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    index: int = Field(
        validation_alias="requestIndex", description="The index of the item that failed."
    )
    reason: str = Field(validation_alias="failureType", description="The reason for the failure.")
    details: str = Field(
        validation_alias="failureMessageDetails", description="The details of the failure."
    )


class InsertionResult(BaseModel):
    added: int = Field(description="The number of items successfully added.")
    ignored: int = Field(description="The number of items ignored, or items that failed.")
    total: int = Field(description="The total number of items.")
    failures: list[Failure] = Field([], description="The list of failures.")


class Revision(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    id: str = Field(description="The unique identifier of this revision.")
    name: str = Field(description="The name of this revision.")
    description: str | None = Field(
        None, description="The description of this revision. Not always present."
    )
    created_on: str = Field(description="The creation date of this revision in ISO format.")
    created_by: str = Field(
        description="The unique identifier of the user who created this revision."
    )
    creation_method: str = Field(description="The creation method of this revision.")
    applied_on: str = Field(description="The application date of this revision in ISO format.")
    applied_by: str = Field(
        description="The unique identifier of the user who applied this revision."
    )


class ModelRevision(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    id: str = Field(
        validation_alias="modelId",
        description="The unique identifier of the model this revision belongs to.",
    )
    name: str = Field(
        validation_alias="modelName", description="The name of the model this revision belongs to."
    )
    workspace_id: str = Field(
        description="The unique identifier of the workspace this revision belongs to."
    )
    applied_by: str = Field(
        description="The unique identifier of the user who applied this revision."
    )
    applied_on: str = Field(description="The application date of this revision in ISO format.")
    applied_method: str = Field(description="The application method of this revision.")
    deleted: bool | None = Field(
        None,
        validation_alias="modelDeleted",
        description="Whether the model has been deleted or not.",
    )


class SyncTask(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    id: str = Field(validation_alias="taskId", description="The unique identifier of this task.")
    task_state: str = Field(description="The state of this task.")
    creation_time: int = Field(description="The creation time of this task.")


class User(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    id: str = Field(description="The unique identifier of this user.")
    active: bool = Field(description="Whether this user is active or not.")
    email: str = Field(description="The email address of this user.")
    email_opt_in: bool = Field(
        description="Whether this user has opted in to receive emails or not."
    )
    first_name: str = Field(description="The first name of this user.")
    last_name: str = Field(description="The last name of this user.")
    last_login_date: str | None = Field(
        None, description="The last login date of this user in ISO format."
    )


class TaskSummary(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    id: str = Field(validation_alias="taskId", description="The unique identifier of this task.")
    task_state: Literal["NOT_STARTED", "IN_PROGRESS", "COMPLETE"] = Field(
        description="The state of this task."
    )
    creation_time: int = Field(description="Unix timestamp of when this task was created.")


class TaskResultDetail(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    local_message_text: str = Field(description="Error message text.")
    occurrences: int = Field(0, description="The number of occurrences of this error.")
    type: str = Field(description="The type of this error.")
    values: list[str] = Field([], description="Further error information if available.")


class TaskResult(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    details: list[TaskResultDetail] = Field(
        [], description="The details of this task result if available."
    )
    successful: bool = Field(description="Whether this task completed successfully or not.")
    failure_dump_available: bool = Field(
        description="Whether this task completed successfully or not."
    )
    nested_results: list["TaskResult"] = Field(
        [], description="The nested results of this task, if available."
    )


class TaskStatus(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    id: str = Field(validation_alias="taskId", description="The unique identifier of this task.")
    task_state: Literal["NOT_STARTED", "IN_PROGRESS", "COMPLETE"] = Field(
        description="The state of this task."
    )
    creation_time: int = Field(description="Unix timestamp of when this task was created.")
    progress: float = Field(description="The progress of this task as a float between 0 and 1.")
    current_step: str | None = Field(None, description="The current step of this task.")
    result: TaskResult | None = Field(None)


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
