from typing import Any, Literal, TypeAlias

from pydantic import Field

from anaplan_sdk.models import AnaplanModel

FilterOpsWithValue = Literal["eq", "ne", "gt", "ge", "lt", "le"]
AnaplanFilterFields = Literal[
    "id", "externalId", "userName", "name.familyName", "name.givenName", "active"
]
ScimFilters: TypeAlias = (
    list[
        tuple[AnaplanFilterFields, FilterOpsWithValue, str]
        | tuple[AnaplanFilterFields, Literal["pr"]]
    ]
    | None
)


class NameInput(AnaplanModel):
    family_name: str = Field(
        description="The family name of the User, or last name in most Western languages"
    )
    given_name: str = Field(
        description="The given name of the User, or first name in most Western languages"
    )


class Name(NameInput):
    formatted: str = Field(
        description=(
            "The formatted full name, including given name and family name. Anaplan does as of now "
            "not have other standard SCIM fields such as middle name or honorific pre- or suffixes."
        )
    )


class Email(AnaplanModel):
    value: str | None = Field(default=None, description="Email address of the User")
    type: Literal["work", "home", "other"] | None = Field(
        default=None, description="A label indicating the emails's function, e.g., 'work' or 'home'"
    )
    primary: bool | None = Field(
        default=None, description="Indicates if this is the primary or 'preferred' email"
    )


class EntitlementInput(AnaplanModel):
    value: str = Field(description="The value of an entitlement.")
    type: Literal["WORKSPACE", "WORKSPACE_IDS", "WORKSPACE_NAMES"] = Field(
        description="A label indicating the attribute's function."
    )


class Entitlement(EntitlementInput):
    display: str | None = Field(
        default=None, description="A human-readable name, primarily used for display purposes."
    )
    primary: bool | None = Field(
        default=None,
        description="Indicating the 'primary' or preferred attribute value for this attribute.",
    )


class _BaseUser(AnaplanModel):
    schemas: list[str] = Field(default=["urn:ietf:params:scim:schemas:core:2.0:User"])
    user_name: str = Field(description="Unique name for the User.")


class User(_BaseUser):
    id: str = Field(description="The unique identifier for the User.")
    name: Name = Field(description="The user's real name.")
    active: bool = Field(description="Indicating the User's active status.")
    emails: list[Email] = Field(description="Email addresses for the user.")
    display_name: str = Field(description="Display Name for the User.")
    entitlements: list[Entitlement] | None = Field(
        default=None, description="A list of entitlements (Workspaces) the User has."
    )


class ReplaceUserInput(_BaseUser):
    id: str = Field(description="The unique identifier for the User.")
    name: NameInput = Field(description="The user's real name.")
    active: bool | None = Field(default=None, description="Indicating the User's active status.")
    display_name: str | None = Field(default=None, description="Display Name for the User.")
    entitlements: list[EntitlementInput] | None = Field(
        default=None, description="A list of entitlements (Workspaces) the User has."
    )


class UserInput(_BaseUser):
    external_id: str = Field(
        description="Your unique id for this user (as stored in your company systems)."
    )
    name: NameInput = Field(description="The user's real name.")


class Meta(AnaplanModel):
    resource_type: str = Field(description="The type of the resource.")
    location: str = Field(description="The URI of the resource.")


class MetaWithDates(Meta):
    created: str = Field(description="The timestamp when the resource was created.")
    last_modified: str = Field(description="The timestamp when the resource was last modified.")


class Supported(AnaplanModel):
    supported: bool = Field(description="Indicates whether the Feature is supported.")


class BulkConfig(Supported):
    max_operations: int = Field(
        description="The maximum number of operations permitted in a single request."
    )
    max_payload_size: int = Field(description="The maximum payload size in bytes.")


class FilterConfig(Supported):
    max_results: int = Field(
        description="The maximum number of results returned from a filtered query."
    )


class AuthenticationScheme(AnaplanModel):
    name: str = Field(description="The name of the authentication scheme.")
    type: str = Field(description="The type of the authentication scheme.")
    description: str = Field(description="A description of the authentication scheme.")
    spec_uri: str = Field(
        description="The URI that points to the specification of the authentication scheme."
    )
    documentation_uri: str = Field(
        description="The URI that points to the documentation of the authentication scheme."
    )


class ServiceProviderConfig(AnaplanModel):
    schemas: list[str] = Field(
        default=["urn:ietf:params:scim:schemas:core:2.0:ServiceProviderConfig"],
        description="Schemas for this resource.",
    )
    meta: MetaWithDates = Field(description="Metadata about the resource.")
    documentation_uri: str = Field(description="URI of the service provider's documentation.")
    patch: Supported = Field(description="Configuration for PATCH operations.")
    bulk: BulkConfig = Field(description="Configuration for bulk operations.")
    filter: FilterConfig = Field(description="Configuration for filtering.")
    change_password: Supported = Field(description="Configuration for password changes.")
    sort: Supported = Field(description="Configuration for sorting.")
    etag: Supported = Field(description="Configuration for ETags.")
    authentication_schemes: list[AuthenticationScheme] = Field(
        description="List of supported authentication schemes."
    )


class Resource(AnaplanModel):
    schemas: list[str] = Field(
        default=["urn:ietf:params:scim:schemas:core:2.0:ResourceType"],
        description="Schemas for this resource.",
    )
    meta: Meta = Field(description="Metadata about the resource.")
    id: str = Field(description="The identifier of the resource type.")
    name: str = Field(description="The name of the resource type.")
    endpoint: str = Field(description="The endpoint where resources of this type may be accessed.")
    description: str = Field(description="A description of the resource type.")


class Attribute(AnaplanModel):
    name: str = Field(description="The name of the attribute.")
    type: str = Field(description="The data type of the attribute.")
    multi_valued: bool = Field(description="Indicates if the attribute can have multiple values.")
    description: str = Field(description="A human-readable description of the attribute.")
    required: bool = Field(description="Indicates if the attribute is required.")
    case_exact: bool = Field(
        description="Indicates if case sensitivity should be considered when comparing values."
    )
    mutability: str = Field(description="Indicates if and how the attribute can be modified.")
    returned: str = Field(
        description="Indicates when the attribute's values are returned in a response."
    )
    uniqueness: str = Field(
        description="Indicates how uniqueness is enforced on the attribute value."
    )
    sub_attributes: list["Attribute"] | None = Field(
        default=None, description="A list of sub-attributes if the attribute is complex."
    )


class Schema(AnaplanModel):
    meta: Meta = Field(description="Metadata about the schema resource.")
    id: str = Field(description="The unique identifier for the schema.")
    name: str = Field(description="The name of the schema.")
    description: str = Field(description="A description of the schema.")
    attributes: list[Attribute] = Field(description="A list of attributes that define the schema.")


class Operation(AnaplanModel):
    op: Literal["add", "remove", "replace"] = Field(description="The operation to be performed.")
    path: str = Field(
        description=(
            "A string containing a JSON-Pointer value that references a location within the target "
            "resource."
        )
    )
    value: Any | None = Field(default=None, description="The value to be used in the operation.")


class Replace(Operation):
    op: Literal["replace"] = Field(
        default="replace", description="Replace the value at path with the new given value."
    )


class Add(Operation):
    op: Literal["add"] = Field(
        default="add", description="Add the given value to the attribute at path."
    )


class Remove(Operation):
    op: Literal["remove"] = Field(default="remove", description="Remove the value at path.")
