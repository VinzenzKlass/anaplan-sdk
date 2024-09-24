from pydantic import BaseModel, Field, field_validator


class Workspace(BaseModel):
    id: str
    """The unique identifier of this workspace."""
    name: str
    """The name of this workspace that is also displayed to the users. This can change any time."""
    active: bool
    """Whether this workspace is active or not."""
    size_allowance: int = Field(alias="sizeAllowance", ge=0)
    """The maximum allowed size of this workspace in bytes."""
    current_size: int = Field(alias="currentSize", ge=0)
    """The current size of this workspace in bytes."""


class Model(BaseModel):
    id: str
    """The unique identifier of this model."""
    name: str
    """The name of this model that is also displayed to the users. This can change any time."""
    active_state: str = Field(alias="activeState")
    """The current state of this model. One of "ARCHIVED", "UNLOCKED", "ACTIVE"."""
    last_saved_serial_number: int = Field(alias="lastSavedSerialNumber")
    """The serial number of the last save of this model."""
    last_modified_by_user_guid: str = Field(alias="lastModifiedByUserGuid")
    """The unique identifier of the user who last modified this model."""
    memory_usage: int | None = Field(None, alias="memoryUsage")
    """The memory usage of this model in bytes."""
    current_workspace_id: str = Field(alias="currentWorkspaceId")
    """The unique identifier of the workspace that this model is currently in."""
    current_workspace_name: str = Field(alias="currentWorkspaceName")
    """The name of the workspace that this model is currently in."""
    url: str = Field(alias="modelUrl")
    """The URL of this model."""
    category_values: list = Field(alias="categoryValues")
    """The category values of this model."""
    iso_creation_date: str = Field(alias="isoCreationDate")
    """The creation date of this model in ISO format."""
    last_modified: str = Field(alias="lastModified")
    """The last modified date of this model in ISO format."""


class File(BaseModel):
    id: int
    """The unique identifier of this file."""
    name: str
    """The name of this file."""
    chunk_count: int = Field(alias="chunkCount")
    """The number of chunks this file is split into."""
    delimiter: str | None = Field(None)
    """The delimiter used in this file."""
    encoding: str | None = Field(None)
    """The encoding of this file."""
    first_data_row: int = Field(alias="firstDataRow")
    """The row number of the first data row in this file."""
    format: str | None = Field(None)
    """The format of this file."""
    header_row: int = Field(alias="headerRow")
    """The row number of the header row in this file."""
    separator: str | None = Field(None)
    """The separator used in this file."""


class List(BaseModel):
    id: int
    """The unique identifier of this list."""
    name: str
    """The name of this list."""


class ListMetadata(BaseModel):
    id: int
    """The unique identifier of this list."""
    name: str
    """The name of this list."""
    has_selective_access: bool = Field(alias="hasSelectiveAccess")
    """Whether this list has selective access or not."""
    properties: list = Field([])
    """The properties of this list."""
    production_data: bool = Field(alias="productionData")
    """Whether this list is production data or not."""
    managed_by: str = Field(alias="managedBy")
    """The user who manages this list."""
    numbered_list: bool = Field(alias="numberedList")
    """Whether this list is a numbered list or not."""
    use_top_level_as_page_default: bool = Field(alias="useTopLevelAsPageDefault")
    """Whether the top level is used as the page default or not."""
    item_count: int = Field(alias="itemCount")
    """The number of items in this list."""
    next_item_index: int | None = Field(None, alias="nextItemIndex")
    """The index of the next item in this list."""
    workflow_enabled: bool = Field(alias="workflowEnabled")
    """Whether the workflow is enabled for this list or not."""
    permitted_items: int = Field(alias="permittedItems")
    """The number of permitted items in this list."""
    used_in_applies_to: str | None = Field(None, alias="usedInAppliesTo")
    """The applies to value of this list."""


class ListItem(BaseModel):
    id: int
    """The unique identifier of this list item."""
    name: str
    """The name of this list item."""
    code: str | None = Field(None)
    """The code of this list item."""
    properties: dict = Field({})
    """The properties of this list item."""
    subsets: dict = Field({})
    """The subsets of this list item."""
    parent: str | None = Field(None)
    """The parent of this list item."""
    parent_id: str | None = Field(None, alias="parentId")
    """The unique identifier of the parent of this list item."""


class Action(BaseModel):
    id: int
    """The unique identifier of this action."""
    name: str
    """The name of this action."""
    type: str = Field(alias="actionType")
    """The type of this action."""


class Process(BaseModel):
    id: int
    """The unique identifier of this process."""
    name: str
    """The name of this process."""


class Import(BaseModel):
    id: int
    """The unique identifier of this import."""
    name: str
    """The name of this import."""
    type: str = Field(alias="importType")
    """The type of this import."""
    source_id: int | None = Field(None, alias="importDataSourceId")
    """The unique identifier of the data source of this import."""

    # noinspection PyNestedDecorators
    @field_validator("source_id", mode="before")
    @classmethod
    def _empty_source_is_none(cls, inp: str):
        return inp if inp else None


class Export(BaseModel):
    id: int
    """The unique identifier of this export."""
    name: str
    """The name of this export."""
    type: str = Field(alias="exportType")
    """The type of this export."""
    format: str = Field(alias="exportFormat")
    """The format of this export."""
    encoding: str
    """The encoding of this export."""
    layout: str
    """The layout of this export. Will hold values such as `GRID_CURRENT_PAGE` 
    and `TABULAR_ALL_LINE_ITEMS`, representing the Anaplan Export Structure.
    """


class Module(BaseModel):
    id: int
    """The unique identifier of this module."""
    name: str
    """The name of this module."""


class ModelStatus(BaseModel):
    peak_memory_usage_estimate: int | None = Field(alias="peakMemoryUsageEstimate")
    """The peak memory usage estimate of this model."""
    peak_memory_usage_time: int | None = Field(alias="peakMemoryUsageTime")
    """The peak memory usage time of this model."""
    progress: float
    """The progress of this model."""
    current_step: str = Field(alias="currentStep")
    """The current step of this model."""
    tooltip: str | None
    """The tooltip of this model."""
    task_id: str | None = Field(alias="taskId")
    """The unique identifier of the task of this model."""
    creation_time: int = Field(alias="creationTime")
    """The creation time of this model."""
    export_task_type: str | None = Field(alias="exportTaskType")
    """The export task type of this model."""


class LineItem(BaseModel):
    id: int
    """The unique identifier of this line item."""
    name: str
    """The name of this line item."""
    module_id: int = Field(alias="moduleId")
    """The unique identifier of the module this line item belongs to."""
    module_name: str = Field(alias="moduleName")
    """The name of the module this line item belongs to."""
    format: str
    """The format of this line item."""
    format_metadata: dict = Field(alias="formatMetadata")
    """The format metadata of this line item."""
    summary: str
    """The summary of this line item."""
    applies_to: list[dict] = Field([], alias="appliesTo")
    """The applies to value of this line item."""
    time_scale: str = Field(alias="timeScale")
    """The time scale of this line item."""
    time_range: str = Field(alias="timeRange")
    """The time range of this line item."""
    version: dict
    """The version of this line item."""
    style: str
    """The style of this line item."""
    cell_count: int | None = Field(None, alias="cellCount")
    """The cell count of this line item."""
    notes: str
    """The notes of this line item."""
    is_summary: bool = Field(alias="isSummary")
    """Whether this line item is a summary or not."""
    formula: str | None = Field(None)
    """The formula of this line item."""
    formula_scope: str = Field(alias="formulaScope")
    """The formula scope of this line item."""
    use_switchover: bool = Field(alias="useSwitchover")
    """Whether the switchover is used or not."""
    breakback: bool
    """Whether the breakback is enabled or not."""
    brought_forward: bool = Field(alias="broughtForward")
    """Whether the brought forward is enabled or not."""
    start_of_section: bool = Field(alias="startOfSection")
    """Whether this line item is the start of a section or not."""


class Failure(BaseModel):
    index: int = Field(alias="requestIndex")
    """The index of the item that failed."""
    reason: str = Field(alias="failureType")
    """The reason for the failure."""
    details: str = Field(alias="failureMessageDetails")
    """The details of the failure."""


class InsertionResult(BaseModel):
    added: int
    """The number of items successfully added."""
    ignored: int
    """The number of items ignored, or items that failed."""
    total: int
    """The total number of items."""
    failures: list[Failure] = Field([])
    """The list of failures."""


class Revision(BaseModel):
    id: str
    """The unique identifier of this revision."""
    name: str
    """The name of this revision."""
    description: str | None = Field(None)
    """The description of this revision. Not always present."""
    created_on: str = Field(alias="createdOn")
    """The creation date of this revision in ISO format."""
    created_by: str = Field(alias="createdBy")
    """The unique identifier of the user who created this revision."""
    creation_method: str = Field(alias="creationMethod")
    """The creation method of this revision."""
    applied_on: str = Field(alias="appliedOn")
    """The application date of this revision in ISO format."""
    applied_by: str = Field(alias="appliedBy")
    """The unique identifier of the user who applied this revision."""


class ModelRevision(BaseModel):
    id: str = Field(alias="modelId")
    """The unique identifier of the model this revision belongs to."""
    name: str = Field(alias="modelName")
    """The name of the model this revision belongs to."""
    workspace_id: str = Field(alias="workspaceId")
    """The unique identifier of the workspace this revision belongs to."""
    applied_by: str = Field(alias="appliedBy")
    """The unique identifier of the user who applied this revision."""
    applied_on: str = Field(alias="appliedOn")
    """The application date of this revision in ISO format."""
    applied_method: str = Field(alias="appliedMethod")
    """The application method of this revision."""
    deleted: bool | None = Field(None, alias="modelDeleted")
    """Whether the model has been deleted or not."""


class SyncTask(BaseModel):
    task_id: str = Field(alias="taskId")
    """The unique identifier of this task."""
    task_state: str = Field(alias="taskState")
    """The state of this task."""
    creation_time: int = Field(alias="creationTime")
    """The creation time of this task."""


class User(BaseModel):
    id: str
    """The unique identifier of this user."""
    active: bool
    """Whether this user is active or not."""
    email: str
    """The email address of this user."""
    email_opt_in: bool = Field(alias="emailOptIn")
    """Whether this user has opted in to receive emails or not."""
    first_name: str = Field(alias="firstName")
    """The first name of this user."""
    last_name: str = Field(alias="lastName")
    """The last name of this user."""
    last_login_date: str | None = Field(None, alias="lastLoginDate")
    """The last login date of this user in ISO format."""
