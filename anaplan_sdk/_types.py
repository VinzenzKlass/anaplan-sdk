from dataclasses import dataclass


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
    delimiter: str
    encoding: str
    first_data_row: int
    format: str
    header_row: int
    separator: str


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
