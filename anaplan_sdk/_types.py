from dataclasses import dataclass


@dataclass
class Import:
    id: int
    name: str
    type: str
    source_id: int | None


@dataclass
class Export:
    id: int
    name: str
    type: str
    format: str
    encoding: str
    layout: str


@dataclass
class Action:
    id: int
    name: str
    type: str


@dataclass
class Process:
    id: int
    name: str


@dataclass
class File:
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
    id: int
    name: str
