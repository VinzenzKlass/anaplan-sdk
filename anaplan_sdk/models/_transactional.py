from pydantic import Field

from ._base import AnaplanModel


class User(AnaplanModel):
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


class ListItem(AnaplanModel):
    id: int = Field(description="The unique identifier of this list item.")
    name: str = Field(description="The name of this list item.")
    code: str | None = Field(None, description="The code of this list item.")
    properties: dict = Field({}, description="The properties of this list item.")
    subsets: dict = Field({}, description="The subsets of this list item.")
    parent: str | None = Field(None, description="The parent of this list item.")
    parent_id: str | None = Field(
        None, description="The unique identifier of the parent of this list item."
    )


class Module(AnaplanModel):
    id: int = Field(description="The unique identifier of this module.")
    name: str = Field(description="The name of this module.")


class LineItem(AnaplanModel):
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


class Failure(AnaplanModel):
    index: int = Field(
        validation_alias="requestIndex", description="The index of the item that failed."
    )
    reason: str = Field(validation_alias="failureType", description="The reason for the failure.")
    details: str = Field(
        validation_alias="failureMessageDetails", description="The details of the failure."
    )


class ModelStatus(AnaplanModel):
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


class InsertionResult(AnaplanModel):
    added: int = Field(description="The number of items successfully added.")
    ignored: int = Field(description="The number of items ignored, or items that failed.")
    total: int = Field(description="The total number of items.")
    failures: list[Failure] = Field([], description="The list of failures.")
