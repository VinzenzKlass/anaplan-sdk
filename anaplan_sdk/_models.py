from dataclasses import dataclass

from ._exceptions import InvalidIdentifierException


@dataclass
class Import:
    """
    Object representing an Anaplan Import.
    """

    id: int
    name: str
    type: str
    source_id: int | None


@dataclass
class Export:
    """
    Object representing an Anaplan Export.
    """

    id: int
    name: str
    type: str
    format: str
    encoding: str
    layout: str


@dataclass
class Action:
    """
    Object representing an Anaplan Action.
    """

    id: int
    name: str
    type: str


@dataclass
class Process:
    """
    Object representing an Anaplan Process.
    """

    id: int
    name: str


@dataclass
class File:
    """
    Object representing an Anaplan File.
    """

    id: int
    name: str
    chunk_count: int
    delimiter: str | None
    encoding: str | None
    first_data_row: int
    format: str | None
    header_row: int
    separator: str | None


@dataclass
class List:
    """
    Object representing an Anaplan List.
    """

    id: int
    name: str


@dataclass
class Workspace:
    """
    Object representing an Anaplan Workspace.
    """

    id: str
    name: str
    active: str
    size_allowance: int
    current_size: int


@dataclass
class Model:
    """
    Object representing an Anaplan Model.
    """

    id: str
    name: str
    active_state: str
    last_saved_serial_number: int
    last_modified_by_user_guid: str
    memory_usage: int
    current_workspace_id: str
    current_workspace_name: str
    model_url: str
    category_values: list
    iso_creation_date: str
    last_modified: str


def to_imports(response: dict[str, float | int | str | list | dict | bool]) -> list[Import]:
    return [
        Import(
            id=int(e.get("id")),
            type=e.get("importType"),
            name=e.get("name"),
            source_id=int(e.get("importDataSourceId")) if e.get("importDataSourceId") else None,
        )
        for e in response.get("imports")
    ]


def to_exports(response: dict[str, float | int | str | list | dict | bool]) -> list[Export]:
    return [
        Export(
            id=int(e.get("id")),
            name=e.get("name"),
            type=e.get("exportType"),
            format=e.get("exportFormat"),
            encoding=e.get("encoding"),
            layout=e.get("layout"),
        )
        for e in response.get("exports")
    ]


def to_actions(response: dict[str, float | int | str | list | dict | bool]) -> list[Action]:
    return [
        Action(id=int(e.get("id")), name=e.get("name"), type=e.get("actionType"))
        for e in response.get("actions")
    ]


def to_processes(response: dict[str, float | int | str | list | dict | bool]) -> list[Process]:
    return [Process(id=int(e.get("id")), name=e.get("name")) for e in response.get("processes")]


def to_files(response: dict[str, float | int | str | list | dict | bool]) -> list[File]:
    return [
        File(
            id=int(e.get("id")),
            name=e.get("name"),
            chunk_count=e.get("chunkCount"),
            delimiter=e.get("delimiter"),
            encoding=e.get("encoding"),
            first_data_row=e.get("firstDataRow"),
            format=e.get("format"),
            header_row=e.get("headerRow"),
            separator=e.get("separator"),
        )
        for e in response.get("files")
    ]


def to_lists(response: dict[str, float | int | str | list | dict | bool]) -> list[List]:
    return [List(id=int(e.get("id")), name=e.get("name")) for e in response.get("lists")]


def to_workspaces(response: dict[str, float | int | str | list | dict | bool]) -> list[Workspace]:
    return [
        Workspace(
            id=e.get("id"),
            name=e.get("name"),
            active=e.get("active"),
            size_allowance=int(e.get("sizeAllowance")),
            current_size=int(e.get("currentSize")),
        )
        for e in response.get("workspaces")
    ]


def to_models(response: dict[str, float | int | str | list | dict | bool]) -> list[Model]:
    return [
        Model(
            id=e.get("id"),
            name=e.get("name"),
            active_state=e.get("activeState"),
            last_saved_serial_number=int(e.get("lastSavedSerialNumber")),
            last_modified_by_user_guid=e.get("lastModifiedByUserGuid"),
            memory_usage=int(e.get("memoryUsage", 0)),
            current_workspace_id=e.get("currentWorkspaceId"),
            current_workspace_name=e.get("currentWorkspaceName"),
            model_url=e.get("modelUrl"),
            category_values=e.get("categoryValues"),
            iso_creation_date=e.get("isoCreationDate"),
            last_modified=e.get("lastModified"),
        )
        for e in response.get("models")
    ]


def determine_action_type(action_id: int) -> str:
    if 12000000000 <= action_id < 113000000000:
        return "imports"
    if 116000000000 <= action_id < 117000000000:
        return "exports"
    if 117000000000 <= action_id < 118000000000:
        return "actions"
    if 118000000000 <= action_id < 119000000000:
        return "processes"
    raise InvalidIdentifierException(f"Action '{action_id}' is not a valid identifier.")
