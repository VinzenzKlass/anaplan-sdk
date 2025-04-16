from typing import Literal, TypeAlias

from pydantic import BaseModel, Field, field_validator

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


class Workspace(BaseModel):
    id: str = Field(description="The unique identifier of this workspace.")
    name: str = Field(description="The name of this workspace that is also displayed to the users.")
    active: bool = Field(description="Whether this workspace is active or not.")
    size_allowance: int = Field(
        alias="sizeAllowance", description="The maximum allowed size of this workspace in bytes."
    )
    current_size: int = Field(
        alias="currentSize", description="The current size of this workspace in bytes."
    )


class Model(BaseModel):
    id: str = Field(description="The unique identifier of this model.")
    name: str
    active_state: Literal["ARCHIVED", "UNLOCKED", "ACTIVE", "PRODUCTION"] = Field(
        alias="activeState", description="The current state of this model."
    )
    last_saved_serial_number: int = Field(
        alias="lastSavedSerialNumber",
        description="The serial number of the last save of this model.",
    )
    last_modified_by_user_guid: str = Field(
        alias="lastModifiedByUserGuid",
        description="The unique identifier of the user who last modified this model.",
    )
    memory_usage: int = Field(
        0, alias="memoryUsage", description="The memory usage of this model in bytes."
    )
    current_workspace_id: str = Field(
        alias="currentWorkspaceId",
        description="The unique identifier of the workspace that this model is currently in.",
    )
    current_workspace_name: str = Field(
        alias="currentWorkspaceName",
        description="The name of the workspace that this model is currently in.",
    )
    url: str = Field(alias="modelUrl", description="The current URL of this model.")
    category_values: list = Field(
        alias="categoryValues", description="The category values of this model."
    )
    iso_creation_date: str = Field(
        alias="isoCreationDate", description="The creation date of this model in ISO format."
    )
    last_modified: str = Field(
        alias="lastModified", description="The last modified date of this model."
    )


class File(BaseModel):
    id: int = Field(description="The unique identifier of this file.")
    name: str = Field(description="The name of this file.")
    chunk_count: int = Field(
        alias="chunkCount", description="The number of chunks this file is split into."
    )
    delimiter: str | None = Field(None, description="The delimiter used in this file.")
    encoding: str | None = Field(None, description="The encoding of this file.")
    first_data_row: int = Field(
        alias="firstDataRow", description="The row number of the first data row in this file."
    )
    format: str | None = Field(None, description="The format of this file.")
    header_row: int = Field(
        alias="headerRow", description="The row number of the header row in this file."
    )
    separator: str | None = Field(None, description="The separator used in this file.")


class List(BaseModel):
    id: int = Field(description="The unique identifier of this list.")
    name: str = Field(description="The name of this list.")


class ListMetadata(BaseModel):
    id: int = Field(description="The unique identifier of this list.")
    name: str = Field(description="The name of this list.")
    has_selective_access: bool = Field(
        alias="hasSelectiveAccess", description="Whether this list has selective access or not."
    )
    properties: list = Field([], description="The properties of this list.")
    production_data: bool = Field(
        alias="productionData", description="Whether this list is production data or not."
    )
    managed_by: str = Field(alias="managedBy", description="The user who manages this list.")
    numbered_list: bool = Field(
        alias="numberedList", description="Whether this list is a numbered list or not."
    )
    use_top_level_as_page_default: bool = Field(
        alias="useTopLevelAsPageDefault",
        description="Whether the top level is used as the page default or not.",
    )
    item_count: int = Field(alias="itemCount", description="The number of items in this list.")
    next_item_index: int | None = Field(
        None, alias="nextItemIndex", description="The index of the next item in this list."
    )
    workflow_enabled: bool = Field(
        alias="workflowEnabled", description="Whether the workflow is enabled for this list or not."
    )
    permitted_items: int = Field(
        alias="permittedItems", description="The number of permitted items in this list."
    )
    used_in_applies_to: str | None = Field(
        None, alias="usedInAppliesTo", description="The applies to value of this list."
    )


class Action(BaseModel):
    id: int = Field(description="The unique identifier of this action.")
    name: str = Field(
        description="The name of this Action. This is the same as the one displayed in the Web UI."
    )
    type: str | None = Field(None, alias="actionType", description="The type of this action.")


class ListItem(BaseModel):
    id: int = Field(description="The unique identifier of this list item.")
    name: str = Field(description="The name of this list item.")
    code: str | None = Field(None, description="The code of this list item.")
    properties: dict = Field({}, description="The properties of this list item.")
    subsets: dict = Field({}, description="The subsets of this list item.")
    parent: str | None = Field(None, description="The parent of this list item.")
    parent_id: str | None = Field(
        None, alias="parentId", description="The unique identifier of the parent of this list item."
    )


class Process(BaseModel):
    id: int = Field(description="The unique identifier of this process.")
    name: str = Field(description="The name of this process.")


class Import(BaseModel):
    id: int = Field(description="The unique identifier of this import.")
    name: str = Field(description="The name of this import.")
    type: ImportTypes = Field(alias="importType", description="The type of this import.")
    source_id: int | None = Field(
        None,
        alias="importDataSourceId",
        description=(
            "The unique identifier of the data source of this import. This is usually a file. If "
            "it is absent, it means that the import is not a file import."
        ),
    )

    # noinspection PyNestedDecorators
    @field_validator("source_id", mode="before")
    @classmethod
    def _empty_source_is_none(cls, inp: str):
        return inp if inp else None


class Export(BaseModel):
    id: int = Field(description="The unique identifier of this export.")
    name: str = Field(description="The name of this export.")
    type: ExportTypes = Field(alias="exportType", description="The type of this export.")
    format: str = Field(alias="exportFormat", description="The format of this export.")
    encoding: str | None = Field(None, description="The encoding of this export.")
    layout: ExportTypes = Field(
        description="The layout of this export, representing the Anaplan Export Structure."
    )


class Module(BaseModel):
    id: int = Field(description="The unique identifier of this module.")
    name: str = Field(description="The name of this module.")


class ModelStatus(BaseModel):
    peak_memory_usage_estimate: int | None = Field(
        alias="peakMemoryUsageEstimate", description="The peak memory usage estimate of this model."
    )
    peak_memory_usage_time: int | None = Field(
        alias="peakMemoryUsageTime", description="The peak memory usage time of this model."
    )
    progress: float = Field(description="The progress of this model.")
    current_step: str = Field(alias="currentStep", description="The current step of this model.")
    tooltip: str | None = Field(description="The tooltip of this model.")
    task_id: str | None = Field(
        alias="taskId", description="The unique identifier of the task of this model."
    )
    creation_time: int = Field(alias="creationTime", description="The creation time of this model.")
    export_task_type: str | None = Field(
        alias="exportTaskType", description="The export task type of this model."
    )


class LineItem(BaseModel):
    id: int = Field(description="The unique identifier of this line item.")
    name: str = Field(description="The name of this line item.")
    module_id: int = Field(
        alias="moduleId",
        description="The unique identifier of the module this line item belongs to.",
    )
    module_name: str = Field(
        alias="moduleName", description="The name of the module this line item belongs to."
    )
    format: str = Field(description="The format of this line item.")
    format_metadata: dict = Field(
        alias="formatMetadata", description="The format metadata of this line item."
    )
    summary: str = Field(description="The summary of this line item.")
    applies_to: list[dict] = Field(
        [], alias="appliesTo", description="The applies to value of this line item."
    )
    time_scale: str = Field(alias="timeScale", description="The time scale of this line item.")
    time_range: str = Field(alias="timeRange", description="The time range of this line item.")
    version: dict = Field(description="The version of this line item.")
    style: str = Field(description="The style of this line item.")
    cell_count: int | None = Field(
        None, alias="cellCount", description="The cell count of this line item."
    )
    notes: str = Field(description="The notes of this line item.")
    is_summary: bool = Field(
        alias="isSummary", description="Whether this line item is a summary or not."
    )
    formula: str | None = Field(None, description="The formula of this line item.")
    formula_scope: str = Field(
        alias="formulaScope", description="The formula scope of this line item."
    )
    use_switchover: bool = Field(
        alias="useSwitchover", description="Whether the switchover is used or not."
    )
    breakback: bool = Field(description="Whether the breakback is enabled or not.")
    brought_forward: bool = Field(
        alias="broughtForward", description="Whether the brought forward is enabled or not."
    )
    start_of_section: bool = Field(
        alias="startOfSection",
        description="Whether this line item is the start of a section or not.",
    )


class Failure(BaseModel):
    index: int = Field(alias="requestIndex", description="The index of the item that failed.")
    reason: str = Field(alias="failureType", description="The reason for the failure.")
    details: str = Field(alias="failureMessageDetails", description="The details of the failure.")


class InsertionResult(BaseModel):
    added: int = Field(description="The number of items successfully added.")
    ignored: int = Field(description="The number of items ignored, or items that failed.")
    total: int = Field(description="The total number of items.")
    failures: list[Failure] = Field([], description="The list of failures.")


class Revision(BaseModel):
    id: str = Field(description="The unique identifier of this revision.")
    name: str = Field(description="The name of this revision.")
    description: str | None = Field(
        None, description="The description of this revision. Not always present."
    )
    created_on: str = Field(
        alias="createdOn", description="The creation date of this revision in ISO format."
    )
    created_by: str = Field(
        alias="createdBy",
        description="The unique identifier of the user who created this revision.",
    )
    creation_method: str = Field(
        alias="creationMethod", description="The creation method of this revision."
    )
    applied_on: str = Field(
        alias="appliedOn", description="The application date of this revision in ISO format."
    )
    applied_by: str = Field(
        alias="appliedBy",
        description="The unique identifier of the user who applied this revision.",
    )


class ModelRevision(BaseModel):
    id: str = Field(
        alias="modelId", description="The unique identifier of the model this revision belongs to."
    )
    name: str = Field(
        alias="modelName", description="The name of the model this revision belongs to."
    )
    workspace_id: str = Field(
        alias="workspaceId",
        description="The unique identifier of the workspace this revision belongs to.",
    )
    applied_by: str = Field(
        alias="appliedBy",
        description="The unique identifier of the user who applied this revision.",
    )
    applied_on: str = Field(
        alias="appliedOn", description="The application date of this revision in ISO format."
    )
    applied_method: str = Field(
        alias="appliedMethod", description="The application method of this revision."
    )
    deleted: bool | None = Field(
        None, alias="modelDeleted", description="Whether the model has been deleted or not."
    )


class SyncTask(BaseModel):
    task_id: str = Field(alias="taskId", description="The unique identifier of this task.")
    task_state: str = Field(alias="taskState", description="The state of this task.")
    creation_time: int = Field(alias="creationTime", description="The creation time of this task.")


class User(BaseModel):
    id: str = Field(description="The unique identifier of this user.")
    active: bool = Field(description="Whether this user is active or not.")
    email: str = Field(description="The email address of this user.")
    email_opt_in: bool = Field(
        alias="emailOptIn", description="Whether this user has opted in to receive emails or not."
    )
    first_name: str = Field(alias="firstName", description="The first name of this user.")
    last_name: str = Field(alias="lastName", description="The last name of this user.")
    last_login_date: str | None = Field(
        None, alias="lastLoginDate", description="The last login date of this user in ISO format."
    )
