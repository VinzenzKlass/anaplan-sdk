from pydantic import Field, ConfigDict
from pydantic.alias_generators import to_camel

from ._base import AnaplanModel


class Entitlement(AnaplanModel):
    value: str = Field(description="Workspace ID(s) or names for this entitlement.")
    display: str | None = Field(None, description="Optional name of a Workspace.")
    type: str = Field(description="The type of identifier used as the entitlement value.")
    primary: bool | None = Field(None, description="First item, ignored by Anaplan.")


class UserScim(AnaplanModel):
    schemas: list = Field(description="Schemas for this user object.")
    id: str = Field(description="The unique identifier of this revision.")
    external_id: str | None = Field(
        None, validation_alias="externalId", description="The unique identifier of this revision."
    )
    active: bool = Field(description="True when user is enabled.")
    user_name: str = Field(validation_alias="userName", description="The name by which this user is known within Anaplan.")
    meta: dict = Field({}, description="Information about this resource.")
    name: dict = Field({}, description="The components of users personal name.")
    display_name: str = Field(validation_alias="displayName", description="The users personal name.")
    entitlements: list[Entitlement] = Field([], description="The workspaces for this user.")
