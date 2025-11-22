## NameInput

Parameters:

| Name          | Type  | Description                                                         | Default    |
| ------------- | ----- | ------------------------------------------------------------------- | ---------- |
| `family_name` | `str` | The family name of the User, or last name in most Western languages | *required* |
| `given_name`  | `str` | The given name of the User, or first name in most Western languages | *required* |

## Name

Parameters:

| Name          | Type  | Description                                                                                                                                                                  | Default    |
| ------------- | ----- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| `family_name` | `str` | The family name of the User, or last name in most Western languages                                                                                                          | *required* |
| `given_name`  | `str` | The given name of the User, or first name in most Western languages                                                                                                          | *required* |
| `formatted`   | `str` | The formatted full name, including given name and family name. Anaplan does as of now not have other standard SCIM fields such as middle name or honorific pre- or suffixes. | *required* |

## Email

Parameters:

| Name      | Type                                     | Description                                                      | Default                                               |
| --------- | ---------------------------------------- | ---------------------------------------------------------------- | ----------------------------------------------------- |
| `value`   | `str`                                    | Email address of the User                                        | *required*                                            |
| `type`    | `Literal['work', 'home', 'other', None]` | A label indicating the emails's function, e.g., 'work' or 'home' | `None`                                                |
| `primary` | \`bool                                   | None\`                                                           | Indicates if this is the primary or 'preferred' email |

## EntitlementInput

Parameters:

| Name    | Type                                                       | Description                                  | Default    |
| ------- | ---------------------------------------------------------- | -------------------------------------------- | ---------- |
| `value` | `str`                                                      | The value of an entitlement.                 | *required* |
| `type`  | `Literal['WORKSPACE', 'WORKSPACE_IDS', 'WORKSPACE_NAMES']` | A label indicating the attribute's function. | *required* |

## Entitlement

Parameters:

| Name      | Type                                                       | Description                                  | Default                                                                   |
| --------- | ---------------------------------------------------------- | -------------------------------------------- | ------------------------------------------------------------------------- |
| `value`   | `str`                                                      | The value of an entitlement.                 | *required*                                                                |
| `type`    | `Literal['WORKSPACE', 'WORKSPACE_IDS', 'WORKSPACE_NAMES']` | A label indicating the attribute's function. | *required*                                                                |
| `display` | \`str                                                      | None\`                                       | A human-readable name, primarily used for display purposes.               |
| `primary` | \`bool                                                     | None\`                                       | Indicating the 'primary' or preferred attribute value for this attribute. |

## Meta

Parameters:

| Name            | Type  | Description               | Default    |
| --------------- | ----- | ------------------------- | ---------- |
| `resource_type` | `str` | The type of the resource. | *required* |
| `location`      | `str` | The URI of the resource.  | *required* |

## MetaWithDates

Parameters:

| Name            | Type  | Description                                        | Default    |
| --------------- | ----- | -------------------------------------------------- | ---------- |
| `resource_type` | `str` | The type of the resource.                          | *required* |
| `location`      | `str` | The URI of the resource.                           | *required* |
| `created`       | `str` | The timestamp when the resource was created.       | *required* |
| `last_modified` | `str` | The timestamp when the resource was last modified. | *required* |

## User

Parameters:

| Name           | Type                | Description                                       | Default                                          |
| -------------- | ------------------- | ------------------------------------------------- | ------------------------------------------------ |
| `schemas`      | `list[str]`         |                                                   | `['urn:ietf:params:scim:schemas:core:2.0:User']` |
| `user_name`    | `str`               | Unique name for the User.                         | *required*                                       |
| `id`           | `str`               | The unique identifier for the User.               | *required*                                       |
| `name`         | `Name`              | The user's real name.                             | *required*                                       |
| `active`       | `bool`              | Indicating the User's active status.              | *required*                                       |
| `emails`       | `list[Email]`       | Email addresses for the user.                     | `[]`                                             |
| `display_name` | `str`               | Display Name for the User.                        | *required*                                       |
| `entitlements` | `list[Entitlement]` | A list of entitlements (Workspaces) the User has. | `[]`                                             |
| `meta`         | `MetaWithDates`     | Metadata about the resource.                      | *required*                                       |

## ReplaceUserInput

Parameters:

| Name           | Type                     | Description                         | Default                                           |
| -------------- | ------------------------ | ----------------------------------- | ------------------------------------------------- |
| `schemas`      | `list[str]`              |                                     | `['urn:ietf:params:scim:schemas:core:2.0:User']`  |
| `user_name`    | `str`                    | Unique name for the User.           | *required*                                        |
| `id`           | `str`                    | The unique identifier for the User. | *required*                                        |
| `name`         | `NameInput`              | The user's real name.               | *required*                                        |
| `active`       | \`bool                   | None\`                              | Indicating the User's active status.              |
| `display_name` | \`str                    | None\`                              | Display Name for the User.                        |
| `entitlements` | \`list[EntitlementInput] | None\`                              | A list of entitlements (Workspaces) the User has. |

## UserInput

Parameters:

| Name          | Type        | Description                                                       | Default                                          |
| ------------- | ----------- | ----------------------------------------------------------------- | ------------------------------------------------ |
| `schemas`     | `list[str]` |                                                                   | `['urn:ietf:params:scim:schemas:core:2.0:User']` |
| `user_name`   | `str`       | Unique name for the User.                                         | *required*                                       |
| `external_id` | `str`       | Your unique id for this user (as stored in your company systems). | *required*                                       |
| `name`        | `NameInput` | The user's real name.                                             | *required*                                       |

## Supported

Parameters:

| Name        | Type   | Description                                 | Default    |
| ----------- | ------ | ------------------------------------------- | ---------- |
| `supported` | `bool` | Indicates whether the Feature is supported. | *required* |

## BulkConfig

Parameters:

| Name               | Type   | Description                                                     | Default    |
| ------------------ | ------ | --------------------------------------------------------------- | ---------- |
| `supported`        | `bool` | Indicates whether the Feature is supported.                     | *required* |
| `max_operations`   | `int`  | The maximum number of operations permitted in a single request. | *required* |
| `max_payload_size` | `int`  | The maximum payload size in bytes.                              | *required* |

## FilterConfig

Parameters:

| Name          | Type   | Description                                                   | Default    |
| ------------- | ------ | ------------------------------------------------------------- | ---------- |
| `supported`   | `bool` | Indicates whether the Feature is supported.                   | *required* |
| `max_results` | `int`  | The maximum number of results returned from a filtered query. | *required* |

## AuthenticationScheme

Parameters:

| Name                | Type  | Description                                                            | Default    |
| ------------------- | ----- | ---------------------------------------------------------------------- | ---------- |
| `name`              | `str` | The name of the authentication scheme.                                 | *required* |
| `type`              | `str` | The type of the authentication scheme.                                 | *required* |
| `description`       | `str` | A description of the authentication scheme.                            | *required* |
| `spec_uri`          | `str` | The URI that points to the specification of the authentication scheme. | *required* |
| `documentation_uri` | `str` | The URI that points to the documentation of the authentication scheme. | *required* |

## ServiceProviderConfig

Parameters:

| Name                     | Type                         | Description                                  | Default                                                           |
| ------------------------ | ---------------------------- | -------------------------------------------- | ----------------------------------------------------------------- |
| `schemas`                | `list[str]`                  | Schemas for this resource.                   | `['urn:ietf:params:scim:schemas:core:2.0:ServiceProviderConfig']` |
| `meta`                   | `MetaWithDates`              | Metadata about the resource.                 | *required*                                                        |
| `documentation_uri`      | `str`                        | URI of the service provider's documentation. | *required*                                                        |
| `patch`                  | `Supported`                  | Configuration for PATCH operations.          | *required*                                                        |
| `bulk`                   | `BulkConfig`                 | Configuration for bulk operations.           | *required*                                                        |
| `filter`                 | `FilterConfig`               | Configuration for filtering.                 | *required*                                                        |
| `change_password`        | `Supported`                  | Configuration for password changes.          | *required*                                                        |
| `sort`                   | `Supported`                  | Configuration for sorting.                   | *required*                                                        |
| `etag`                   | `Supported`                  | Configuration for ETags.                     | *required*                                                        |
| `authentication_schemes` | `list[AuthenticationScheme]` | List of supported authentication schemes.    | *required*                                                        |

## Resource

Parameters:

| Name          | Type        | Description                                                | Default                                                  |
| ------------- | ----------- | ---------------------------------------------------------- | -------------------------------------------------------- |
| `schemas`     | `list[str]` | Schemas for this resource.                                 | `['urn:ietf:params:scim:schemas:core:2.0:ResourceType']` |
| `meta`        | `Meta`      | Metadata about the resource.                               | *required*                                               |
| `id`          | `str`       | The identifier of the resource type.                       | *required*                                               |
| `name`        | `str`       | The name of the resource type.                             | *required*                                               |
| `endpoint`    | `str`       | The endpoint where resources of this type may be accessed. | *required*                                               |
| `description` | `str`       | A description of the resource type.                        | *required*                                               |

## Attribute

Parameters:

| Name             | Type              | Description                                                               | Default                                               |
| ---------------- | ----------------- | ------------------------------------------------------------------------- | ----------------------------------------------------- |
| `name`           | `str`             | The name of the attribute.                                                | *required*                                            |
| `type`           | `str`             | The data type of the attribute.                                           | *required*                                            |
| `multi_valued`   | `bool`            | Indicates if the attribute can have multiple values.                      | *required*                                            |
| `description`    | `str`             | A human-readable description of the attribute.                            | *required*                                            |
| `required`       | `bool`            | Indicates if the attribute is required.                                   | *required*                                            |
| `case_exact`     | `bool`            | Indicates if case sensitivity should be considered when comparing values. | *required*                                            |
| `mutability`     | `str`             | Indicates if and how the attribute can be modified.                       | *required*                                            |
| `returned`       | `str`             | Indicates when the attribute's values are returned in a response.         | *required*                                            |
| `uniqueness`     | `str`             | Indicates how uniqueness is enforced on the attribute value.              | *required*                                            |
| `sub_attributes` | \`list[Attribute] | None\`                                                                    | A list of sub-attributes if the attribute is complex. |

## Schema

Parameters:

| Name          | Type              | Description                                  | Default    |
| ------------- | ----------------- | -------------------------------------------- | ---------- |
| `meta`        | `Meta`            | Metadata about the schema resource.          | *required* |
| `id`          | `str`             | The unique identifier for the schema.        | *required* |
| `name`        | `str`             | The name of the schema.                      | *required* |
| `description` | `str`             | A description of the schema.                 | *required* |
| `attributes`  | `list[Attribute]` | A list of attributes that define the schema. | *required* |

## Operation

Parameters:

| Name    | Type                                  | Description                                                                                     | Default                                |
| ------- | ------------------------------------- | ----------------------------------------------------------------------------------------------- | -------------------------------------- |
| `op`    | `Literal['add', 'remove', 'replace']` | The operation to be performed.                                                                  | *required*                             |
| `path`  | `str`                                 | A string containing a JSON-Pointer value that references a location within the target resource. | *required*                             |
| `value` | \`Any                                 | None\`                                                                                          | The value to be used in the operation. |

## Replace

Parameters:

| Name    | Type                 | Description                                                                                     | Default                                |
| ------- | -------------------- | ----------------------------------------------------------------------------------------------- | -------------------------------------- |
| `op`    | `Literal['replace']` | Replace the value at path with the new given value.                                             | `'replace'`                            |
| `path`  | `str`                | A string containing a JSON-Pointer value that references a location within the target resource. | *required*                             |
| `value` | \`Any                | None\`                                                                                          | The value to be used in the operation. |

## Add

Parameters:

| Name    | Type             | Description                                                                                     | Default                                |
| ------- | ---------------- | ----------------------------------------------------------------------------------------------- | -------------------------------------- |
| `op`    | `Literal['add']` | Add the given value to the attribute at path.                                                   | `'add'`                                |
| `path`  | `str`            | A string containing a JSON-Pointer value that references a location within the target resource. | *required*                             |
| `value` | \`Any            | None\`                                                                                          | The value to be used in the operation. |

## Remove

Parameters:

| Name    | Type                | Description                                                                                     | Default                                |
| ------- | ------------------- | ----------------------------------------------------------------------------------------------- | -------------------------------------- |
| `op`    | `Literal['remove']` | Remove the value at path.                                                                       | `'remove'`                             |
| `path`  | `str`               | A string containing a JSON-Pointer value that references a location within the target resource. | *required*                             |
| `value` | \`Any               | None\`                                                                                          | The value to be used in the operation. |
