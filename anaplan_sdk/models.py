from pydantic import BaseModel, Field, field_validator


class Workspace(BaseModel):
    """
    Object representing an Anaplan Workspace.

    **id (str):** The unique identifier of this workspace.

    **name (str):** The name of this workspace that is also displayed to the users. This can
    change any time.

    **active (bool):** Whether this workspace is active or not.

    **size_allowance (int):** The maximum allowed size of this workspace in bytes.

    **current_size (int):** The current size of this workspace in bytes.
    """

    id: str
    name: str
    active: bool
    size_allowance: int = Field(alias="sizeAllowance", ge=0)
    current_size: int = Field(alias="currentSize", ge=0)


class Model(BaseModel):
    """
    Object representing an Anaplan Model.

    **id (str):** The unique identifier of this model.

    **name (str):** The name of this model that is also displayed to the users. This can
    change any time.

    **active_state (str):** The current state of this model. One of "ARCHIVED", "UNLOCKED", "ACTIVE"

    **last_saved_serial_number (int):** The serial number of the last save of this model.

    **last_modified_by_user_guid (str):** The unique identifier of the user who last modified this
    model.

    **memory_usage (int):** The memory usage of this model in bytes.

    **current_workspace_id (str):** The unique identifier of the workspace that this model is
    currently in.

    **current_workspace_name (str):** The name of the workspace that this model is currently in.

    **url (str):** The URL of this model.

    **category_values (list):** The category values of this model.

    **iso_creation_date (str):** The creation date of this model in ISO format.

    **last_modified (str):** The last modified date of this model in ISO format.
    """

    id: str
    name: str
    active_state: str = Field(alias="activeState")
    last_saved_serial_number: int = Field(alias="lastSavedSerialNumber")
    last_modified_by_user_guid: str = Field(alias="lastModifiedByUserGuid")
    memory_usage: int | None = Field(None, alias="memoryUsage")
    current_workspace_id: str = Field(alias="currentWorkspaceId")
    current_workspace_name: str = Field(alias="currentWorkspaceName")
    url: str = Field(alias="modelUrl")
    category_values: list = Field(alias="categoryValues")
    iso_creation_date: str = Field(alias="isoCreationDate")
    last_modified: str = Field(alias="lastModified")


class File(BaseModel):
    """
    Object representing an Anaplan File.

    **id (int):** The unique identifier of this file.

    **name (str):** The name of this file.

    **chunk_count (int):** The number of chunks this file is split into.

    **delimiter (str):** The delimiter used in this file.

    **encoding (str):** The encoding of this file.

    **first_data_row (int):** The row number of the first data row in this file.

    **format (str):** The format of this file.

    **header_row (int):** The row number of the header row in this file.

    **separator (str):** The separator used in this file.
    """

    id: int
    name: str
    chunk_count: int = Field(alias="chunkCount")
    delimiter: str | None = Field(None)
    encoding: str | None = Field(None)
    first_data_row: int = Field(alias="firstDataRow")
    format: str | None = Field(None)
    header_row: int = Field(alias="headerRow")
    separator: str | None = Field(None)


class List(BaseModel):
    """
    Object representing an Anaplan List.

    **id (int):** The unique identifier of this list.

    **name (str):** The name of this list.
    """

    id: int
    name: str


class ListMetadata(BaseModel):
    """
    Object representing the metadata of an Anaplan List.

    **id (int):** The unique identifier of this list.

    **name (str):** The name of this list.

    **has_selective_access (bool):** Whether this list has selective access or not.

    **properties (list):** The properties of this list.

    **production_data (bool):** Whether this list is production data or not.

    **managed_by (str):** The user who manages this list.

    **numbered_list (bool):** Whether this list is a numbered list or not.

    **use_top_level_as_page_default (bool):** Whether the top level is used as the page default
    or not.

    **item_count (int):** The number of items in this list.

    **next_item_index (int):** The index of the next item in this list.

    **workflow_enabled (bool):** Whether the workflow is enabled for this list or not.

    **permitted_items (int):** The number of permitted items in this list.

    **used_in_applies_to (str):** The applies to value of this list.
    """

    id: int
    name: str
    has_selective_access: bool = Field(alias="hasSelectiveAccess")
    properties: list = Field([])
    production_data: bool = Field(alias="productionData")
    managed_by: str = Field(alias="managedBy")
    numbered_list: bool = Field(alias="numberedList")
    use_top_level_as_page_default: bool = Field(alias="useTopLevelAsPageDefault")
    item_count: int = Field(alias="itemCount")
    next_item_index: int | None = Field(None, alias="nextItemIndex")
    workflow_enabled: bool = Field(alias="workflowEnabled")
    permitted_items: int = Field(alias="permittedItems")
    used_in_applies_to: str | None = Field(None, alias="usedInAppliesTo")


class ListItem(BaseModel):
    """
    Object representing an Anaplan List Item.

    **id (int):** The unique identifier of this list item.

    **name (str):** The name of this list item.

    **code (str):** The code of this list item.

    **properties (dict):** The properties of this list item.

    **subsets (dict):** The subsets of this list item.

    **parent (str):** The parent of this list item.

    **parent_id (str):** The unique identifier of the parent of this list item.
    """

    id: int
    name: str
    code: str | None = Field(None)
    properties: dict = Field({})
    subsets: dict = Field({})
    parent: str | None = Field(None)
    parent_id: str | None = Field(None, alias="parentId")


class Action(BaseModel):
    """
    Object representing an Anaplan Action.

    **id (int):** The unique identifier of this action.

    **name (str):** The name of this action.

    **type (str):** The type of this action.
    """

    id: int
    name: str
    type: str = Field(alias="actionType")


class Process(BaseModel):
    """
    Object representing an Anaplan Process.

    **id (int):** The unique identifier of this process.

    **name (str):** The name of this process.
    """

    id: int
    name: str


class Import(BaseModel):
    """
    Object representing an Anaplan Import.

    **id (int):** The unique identifier of this import.

    **name (str):** The name of this import.

    **type (str):** The type of this import.

    **source_id (int):** The unique identifier of the data source of this import.
    """

    id: int
    name: str
    type: str = Field(alias="importType")
    source_id: int | None = Field(None, alias="importDataSourceId")

    # noinspection PyNestedDecorators
    @field_validator("source_id", mode="before")
    @classmethod
    def _empty_source_is_none(cls, inp: str):
        return inp if inp else None


class Export(BaseModel):
    """
    Object representing an Anaplan Export.

    **id (int):** The unique identifier of this export.

    **name (str):** The name of this export.

    **type (str):** The type of this export.

    **format (str):** The format of this export.

    **encoding (str):** The encoding of this export.

    **layout (str):** The layout of this export.
    """

    id: int
    name: str
    type: str = Field(alias="exportType")
    format: str = Field(alias="exportFormat")
    encoding: str
    layout: str


class Module(BaseModel):
    """
    Object representing an Anaplan Module.

    **id (int):** The unique identifier of this module.

    **name (str):** The name of this module.
    """

    id: int
    name: str


class ModelStatus(BaseModel):
    """
    Object representing the status of an Anaplan Model.

    **peak_memory_usage_estimate (int):** The peak memory usage estimate of this model.

    **peak_memory_usage_time (int):** The peak memory usage time of this model.

    **progress (float):** The progress of this model.

    **current_step (str):** The current step of this model.

    **tooltip (str):** The tooltip of this model.

    **task_id (str):** The unique identifier of the task of this model.

    **creation_time (int):** The creation time of this model.

    **export_task_type (str):** The export task type of this model.
    """

    peak_memory_usage_estimate: int | None = Field(alias="peakMemoryUsageEstimate")
    peak_memory_usage_time: int | None = Field(alias="peakMemoryUsageTime")
    progress: float
    current_step: str = Field(alias="currentStep")
    tooltip: str | None
    task_id: str | None = Field(alias="taskId")
    creation_time: int = Field(alias="creationTime")
    export_task_type: str | None = Field(alias="exportTaskType")


class LineItem(BaseModel):
    """
    Object representing an Anaplan Line Item.

    **id (int):** The unique identifier of this line item.

    **name (str):** The name of this line item.

    **module_id (int):** The unique identifier of the module this line item belongs to.

    **module_name (str):** The name of the module this line item belongs to.

    **format (str):** The format of this line item.

    **format_metadata (dict):** The format metadata of this line item.

    **summary (str):** The summary of this line item.

    **applies_to (list):** The applies to value of this line item.

    **time_scale (str):** The time scale of this line item.

    **time_range (str):** The time range of this line item.

    **version (dict):** The version of this line item.

    **style (str):** The style of this line item.

    **cell_count (int):** The cell count of this line item.

    **notes (str):** The notes of this line item.

    **is_summary (bool):** Whether this line item is a summary or not.

    **formula (str):** The formula of this line item.

    **formula_scope (str):** The formula scope of this line item.

    **use_switchover (bool):** Whether the switchover is used or not.

    **breakback (bool):** Whether the breakback is enabled or not.

    **brought_forward (bool):** Whether the brought forward is enabled or not.

    **start_of_section (bool):** Whether this line item is the start of a section or not.
    """

    id: int
    name: str
    module_id: int = Field(alias="moduleId")
    module_name: str = Field(alias="moduleName")
    format: str
    format_metadata: dict = Field(alias="formatMetadata")
    summary: str
    applies_to: list[dict] = Field([], alias="appliesTo")
    time_scale: str = Field(alias="timeScale")
    time_range: str = Field(alias="timeRange")
    version: dict
    style: str
    cell_count: int | None = Field(None, alias="cellCount")
    notes: str
    is_summary: bool = Field(alias="isSummary")
    formula: str | None = Field(None)
    formula_scope: str = Field(alias="formulaScope")
    use_switchover: bool = Field(alias="useSwitchover")
    breakback: bool
    brought_forward: bool = Field(alias="broughtForward")
    start_of_section: bool = Field(alias="startOfSection")


class Failure(BaseModel):
    """
    Object representing a failure in an Anaplan import or export.

    **index (int):** The index of the item that failed.

    **reason (str):** The reason for the failure.

    **details (str):** The details of the failure.
    """

    index: int = Field(alias="requestIndex")
    reason: str = Field(alias="failureType")
    details: str = Field(alias="failureMessageDetails")


class InsertionResult(BaseModel):
    """
    Object representing the result of an insertion in an Anaplan list.

    **added (int):** The number of items successfully added.

    **ignored (int):** The number of items ignored, or items that failed.

    **total (int):** The total number of items.

    **failures (list):** The list of failures.
    """

    added: int
    ignored: int
    total: int
    failures: list[Failure] = Field([])


class Revision(BaseModel):
    """
    Object representing an Anaplan revision.

    **id (str):** The unique identifier of this revision.

    **name (str):** The name of this revision.

    **description (str):** The description of this revision. Not always present.

    **created_on (str):** The creation date of this revision in ISO format.

    **created_by (str):** The unique identifier of the user who created this revision.

    **creation_method (str):** The creation method of this revision.

    **applied_on (str):** The application date of this revision in ISO format.

    **applied_by (str):** The unique identifier of the user who applied this revision.
    """

    id: str
    name: str
    description: str | None = Field(None)
    created_on: str = Field(alias="createdOn")
    created_by: str = Field(alias="createdBy")
    creation_method: str = Field(alias="creationMethod")
    applied_on: str = Field(alias="appliedOn")
    applied_by: str = Field(alias="appliedBy")


class ModelRevision(BaseModel):
    """
    Object representing a Model Revision in Anaplan.

    **model_id (str):** The unique identifier of the model this revision belongs to.

    **model_name (str):** The name of the model this revision belongs to.

    **workspace_id (str):** The unique identifier of the workspace this revision belongs to.

    **applied_by (str):** The unique identifier of the user who applied this revision.

    **applied_on (str):** The application date of this revision in ISO format.

    **applied_method (str):** The application method of this revision.

    **model_deleted (bool):** Whether the model has been deleted or not.
    """

    id: str = Field(alias="modelId")
    """The unique identifier of the model this revision belongs to."""
    name: str = Field(alias="modelName")
    workspace_id: str = Field(alias="workspaceId")
    applied_by: str = Field(alias="appliedBy")
    applied_on: str = Field(alias="appliedOn")
    applied_method: str = Field(alias="appliedMethod")
    deleted: bool | None = Field(None, alias="modelDeleted")


class SyncTask(BaseModel):
    """
    Object representing a sync task in Anaplan.

    **task_id (str):** The unique identifier of this task.

    **task_state (str):** The state of this task.

    **creation_time (int):** The creation time of this task.
    """

    task_id: str = Field(alias="taskId")
    task_state: str = Field(alias="taskState")
    creation_time: int = Field(alias="creationTime")
