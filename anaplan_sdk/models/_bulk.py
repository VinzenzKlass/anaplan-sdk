from typing import Literal, TypeAlias

from pydantic import Field, field_validator

from ._base import AnaplanModel

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


class Workspace(AnaplanModel):
    id: str = Field(description="The unique identifier of this workspace.")
    name: str = Field(description="The name of this workspace that is also displayed to the users.")
    active: bool = Field(description="Whether this workspace is active or not.")
    size_allowance: int = Field(description="The maximum allowed size of this workspace in bytes.")
    current_size: int = Field(description="The current size of this workspace in bytes.")


class Model(AnaplanModel):
    id: str = Field(description="The unique identifier of this model.")
    name: str
    active_state: Literal[
        "ARCHIVED", "UNLOCKED", "ACTIVE", "PRODUCTION", "MAINTENANCE", "PRODUCTION_MAINTENANCE"
    ] = Field(description="The current state of this model.")
    last_saved_serial_number: int = Field(
        description="The serial number of the last save of this model."
    )
    last_modified_by_user_guid: str = Field(
        description="The unique identifier of the user who last modified this model."
    )
    memory_usage: int = Field(0, description="The memory usage of this model in bytes.")
    workspace_id: str = Field(
        validation_alias="currentWorkspaceId",
        description="The unique identifier of the workspace that this model is currently in.",
    )
    workspace_name: str = Field(
        validation_alias="currentWorkspaceName",
        description="The name of the workspace that this model is currently in.",
    )
    url: str = Field(validation_alias="modelUrl", description="The current URL of this model.")
    category_values: list = Field(description="The category values of this model.")
    iso_creation_date: str = Field(description="The creation date of this model in ISO format.")
    last_modified: str = Field(description="The last modified date of this model.")


class File(AnaplanModel):
    id: int = Field(description="The unique identifier of this file.")
    name: str = Field(description="The name of this file.")
    chunk_count: int = Field(description="The number of chunks this file is split into.")
    delimiter: str | None = Field(None, description="The delimiter used in this file.")
    encoding: str | None = Field(None, description="The encoding of this file.")
    first_data_row: int = Field(description="The row number of the first data row in this file.")
    format: str | None = Field(None, description="The format of this file.")
    header_row: int = Field(description="The row number of the header row in this file.")
    separator: str | None = Field(None, description="The separator used in this file.")


class List(AnaplanModel):
    id: int = Field(description="The unique identifier of this list.")
    name: str = Field(description="The name of this list.")


class ListMetadata(AnaplanModel):
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


class Action(AnaplanModel):
    id: int = Field(description="The unique identifier of this action.")
    name: str = Field(
        description="The name of this Action. This is the same as the one displayed in the Web UI."
    )
    type: str | None = Field(
        None, validation_alias="actionType", description="The type of this action."
    )


class Process(AnaplanModel):
    id: int = Field(description="The unique identifier of this process.")
    name: str = Field(description="The name of this process.")


class Import(AnaplanModel):
    id: int = Field(description="The unique identifier of this import.")
    name: str = Field(description="The name of this import.")
    type: ImportTypes = Field(validation_alias="importType", description="The type of this import.")
    file_id: int | None = Field(
        None,
        validation_alias="importDataSourceId",
        description=(
            "The unique identifier of the data source of this import. If it is absent, it means "
            "that the import does not read from any file."
        ),
    )

    @field_validator("file_id", mode="before")
    @classmethod
    def _empty_source_is_none(cls, inp: str):
        return inp if inp else None


class Export(AnaplanModel):
    id: int = Field(description="The unique identifier of this export.")
    name: str = Field(description="The name of this export.")
    type: ExportTypes = Field(validation_alias="exportType", description="The type of this export.")
    format: str = Field(validation_alias="exportFormat", description="The format of this export.")
    encoding: str | None = Field(None, description="The encoding of this export.")
    layout: ExportTypes = Field(
        description="The layout of this export, representing the Anaplan Export Structure."
    )


class TaskSummary(AnaplanModel):
    id: str = Field(validation_alias="taskId", description="The unique identifier of this task.")
    task_state: Literal["NOT_STARTED", "IN_PROGRESS", "COMPLETE"] = Field(
        description="The state of this task."
    )
    creation_time: int = Field(description="Unix timestamp of when this task was created.")


class TaskResultDetail(AnaplanModel):
    local_message_text: str | None = Field(None, description="Error message text.")
    occurrences: int = Field(0, description="The number of occurrences of this error.")
    type: str = Field(description="The type of this error.")
    values: list[str | None] = Field([], description="Further error information if available.")


class TaskResult(AnaplanModel):
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


class TaskStatus(TaskSummary):
    progress: float = Field(description="The progress of this task as a float between 0 and 1.")
    current_step: str | None = Field(None, description="The current step of this task.")
    result: TaskResult | None = Field(None)


class DeletionFailure(AnaplanModel):
    model_id: str = Field(description="The unique identifier of the model that failed to delete.")
    message: str = Field(description="The error message explaining why the deletion failed.")


class ModelDeletionResult(AnaplanModel):
    models_deleted: int = Field(description="The number of models that were successfully deleted.")
    failures: list[DeletionFailure] = Field(
        [],
        validation_alias="bulkDeleteModelsFailures",
        description="List of models that failed to delete with their error messages.",
    )
