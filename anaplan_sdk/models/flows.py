from datetime import datetime
from typing import Literal

from pydantic import Field

from ._base import AnaplanModel
from .cloud_works import _BaseIntegration  # pyright: ignore[reportPrivateUsage]


class FlowSummary(_BaseIntegration):
    id: str = Field(description="The unique identifier of this flow.")
    steps_count: int = Field(description="The number of steps in this flow.")


class ExceptionBehavior(AnaplanModel):
    type: Literal["failure", "partial_success"] = Field(
        description="The type of exception that this behavior applies to."
    )
    strategy: Literal["stop", "continue"] = Field(
        description="The strategy to handle the exception."
    )


class FlowStep(AnaplanModel):
    referrer: str = Field(
        description="The unique identifier of the referenced step or integration."
    )
    name: str = Field(description="The name of this flow step.")
    type: Literal["Process", "Import", "Export"] = Field(description="The type of this flow step.")
    created_by: str = Field(description="The user who created this step.")
    created_date: datetime = Field(description="The initial creation date of this step.")
    modified_date: datetime = Field(description="The last modification date of this step.")
    modified_by: str | None = Field(
        default=None, description="The user who last modified this step."
    )
    model_id: str = Field(description="The ID of the model this step belongs to.")
    workspace_id: str = Field(description="The ID of the workspace this step belongs to.")
    depends_on: list[str] | None = Field(
        default=[], description="The IDs of steps that this step depends on."
    )
    is_skipped: bool = Field(description="Whether this step is skipped during execution.")
    exception_behavior: list[ExceptionBehavior] = Field(
        description="Configuration for handling exceptions during step execution."
    )


class Flow(FlowSummary):
    version: Literal["2.0"] = Field(default="2.0", description="The version of this flow.")
    nux_visible: bool = Field(description="Whether this integration is visible in the UI.")
    steps: list[FlowStep] = Field(default=[], description="The steps in this flow.")


class FlowStepInput(AnaplanModel):
    type: Literal["Integration"] = Field(
        default="Integration", description="The type of this flow step."
    )
    referrer: str = Field(
        description="The unique identifier of the referenced step or integration."
    )
    depends_on: list[str] | None = Field(
        default=None, description="The IDs of steps that this step depends on."
    )
    is_skipped: bool = Field(
        default=False, description="Whether this step is skipped during execution."
    )
    exception_behavior: list[ExceptionBehavior] = Field(
        default=[
            ExceptionBehavior(type="failure", strategy="stop"),
            ExceptionBehavior(type="partial_success", strategy="continue"),
        ],
        description=(
            "Configuration for handling exceptions during step execution. Defaults to stopping on "
            "Failure and continuing on Partial Success."
        ),
    )


class FlowInput(AnaplanModel):
    name: str = Field(description="The name of this flow.")
    version: Literal["2.0"] = Field(default="2.0", description="The version of this flow.")
    type: Literal["IntegrationFlow"] = Field(
        default="IntegrationFlow", description="The type of this flow."
    )
    steps: list[FlowStepInput] = Field(
        description="The steps in this flow.", min_length=2, max_length=100
    )
