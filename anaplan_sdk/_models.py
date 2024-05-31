from pydantic import BaseModel, Field, field_validator

from ._exceptions import InvalidIdentifierException


class Workspace(BaseModel):
    """
    Object representing an Anaplan Workspace.
    """

    id: str
    name: str
    active: bool
    size_allowance: int = Field(alias="sizeAllowance", ge=0)
    current_size: int = Field(alias="currentSize", ge=0)


class Model(BaseModel):
    """
    Object representing an Anaplan Model.
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
    """

    id: int
    name: str


class Action(BaseModel):
    """
    Object representing an Anaplan Action.
    """

    id: int
    name: str
    type: str = Field(alias="actionType")


class Process(BaseModel):
    """
    Object representing an Anaplan Process.
    """

    id: int
    name: str


class Import(BaseModel):
    """
    Object representing an Anaplan Import.
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
    """

    id: int
    name: str
    type: str = Field(alias="exportType")
    format: str = Field(alias="exportFormat")
    encoding: str
    layout: str


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
