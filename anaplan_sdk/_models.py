from pydantic import BaseModel, Field, field_validator

from ._exceptions import InvalidIdentifierException


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


class ModelStatus(BaseModel):
    peak_memory_usage_estimate: int = Field(alias="peakMemoryUsageEstimate")
    peak_memory_usage_time: int = Field(alias="peakMemoryUsageTime")
    progress: float
    current_step: str = Field(alias="currentStep")
    tooltip: str
    task_id: str = Field(alias="taskId")
    creation_time: int = Field(alias="creationTime")
    export_task_type: str = Field(alias="exportTaskType")


def determine_action_type(action_id: int) -> str:
    """
    Determine the type of action based on its identifier.
    :param action_id: The identifier of the action.]
    :return: The type of action.
    """
    if 12000000000 <= action_id < 113000000000:
        return "imports"
    if 116000000000 <= action_id < 117000000000:
        return "exports"
    if 117000000000 <= action_id < 118000000000:
        return "actions"
    if 118000000000 <= action_id < 119000000000:
        return "processes"
    raise InvalidIdentifierException(f"Action '{action_id}' is not a valid identifier.")
