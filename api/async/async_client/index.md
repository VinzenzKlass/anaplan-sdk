# Bulk API Client (`AsyncClient`)

Asynchronous Anaplan Client. For guides and examples refer to https://vinzenzklass.github.io/anaplan-sdk.

## __init__

```
__init__(
    workspace_id: str | None = None,
    model_id: str | None = None,
    user_email: str | None = None,
    password: str | None = None,
    certificate: str | bytes | None = None,
    private_key: str | bytes | None = None,
    private_key_password: str | bytes | None = None,
    token: str | None = None,
    auth: Auth | None = None,
    timeout: float | Timeout = 30,
    retry_count: int = 2,
    backoff: float = 1.0,
    backoff_factor: float = 2.0,
    page_size: int = 5000,
    status_poll_delay: int = 1,
    upload_chunk_size: int = 25000000,
    allow_file_creation: bool = False,
    **httpx_kwargs: Any,
) -> None
```

Asynchronous Anaplan Client. For guides and examples refer to https://vinzenzklass.github.io/anaplan-sdk.

Parameters:

| Name                   | Type    | Description                                                                                                                                                                                                                                                                                                                                                           | Default                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| ---------------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `workspace_id`         | \`str   | None\`                                                                                                                                                                                                                                                                                                                                                                | The Anaplan workspace Id. You can copy this from the browser URL or find them using an HTTP Client like Postman, Paw, Insomnia etc.                                                                                                                                                                                                                                                                                                                                                                   |
| `model_id`             | \`str   | None\`                                                                                                                                                                                                                                                                                                                                                                | The identifier of the model.                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `user_email`           | \`str   | None\`                                                                                                                                                                                                                                                                                                                                                                | A valid email registered with the Anaplan Workspace you are attempting to access.                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `password`             | \`str   | None\`                                                                                                                                                                                                                                                                                                                                                                | Password for the given user_email for basic Authentication.                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `certificate`          | \`str   | bytes                                                                                                                                                                                                                                                                                                                                                                 | None\`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `private_key`          | \`str   | bytes                                                                                                                                                                                                                                                                                                                                                                 | None\`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `private_key_password` | \`str   | bytes                                                                                                                                                                                                                                                                                                                                                                 | None\`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `token`                | \`str   | None\`                                                                                                                                                                                                                                                                                                                                                                | An Anaplan API Token. This will be used to authenticate the client. If sufficient other authentication parameters are provided, the token will be used until it expires, after which a new one will be created. If you provide only this parameter, the client will raise an error upon first authentication failure. For short-lived instances, such as in web applications where user specific clients are created, this is the recommended way to authenticate, since this has the least overhead. |
| `auth`                 | \`Auth  | None\`                                                                                                                                                                                                                                                                                                                                                                | You can provide a subclass of httpx.Auth to use for authentication. You can provide an instance of one of the classes provided by the SDK, or an instance of your own subclass of httpx.Auth. This will give you full control over the authentication process, but you will need to implement the entire authentication logic yourself.                                                                                                                                                               |
| `timeout`              | \`float | Timeout\`                                                                                                                                                                                                                                                                                                                                                             | The timeout in seconds for the HTTP requests. Alternatively, you can pass an instance of httpx.Timeout to set the timeout for the HTTP requests.                                                                                                                                                                                                                                                                                                                                                      |
| `retry_count`          | `int`   | The number of times to retry an HTTP request if it fails. Set this to 0 to never retry. Defaults to 2, meaning each HTTP Operation will be tried a total number of 2 times.                                                                                                                                                                                           | `2`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `backoff`              | `float` | The initial backoff time in seconds for the retry mechanism. This is the time to wait before the first retry.                                                                                                                                                                                                                                                         | `1.0`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `backoff_factor`       | `float` | The factor by which the backoff time is multiplied after each retry. For example, if the initial backoff is 1 second and the factor is 2, the second retry will wait 2 seconds, the third retry will wait 4 seconds, and so on.                                                                                                                                       | `2.0`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `page_size`            | `int`   | The number of items to return per page when paginating through results. Defaults to 5000. This is the maximum number of items that can be returned per request. If you pass a value greater than 5000, it will be capped to 5000.                                                                                                                                     | `5000`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `status_poll_delay`    | `int`   | The delay between polling the status of a task.                                                                                                                                                                                                                                                                                                                       | `1`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `upload_chunk_size`    | `int`   | The size of the chunks to upload. This is the maximum size of each chunk. Defaults to 25MB.                                                                                                                                                                                                                                                                           | `25000000`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `allow_file_creation`  | `bool`  | Whether to allow the creation of new files. Defaults to False since this is typically unintentional and may well be unwanted behaviour in the API altogether. A file that is created this way will not be referenced by any action in anaplan until manually assigned so there is typically no value in dynamically creating new files and uploading content to them. | `False`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `httpx_kwargs`         | `Any`   | Additional keyword arguments to pass to the httpx.AsyncClient. This can be used to set additional options such as proxies, headers, etc. See https://www.python-httpx.org/api/#asyncclient for the full list of arguments.                                                                                                                                            | `{}`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |

## with_model

```
with_model(
    model_id: str | None = None, workspace_id: str | None = None
) -> Self
```

Create a new instance of the Client with the given model and workspace Ids. **This creates a copy of the current client. The current instance remains unchanged.**

Parameters:

| Name           | Type  | Description | Default                                                           |
| -------------- | ----- | ----------- | ----------------------------------------------------------------- |
| `workspace_id` | \`str | None\`      | The workspace Id to use or None to use the existing workspace Id. |
| `model_id`     | \`str | None\`      | The model Id to use or None to use the existing model Id.         |

Returns:

| Type   | Description                   |
| ------ | ----------------------------- |
| `Self` | A new instance of the Client. |

## audit

```
audit: _AsyncAuditClient
```

The Audit Client provides access to the Anaplan Audit API. For details, see https://vinzenzklass.github.io/anaplan-sdk/guides/audit/.

## cw

```
cw: _AsyncCloudWorksClient
```

The Cloud Works Client provides access to the Anaplan Cloud Works API. For details, see https://vinzenzklass.github.io/anaplan-sdk/guides/cloud_works/.

## tr

```
tr: _AsyncTransactionalClient
```

The Transactional Client provides access to the Anaplan Transactional API. This is useful for more advanced use cases where you need to interact with the Anaplan Model in a more granular way.

If you instantiated the client without the field `model_id`, this will raise a `ValueError`, since none of the endpoints can be invoked without the model Id.

Returns:

| Type                        | Description               |
| --------------------------- | ------------------------- |
| `_AsyncTransactionalClient` | The Transactional Client. |

## alm

```
alm: _AsyncAlmClient
```

**To use the Application Lifecycle Management (ALM) API, you need a Professional or Enterprise subscription.**

The ALM Client provides access to the Anaplan ALM API. This is useful for more advanced use cases where you need retrieve Meta Information for yours models, read or create revisions, spawn sync tasks or generate comparison reports.

Returns:

| Type              | Description     |
| ----------------- | --------------- |
| `_AsyncAlmClient` | The ALM Client. |

## scim

```
scim: _AsyncScimClient
```

To use the SCIM API, you must be User Admin. The SCIM API allows managing internal users. Visiting users are excluded from the SCIM API.

Returns:

| Type               | Description      |
| ------------------ | ---------------- |
| `_AsyncScimClient` | The SCIM Client. |

## get_workspace

```
get_workspace(workspace_id: str | None = None) -> Workspace
```

Retrieves the Workspace with the given Id, or the Workspace of the current instance if no Id is given. If no Id is given and the instance has no workspace Id, this will raise a ValueError.

Parameters:

| Name           | Type  | Description | Default                                      |
| -------------- | ----- | ----------- | -------------------------------------------- |
| `workspace_id` | \`str | None\`      | The identifier of the Workspace to retrieve. |

Returns:

| Type        | Description    |
| ----------- | -------------- |
| `Workspace` | The Workspace. |

## get_workspaces

```
get_workspaces(
    search_pattern: str | None = None,
    sort_by: Literal["size_allowance", "name"] | None = None,
    descending: bool = False,
) -> list[Workspace]
```

Lists all the Workspaces the authenticated user has access to.

Parameters:

| Name             | Type                                | Description                                              | Default                                                                                                                                                                                                                                                                                                                                                                                               |
| ---------------- | ----------------------------------- | -------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `search_pattern` | \`str                               | None\`                                                   | Caution: This is an undocumented Feature and may behave unpredictably. It requires the Tenant Admin role. For non-admin users, it is ignored. Optionally filter for specific workspaces. When provided, case-insensitive matches workspaces with names containing this string. You can use the wildcards % for 0-n characters, and _ for exactly 1 character. When None (default), returns all users. |
| `sort_by`        | \`Literal['size_allowance', 'name'] | None\`                                                   | The field to sort the results by.                                                                                                                                                                                                                                                                                                                                                                     |
| `descending`     | `bool`                              | If True, the results will be sorted in descending order. | `False`                                                                                                                                                                                                                                                                                                                                                                                               |

Returns:

| Type              | Description             |
| ----------------- | ----------------------- |
| `list[Workspace]` | The List of Workspaces. |

## get_model

```
get_model(model_id: str | None = None) -> ModelWithTransactionInfo
```

Retrieves the Model with the given Id, or the Model of the current instance if no Id is given. If no Id is given and the instance has no model Id, this will raise a ValueError.

Parameters:

| Name       | Type  | Description | Default                                  |
| ---------- | ----- | ----------- | ---------------------------------------- |
| `model_id` | \`str | None\`      | The identifier of the Model to retrieve. |

Returns:

| Type                       | Description |
| -------------------------- | ----------- |
| `ModelWithTransactionInfo` | The Model.  |

## get_models

```
get_models(
    only_in_workspace: bool | str = False,
    search_pattern: str | None = None,
    sort_by: Literal["active_state", "name"] | None = None,
    descending: bool = False,
) -> list[Model]
```

Lists all the Models the authenticated user has access to.

Parameters:

| Name                | Type                              | Description                                              | Default                                                                                                                                                                                                                                                                                                                                                                                  |
| ------------------- | --------------------------------- | -------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `only_in_workspace` | \`bool                            | str\`                                                    | If True, only lists models in the workspace provided when instantiating the client. If a string is provided, only lists models in the workspace with the given Id. If False (default), lists models in all workspaces the user                                                                                                                                                           |
| `search_pattern`    | \`str                             | None\`                                                   | Caution: This is an undocumented Feature and may behave unpredictably. It requires the Tenant Admin role. For non-admin users, it is ignored. Optionally filter for specific models. When provided, case-insensitive matches model names containing this string. You can use the wildcards % for 0-n characters, and _ for exactly 1 character. When None (default), returns all models. |
| `sort_by`           | \`Literal['active_state', 'name'] | None\`                                                   | The field to sort the results by.                                                                                                                                                                                                                                                                                                                                                        |
| `descending`        | `bool`                            | If True, the results will be sorted in descending order. | `False`                                                                                                                                                                                                                                                                                                                                                                                  |

Returns:

| Type          | Description         |
| ------------- | ------------------- |
| `list[Model]` | The List of Models. |

## delete_models

```
delete_models(model_ids: list[str]) -> ModelDeletionResult
```

Delete the given Models. Models need to be closed before they can be deleted. If one of the deletions fails, the other deletions will still be attempted and may complete.

Parameters:

| Name        | Type        | Description                              | Default    |
| ----------- | ----------- | ---------------------------------------- | ---------- |
| `model_ids` | `list[str]` | The list of Model identifiers to delete. | *required* |

Returns:

| Type                  | Description |
| --------------------- | ----------- |
| `ModelDeletionResult` |             |

## get_files

```
get_files(sort_by: SortBy = None, descending: bool = False) -> list[File]
```

Lists all the Files in the Model.

Parameters:

| Name         | Type     | Description                                              | Default |
| ------------ | -------- | -------------------------------------------------------- | ------- |
| `sort_by`    | `SortBy` | The field to sort the results by.                        | `None`  |
| `descending` | `bool`   | If True, the results will be sorted in descending order. | `False` |

Returns:

| Type         | Description        |
| ------------ | ------------------ |
| `list[File]` | The List of Files. |

## get_actions

```
get_actions(sort_by: SortBy = None, descending: bool = False) -> list[Action]
```

Lists all the Actions in the Model. This will only return the Actions listed under `Other Actions` in Anaplan. For Imports, exports, and processes, see their respective methods instead.

Parameters:

| Name         | Type     | Description                                              | Default |
| ------------ | -------- | -------------------------------------------------------- | ------- |
| `sort_by`    | `SortBy` | The field to sort the results by.                        | `None`  |
| `descending` | `bool`   | If True, the results will be sorted in descending order. | `False` |

Returns:

| Type           | Description          |
| -------------- | -------------------- |
| `list[Action]` | The List of Actions. |

## get_processes

```
get_processes(
    sort_by: SortBy = None, descending: bool = False
) -> list[Process]
```

Lists all the Processes in the Model.

Parameters:

| Name         | Type     | Description                                              | Default |
| ------------ | -------- | -------------------------------------------------------- | ------- |
| `sort_by`    | `SortBy` | The field to sort the results by.                        | `None`  |
| `descending` | `bool`   | If True, the results will be sorted in descending order. | `False` |

Returns:

| Type            | Description            |
| --------------- | ---------------------- |
| `list[Process]` | The List of Processes. |

## get_imports

```
get_imports(sort_by: SortBy = None, descending: bool = False) -> list[Import]
```

Lists all the Imports in the Model.

Parameters:

| Name         | Type     | Description                                              | Default |
| ------------ | -------- | -------------------------------------------------------- | ------- |
| `sort_by`    | `SortBy` | The field to sort the results by.                        | `None`  |
| `descending` | `bool`   | If True, the results will be sorted in descending order. | `False` |

Returns:

| Type           | Description          |
| -------------- | -------------------- |
| `list[Import]` | The List of Imports. |

## get_exports

```
get_exports(sort_by: SortBy = None, descending: bool = False) -> list[Export]
```

Lists all the Exports in the Model.

Parameters:

| Name         | Type     | Description                                              | Default |
| ------------ | -------- | -------------------------------------------------------- | ------- |
| `sort_by`    | `SortBy` | The field to sort the results by.                        | `None`  |
| `descending` | `bool`   | If True, the results will be sorted in descending order. | `False` |

Returns:

| Type           | Description          |
| -------------- | -------------------- |
| `list[Export]` | The List of Exports. |

## run_action

```
run_action(
    action_id: int, wait_for_completion: Literal[True] = True
) -> CompletedTask
```

```
run_action(action_id: int, wait_for_completion: Literal[False] = False) -> Task
```

```
run_action(action_id: int, wait_for_completion: bool = True) -> TaskStatus
```

Runs the Action and validates the spawned task. If the Action fails or completes with errors, this will raise an AnaplanActionError. Failed Tasks are often not something you can recover from at runtime and often require manual changes in Anaplan, i.e. updating the mapping of an Import or similar.

Parameters:

| Name                  | Type   | Description                                                                                                                                       | Default    |
| --------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| `action_id`           | `int`  | The identifier of the Action to run. Can be any Anaplan Invokable; Processes, Imports, Exports, Other Actions.                                    | *required* |
| `wait_for_completion` | `bool` | If True, the method will poll the task status and not return until the task is complete. If False, it will spawn the task and return immediately. | `True`     |

## get_file

```
get_file(file_id: int) -> bytes
```

Retrieves the content of the specified file.

Parameters:

| Name      | Type  | Description                             | Default    |
| --------- | ----- | --------------------------------------- | ---------- |
| `file_id` | `int` | The identifier of the file to retrieve. | *required* |

Returns:

| Type    | Description              |
| ------- | ------------------------ |
| `bytes` | The content of the file. |

## get_file_stream

```
get_file_stream(file_id: int, batch_size: int = 1) -> AsyncIterator[bytes]
```

Retrieves the content of the specified file as a stream of chunks. The chunks are yielded one by one, so you can process them as they arrive. This is useful for large files where you don't want to or cannot load the entire file into memory at once.

Parameters:

| Name         | Type  | Description                                                                                                                                                                                                          | Default    |
| ------------ | ----- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| `file_id`    | `int` | The identifier of the file to retrieve.                                                                                                                                                                              | *required* |
| `batch_size` | `int` | Number of chunks to fetch concurrently. If > 1, n chunks will be fetched concurrently. This still yields each chunk individually, only the requests are batched. If 1 (default), each chunk is fetched sequentially. | `1`        |

Returns:

| Type                   | Description                                  |
| ---------------------- | -------------------------------------------- |
| `AsyncIterator[bytes]` | A generator yielding the chunks of the file. |

## upload_file

```
upload_file(file_id: int, content: str | bytes) -> None
```

Uploads the content to the specified file. If there are several chunks, upload of individual chunks are uploaded concurrently.

Parameters:

| Name      | Type  | Description                              | Default                                                                                                                               |
| --------- | ----- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `file_id` | `int` | The identifier of the file to upload to. | *required*                                                                                                                            |
| `content` | \`str | bytes\`                                  | The content to upload. This Content will be compressed before uploading. If you are passing the Input as bytes, pass it uncompressed. |

## upload_file_stream

```
upload_file_stream(
    file_id: int,
    content: AsyncIterator[bytes | str] | Iterator[str | bytes],
    batch_size: int = 1,
) -> None
```

Uploads the content to the specified file as a stream of chunks. This is useful either for large files where you don't want to or cannot load the entire file into memory at once, or if you simply do not know the number of chunks ahead of time and instead just want to pass on chunks i.e. consumed from a queue until it is exhausted. In this case, you can pass a generator that yields the chunks of the file one by one to this method.

Parameters:

| Name         | Type                   | Description                                                                                                                                                                                                                           | Default       |
| ------------ | ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- |
| `file_id`    | `int`                  | The identifier of the file to upload to.                                                                                                                                                                                              | *required*    |
| `content`    | \`AsyncIterator\[bytes | str\]                                                                                                                                                                                                                                 | Iterator\[str |
| `batch_size` | `int`                  | Number of chunks to upload concurrently. If > 1, n chunks will be uploaded concurrently. This can be useful if you either do not control the chunk size, or if you want to keep the chunk size small but still want some concurrency. | `1`           |

## upload_and_import

```
upload_and_import(
    file_id: int,
    content: str | bytes,
    action_id: int,
    wait_for_completion: Literal[True] = True,
) -> CompletedTask
```

```
upload_and_import(
    file_id: int,
    content: str | bytes,
    action_id: int,
    wait_for_completion: Literal[False] = False,
) -> Task
```

```
upload_and_import(
    file_id: int,
    content: str | bytes,
    action_id: int,
    wait_for_completion: bool = True,
) -> TaskStatus
```

Convenience wrapper around `upload_file()` and `run_action()` to upload content to a file and run an import action in one call.

Parameters:

| Name                  | Type   | Description                                                                                                                                                     | Default                                                                                                                                                       |
| --------------------- | ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `file_id`             | `int`  | The identifier of the file to upload to.                                                                                                                        | *required*                                                                                                                                                    |
| `content`             | \`str  | bytes\`                                                                                                                                                         | The content to upload. This Content will be compressed before uploading. If you are passing the Input as bytes, pass it uncompressed to avoid redundant work. |
| `action_id`           | `int`  | The identifier of the action to run after uploading the content.                                                                                                | *required*                                                                                                                                                    |
| `wait_for_completion` | `bool` | If True, the method will poll the import task status and not return until the task is complete. If False, it will spawn the import task and return immediately. | `True`                                                                                                                                                        |

## export_and_download

```
export_and_download(action_id: int) -> bytes
```

Convenience wrapper around `run_action()` and `get_file()` to run an export action and download the exported content in one call.

Parameters:

| Name        | Type  | Description                          | Default    |
| ----------- | ----- | ------------------------------------ | ---------- |
| `action_id` | `int` | The identifier of the action to run. | *required* |

Returns:

| Type    | Description                       |
| ------- | --------------------------------- |
| `bytes` | The content of the exported file. |

## get_task_summaries

```
get_task_summaries(action_id: int) -> list[TaskSummary]
```

Retrieves the status of all tasks spawned by the specified action.

Parameters:

| Name        | Type  | Description                                    | Default    |
| ----------- | ----- | ---------------------------------------------- | ---------- |
| `action_id` | `int` | The identifier of the action that was invoked. | *required* |

Returns:

| Type                | Description                              |
| ------------------- | ---------------------------------------- |
| `list[TaskSummary]` | The list of tasks spawned by the action. |

## get_task_status

```
get_task_status(action_id: int, task_id: str) -> TaskStatus
```

Retrieves the status of the specified task.

Parameters:

| Name        | Type  | Description                                    | Default    |
| ----------- | ----- | ---------------------------------------------- | ---------- |
| `action_id` | `int` | The identifier of the action that was invoked. | *required* |
| `task_id`   | `str` | The identifier of the spawned task.            | *required* |

Returns:

| Type         | Description             |
| ------------ | ----------------------- |
| `TaskStatus` | The status of the task. |

## get_optimizer_log

```
get_optimizer_log(action_id: int, task_id: str) -> bytes
```

Retrieves the solution logs of the specified optimization action task.

Parameters:

| Name        | Type  | Description                                                            | Default    |
| ----------- | ----- | ---------------------------------------------------------------------- | ---------- |
| `action_id` | `int` | The identifier of the optimization action that was invoked.            | *required* |
| `task_id`   | `str` | The Task identifier, sometimes also referred to as the Correlation Id. | *required* |

Returns:

| Type    | Description                       |
| ------- | --------------------------------- |
| `bytes` | The content of the solution logs. |
