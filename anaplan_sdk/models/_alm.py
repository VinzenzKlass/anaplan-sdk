from pydantic import Field

from ._base import AnaplanModel


class Revision(AnaplanModel):
    id: str = Field(description="The unique identifier of this revision.")
    name: str = Field(description="The name of this revision.")
    description: str | None = Field(
        None, description="The description of this revision. Not always present."
    )
    created_on: str = Field(description="The creation date of this revision in ISO format.")
    created_by: str = Field(
        description="The unique identifier of the user who created this revision."
    )
    creation_method: str = Field(description="The creation method of this revision.")
    applied_on: str = Field(description="The application date of this revision in ISO format.")
    applied_by: str = Field(
        description="The unique identifier of the user who applied this revision."
    )


class ModelRevision(AnaplanModel):
    id: str = Field(
        validation_alias="modelId",
        description="The unique identifier of the model this revision belongs to.",
    )
    name: str = Field(
        default="",
        validation_alias="modelName",
        description=(
            "The name of the model this revision belongs to. This can be an empty string, when the "
            "calling user does not have access to the model, but is workspace admin in the "
            "workspace."
        ),
    )
    workspace_id: str = Field(
        description="The unique identifier of the workspace this revision belongs to."
    )
    applied_by: str = Field(
        description="The unique identifier of the user who applied this revision."
    )
    applied_on: str = Field(description="The application date of this revision in ISO format.")
    applied_method: str = Field(description="The application method of this revision.")
    deleted: bool | None = Field(
        None,
        validation_alias="modelDeleted",
        description="Whether the model has been deleted or not.",
    )


class SyncTask(AnaplanModel):
    id: str = Field(validation_alias="taskId", description="The unique identifier of this task.")
    task_state: str = Field(description="The state of this task.")
    creation_time: int = Field(description="The creation time of this task.")
