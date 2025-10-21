import logging
from asyncio import gather
from copy import copy
from typing import AsyncIterator, Iterator, Literal

import httpx
from typing_extensions import Self

from anaplan_sdk._auth import _create_auth
from anaplan_sdk._services import _AsyncHttpService
from anaplan_sdk._utils import action_url, models_url, sort_params
from anaplan_sdk.exceptions import AnaplanActionError, InvalidIdentifierException
from anaplan_sdk.models import (
    Action,
    Export,
    File,
    Import,
    Model,
    ModelDeletionResult,
    Process,
    TaskStatus,
    TaskSummary,
    Workspace,
)

from ._alm import _AsyncAlmClient
from ._audit import _AsyncAuditClient
from ._cloud_works import _AsyncCloudWorksClient
from ._scim import _AsyncScimClient
from ._transactional import _AsyncTransactionalClient

SortBy = Literal["id", "name"] | None

logger = logging.getLogger("anaplan_sdk")


class AsyncClient:
    """
    Asynchronous Anaplan Client. For guides and examples
    refer to https://vinzenzklass.github.io/anaplan-sdk.
    """

    def __init__(
        self,
        workspace_id: str | None = None,
        model_id: str | None = None,
        user_email: str | None = None,
        password: str | None = None,
        certificate: str | bytes | None = None,
        private_key: str | bytes | None = None,
        private_key_password: str | bytes | None = None,
        token: str | None = None,
        auth: httpx.Auth | None = None,
        timeout: float | httpx.Timeout = 30,
        retry_count: int = 2,
        backoff: float = 1.0,
        backoff_factor: float = 2.0,
        page_size: int = 5_000,
        status_poll_delay: int = 1,
        upload_chunk_size: int = 25_000_000,
        allow_file_creation: bool = False,
        **httpx_kwargs,
    ) -> None:
        """
        Asynchronous Anaplan Client. For guides and examples
        refer to https://vinzenzklass.github.io/anaplan-sdk.

        :param workspace_id: The Anaplan workspace Id. You can copy this from the browser URL or
               find them using an HTTP Client like Postman, Paw, Insomnia etc.
        :param model_id: The identifier of the model.
        :param user_email: A valid email registered with the Anaplan Workspace you are attempting
               to access.
        :param password: Password for the given `user_email` for basic Authentication.
        :param certificate: The certificate content or the absolute path to the certificate file.
        :param private_key: The private key content or the absolute path to the private key file.
        :param private_key_password: The password to access the private key file. This is only
               considered if you provided a private key file and it password-protected.
        :param token: An Anaplan API Token. This will be used to authenticate the client. If
               sufficient other authentication parameters are provided, the token will be used
               until it expires, after which a new one will be created. If you provide only this
               parameter, the client will raise an error upon first authentication failure. For
               short-lived instances, such as in web applications where user specific clients are
               created, this is the recommended way to authenticate, since this has the least
               overhead.
        :param auth: You can provide a subclass of `httpx.Auth` to use for authentication. You can
               provide an instance of one of the classes provided by the SDK, or an instance of
               your own subclass of `httpx.Auth`. This will give you full control over the
               authentication process, but you will need to implement the entire authentication
               logic yourself.
        :param timeout: The timeout in seconds for the HTTP requests. Alternatively, you can pass
               an instance of `httpx.Timeout` to set the timeout for the HTTP requests.
        :param retry_count: The number of times to retry an HTTP request if it fails. Set this to 0
               to never retry. Defaults to 2, meaning each HTTP Operation will be tried a total
               number of 2 times.
        :param backoff: The initial backoff time in seconds for the retry mechanism. This is the
               time to wait before the first retry.
        :param backoff_factor: The factor by which the backoff time is multiplied after each retry.
               For example, if the initial backoff is 1 second and the factor is 2, the second
               retry will wait 2 seconds, the third retry will wait 4 seconds, and so on.
        :param page_size: The number of items to return per page when paginating through results.
               Defaults to 5000. This is the maximum number of items that can be returned per
               request. If you pass a value greater than 5000, it will be capped to 5000.
        :param status_poll_delay: The delay between polling the status of a task.
        :param upload_chunk_size: The size of the chunks to upload. This is the maximum size of
               each chunk. Defaults to 25MB.
        :param allow_file_creation: Whether to allow the creation of new files. Defaults to False
               since this is typically unintentional and may well be unwanted behaviour in the API
               altogether. A file that is created this way will not be referenced by any action in
               anaplan until manually assigned so there is typically no value in dynamically
               creating new files and uploading content to them.
        :param httpx_kwargs: Additional keyword arguments to pass to the `httpx.AsyncClient`.
               This can be used to set additional options such as proxies, headers, etc. See
               https://www.python-httpx.org/api/#asyncclient for the full list of arguments.
        """
        _auth = auth or _create_auth(
            token=token,
            user_email=user_email,
            password=password,
            certificate=certificate,
            private_key=private_key,
            private_key_password=private_key_password,
        )
        _client = httpx.AsyncClient(auth=_auth, timeout=timeout, **httpx_kwargs)
        self._http = _AsyncHttpService(
            _client,
            retry_count=retry_count,
            backoff=backoff,
            backoff_factor=backoff_factor,
            page_size=page_size,
            poll_delay=status_poll_delay,
        )
        self._workspace_id = workspace_id
        self._model_id = model_id
        self._url = f"https://api.anaplan.com/2/0/workspaces/{workspace_id}/models/{model_id}"
        self._transactional_client = (
            _AsyncTransactionalClient(self._http, model_id) if model_id else None
        )
        self._alm_client = _AsyncAlmClient(self._http, model_id) if model_id else None
        self._audit_client = _AsyncAuditClient(self._http)
        self._scim_client = _AsyncScimClient(self._http)
        self._cloud_works = _AsyncCloudWorksClient(self._http)
        self.upload_chunk_size = upload_chunk_size
        self.allow_file_creation = allow_file_creation
        logger.debug(
            f"Initialized AsyncClient with workspace_id={workspace_id}, model_id={model_id}"
        )

    def with_model(self, model_id: str | None = None, workspace_id: str | None = None) -> Self:
        """
        Create a new instance of the Client with the given model and workspace Ids. **This creates
        a copy of the current client. The current instance remains unchanged.**
        :param workspace_id: The workspace Id to use or None to use the existing workspace Id.
        :param model_id: The model Id to use or None to use the existing model Id.
        :return: A new instance of the Client.
        """
        client = copy(self)
        client._workspace_id = workspace_id or self._workspace_id
        client._model_id = model_id or self._model_id
        logger.debug(
            f"Creating a new AsyncClient from existing instance "
            f"with workspace_id={client._workspace_id}, model_id={client._model_id}."
        )
        client._url = (
            "https://api.anaplan.com/2/0/workspaces"
            f"/{client._workspace_id}/models/{client._model_id}"
        )
        client._transactional_client = _AsyncTransactionalClient(self._http, client._model_id)
        client._alm_client = _AsyncAlmClient(self._http, client._model_id)
        return client

    @property
    def audit(self) -> _AsyncAuditClient:
        """
        The Audit Client provides access to the Anaplan Audit API.
        For details, see https://vinzenzklass.github.io/anaplan-sdk/guides/audit/.
        """
        return self._audit_client

    @property
    def cw(self) -> _AsyncCloudWorksClient:
        """
        The Cloud Works Client provides access to the Anaplan Cloud Works API.
        For details, see https://vinzenzklass.github.io/anaplan-sdk/guides/cloud_works/.
        """
        return self._cloud_works

    @property
    def tr(self) -> _AsyncTransactionalClient:
        """
        The Transactional Client provides access to the Anaplan Transactional API. This is useful
        for more advanced use cases where you need to interact with the Anaplan Model in a more
        granular way.

        If you instantiated the client without the field `model_id`, this will raise a
        `ValueError`, since none of the endpoints can be invoked without the model Id.
        :return: The Transactional Client.
        """
        if not self._transactional_client:
            raise ValueError(
                "Cannot use the Transactional Client (Anaplan Transactional API) "
                "without field `model_id`. Make sure the instance you are trying to call this on "
                "is instantiated correctly with a valid `model_id`."
            )
        return self._transactional_client

    @property
    def alm(self) -> _AsyncAlmClient:
        """
        **To use the Application Lifecycle Management (ALM) API, you need a Professional or
        Enterprise subscription.**

        The ALM Client provides access to the Anaplan ALM API. This is useful for more advanced use
        cases where you need retrieve Meta Information for yours models, read or create revisions,
        spawn sync tasks or generate comparison reports.

        :return: The ALM Client.
        """
        if not self._alm_client:
            raise ValueError(
                "Cannot use the ALM Client (Anaplan ALM API) "
                "without field `model_id`. Make sure the instance you are trying to call this on "
                "is instantiated correctly with a valid `model_id`."
            )
        return self._alm_client

    @property
    def scim(self) -> _AsyncScimClient:
        """
        To use the SCIM API, you must be User Admin. The SCIM API allows managing internal users.
        Visiting users are excluded from the SCIM API.
        :return: The SCIM Client.
        """
        return self._scim_client

    async def get_workspace(self, workspace_id: str | None = None) -> Workspace:
        """
        Retrieves the Workspace with the given Id, or the Workspace of the current instance if no Id
        is given. If no Id is given and the instance has no workspace Id, this will
        raise a ValueError.
        :param workspace_id: The identifier of the Workspace to retrieve.
        :return: The Workspace.
        """
        ws_id = workspace_id or self._workspace_id
        if not ws_id:
            raise ValueError(
                "No `workspace_id` provided and the client instance has no `workspace_id`. "
                "Cannot retrieve Workspace."
            )
        res = await self._http.get(
            f"https://api.anaplan.com/2/0/workspaces/{ws_id}", params={"tenantDetails": "true"}
        )
        return Workspace.model_validate(res["workspace"])

    async def get_workspaces(
        self,
        search_pattern: str | None = None,
        sort_by: Literal["size_allowance", "name"] | None = None,
        descending: bool = False,
    ) -> list[Workspace]:
        """
        Lists all the Workspaces the authenticated user has access to.
        :param search_pattern: **Caution: This is an undocumented Feature and may behave
               unpredictably. It requires the Tenant Admin role. For non-admin users, it is
               ignored.** Optionally filter for specific workspaces. When provided,
               case-insensitive matches workspaces with names containing this string.
               You can use the wildcards `%` for 0-n characters, and `_` for exactly 1 character.
               When None (default), returns all users.
        :param sort_by: The field to sort the results by.
        :param descending: If True, the results will be sorted in descending order.
        :return: The List of Workspaces.
        """
        params = {"tenantDetails": "true"} | sort_params(sort_by, descending)
        if search_pattern:
            params["s"] = search_pattern
        res = await self._http.get_paginated(
            "https://api.anaplan.com/2/0/workspaces", "workspaces", params=params
        )
        return [Workspace.model_validate(e) for e in res]

    async def get_model(self, model_id: str | None = None) -> Model:
        """
        Retrieves the Model with the given Id, or the Model of the current instance if no Id
        is given. If no Id is given and the instance has no model Id, this will raise a ValueError.
        :param model_id: The identifier of the Model to retrieve.
        :return: The Model.
        """
        _model_id = model_id or self._model_id
        if not _model_id:
            raise ValueError(
                "No `model_id` provided and the client instance has no `model_id`. "
                "Cannot retrieve Model."
            )
        res = await self._http.get(
            f"https://api.anaplan.com/2/0/models/{_model_id}", params={"modelDetails": "true"}
        )
        return Model.model_validate(res["model"])

    async def get_models(
        self,
        only_in_workspace: bool | str = False,
        search_pattern: str | None = None,
        sort_by: Literal["active_state", "name"] | None = None,
        descending: bool = False,
    ) -> list[Model]:
        """
        Lists all the Models the authenticated user has access to.
        :param only_in_workspace: If True, only lists models in the workspace provided when
               instantiating the client. If a string is provided, only lists models in the workspace
               with the given Id. If False (default), lists models in all workspaces the user
        :param search_pattern:  **Caution: This is an undocumented Feature and may behave
               unpredictably. It requires the Tenant Admin role. For non-admin users, it is
               ignored.** Optionally filter for specific models. When provided,
               case-insensitive matches model names containing this string.
               You can use the wildcards `%` for 0-n characters, and `_` for exactly 1 character.
               When None (default), returns all models.
        :param sort_by: The field to sort the results by.
        :param descending: If True, the results will be sorted in descending order.
        :return: The List of Models.
        """
        params = {"modelDetails": "true"} | sort_params(sort_by, descending)
        if search_pattern:
            params["s"] = search_pattern
        res = await self._http.get_paginated(
            models_url(only_in_workspace, self._workspace_id), "models", params=params
        )
        return [Model.model_validate(e) for e in res]

    async def delete_models(self, model_ids: list[str]) -> ModelDeletionResult:
        """
        Delete the given Models. Models need to be closed before they can be deleted. If one of the
        deletions fails, the other deletions will still be attempted and may complete.
        :param model_ids: The list of Model identifiers to delete.
        :return:
        """
        logger.info(f"Deleting Models: {', '.join(model_ids)}.")
        res = await self._http.post(
            f"https://api.anaplan.com/2/0/workspaces/{self._workspace_id}/bulkDeleteModels",
            json={"modelIdsToDelete": model_ids},
        )
        return ModelDeletionResult.model_validate(res)

    async def get_files(self, sort_by: SortBy = None, descending: bool = False) -> list[File]:
        """
        Lists all the Files in the Model.
        :param sort_by: The field to sort the results by.
        :param descending: If True, the results will be sorted in descending order.
        :return: The List of Files.
        """
        res = await self._http.get_paginated(
            f"{self._url}/files", "files", params=sort_params(sort_by, descending)
        )
        return [File.model_validate(e) for e in res]

    async def get_actions(self, sort_by: SortBy = None, descending: bool = False) -> list[Action]:
        """
        Lists all the Actions in the Model. This will only return the Actions listed under
        `Other Actions` in Anaplan. For Imports, exports, and processes, see their respective
        methods instead.
        :param sort_by: The field to sort the results by.
        :param descending: If True, the results will be sorted in descending order.
        :return: The List of Actions.
        """
        res = await self._http.get_paginated(
            f"{self._url}/actions", "actions", params=sort_params(sort_by, descending)
        )
        return [Action.model_validate(e) for e in res]

    async def get_processes(
        self, sort_by: SortBy = None, descending: bool = False
    ) -> list[Process]:
        """
        Lists all the Processes in the Model.
        :param sort_by: The field to sort the results by.
        :param descending: If True, the results will be sorted in descending order.
        :return: The List of Processes.
        """
        res = await self._http.get_paginated(
            f"{self._url}/processes", "processes", params=sort_params(sort_by, descending)
        )
        return [Process.model_validate(e) for e in res]

    async def get_imports(self, sort_by: SortBy = None, descending: bool = False) -> list[Import]:
        """
        Lists all the Imports in the Model.
        :param sort_by: The field to sort the results by.
        :param descending: If True, the results will be sorted in descending order.
        :return: The List of Imports.
        """
        res = await self._http.get_paginated(
            f"{self._url}/imports", "imports", params=sort_params(sort_by, descending)
        )
        return [Import.model_validate(e) for e in res]

    async def get_exports(self, sort_by: SortBy = None, descending: bool = False) -> list[Export]:
        """
        Lists all the Exports in the Model.
        :param sort_by: The field to sort the results by.
        :param descending: If True, the results will be sorted in descending order.
        :return: The List of Exports.
        """
        res = await self._http.get_paginated(
            f"{self._url}/exports", "exports", params=sort_params(sort_by, descending)
        )
        return [Export.model_validate(e) for e in res]

    async def run_action(self, action_id: int, wait_for_completion: bool = True) -> TaskStatus:
        """
        Runs the Action and validates the spawned task. If the Action fails or completes with
        errors, this will raise an AnaplanActionError. Failed Tasks are often not something you
        can recover from at runtime and often require manual changes in Anaplan, i.e. updating the
        mapping of an Import or similar.
        :param action_id: The identifier of the Action to run. Can be any Anaplan Invokable;
               Processes, Imports, Exports, Other Actions.
        :param wait_for_completion: If True, the method will poll the task status and not return
               until the task is complete. If False, it will spawn the task and return immediately.
        """
        body = {"localeName": "en_US"}
        res = await self._http.post(
            f"{self._url}/{action_url(action_id)}/{action_id}/tasks", json=body
        )
        task_id = res["task"]["taskId"]
        logger.info(f"Invoked Action '{action_id}', spawned Task: '{task_id}'.")

        if not wait_for_completion:
            return TaskStatus.model_validate(await self.get_task_status(action_id, task_id))
        status = await self._http.poll_task(self.get_task_status, action_id, task_id)
        if status.task_state == "COMPLETE" and not status.result.successful:
            logger.error(f"Task '{task_id}' completed with errors.")
            raise AnaplanActionError(f"Task '{task_id}' completed with errors.")

        logger.info(f"Task '{task_id}' of '{action_id}' completed successfully.")
        return status

    async def get_file(self, file_id: int) -> bytes:
        """
        Retrieves the content of the specified file.
        :param file_id: The identifier of the file to retrieve.
        :return: The content of the file.
        """
        chunk_count = await self._file_pre_check(file_id)
        logger.info(f"File {file_id} has {chunk_count} chunks.")
        if chunk_count <= 1:
            return await self._http.get_binary(f"{self._url}/files/{file_id}")
        return b"".join(
            await gather(
                *(
                    self._http.get_binary(f"{self._url}/files/{file_id}/chunks/{i}")
                    for i in range(chunk_count)
                )
            )
        )

    async def get_file_stream(self, file_id: int, batch_size: int = 1) -> AsyncIterator[bytes]:
        """
        Retrieves the content of the specified file as a stream of chunks. The chunks are yielded
        one by one, so you can process them as they arrive. This is useful for large files where
        you don't want to or cannot load the entire file into memory at once.
        :param file_id: The identifier of the file to retrieve.
        :param batch_size: Number of chunks to fetch concurrently. If > 1, n chunks will be fetched
               concurrently. This still yields each chunk individually, only the requests are
               batched. If 1 (default), each chunk is fetched sequentially.
        :return: A generator yielding the chunks of the file.
        """
        chunk_count = await self._file_pre_check(file_id)
        logger.info(f"File {file_id} has {chunk_count} chunks.")
        if chunk_count <= 1:
            yield await self._http.get_binary(f"{self._url}/files/{file_id}")
            return

        for batch_start in range(0, chunk_count, batch_size):
            batch_chunks = await gather(
                *(
                    self._http.get_binary(f"{self._url}/files/{file_id}/chunks/{i}")
                    for i in range(batch_start, min(batch_start + batch_size, chunk_count))
                )
            )
            for chunk in batch_chunks:
                yield chunk

    async def upload_file(self, file_id: int, content: str | bytes) -> None:
        """
        Uploads the content to the specified file. If there are several chunks, upload of
        individual chunks are uploaded concurrently.

        :param file_id: The identifier of the file to upload to.
        :param content: The content to upload. **This Content will be compressed before uploading.
               If you are passing the Input as bytes, pass it uncompressed.**
        """
        chunks = [
            content[i : i + self.upload_chunk_size]
            for i in range(0, len(content), self.upload_chunk_size)
        ]
        logger.info(f"Content for file '{file_id}' will be uploaded in {len(chunks)} chunks.")
        await self._set_chunk_count(file_id, len(chunks))
        await gather(
            *(self._upload_chunk(file_id, index, chunk) for index, chunk in enumerate(chunks))
        )

        logger.info(f"Completed upload for file '{file_id}'.")

    async def upload_file_stream(
        self,
        file_id: int,
        content: AsyncIterator[bytes | str] | Iterator[str | bytes],
        batch_size: int = 1,
    ) -> None:
        """
        Uploads the content to the specified file as a stream of chunks. This is useful either for
        large files where you don't want to or cannot load the entire file into memory at once, or
        if you simply do not know the number of chunks ahead of time and instead just want to pass
        on chunks i.e. consumed from a queue until it is exhausted. In this case, you can pass a
        generator that yields the chunks of the file one by one to this method.

        :param file_id: The identifier of the file to upload to.
        :param content: An Iterator or AsyncIterator yielding the chunks of the file. You can pass
               any Iterator, but you will most likely want to pass a Generator.
        :param batch_size: Number of chunks to upload concurrently. If > 1, n chunks will be
               uploaded concurrently. This can be useful if you either do not control the chunk
               size, or if you want to keep the chunk size small but still want some concurrency.
        """
        logger.info(f"Starting upload stream for file '{file_id}' with batch size {batch_size}.")
        await self._set_chunk_count(file_id, -1)
        tasks = []
        if isinstance(content, Iterator):
            for index, chunk in enumerate(content):
                tasks.append(self._upload_chunk(file_id, index, chunk))
                if len(tasks) == max(batch_size, 1):
                    await gather(*tasks)
                    logger.info(
                        f"Completed upload stream batch of size {batch_size} for file {file_id}."
                    )
                    tasks = []
        else:
            index = 0
            async for chunk in content:
                tasks.append(self._upload_chunk(file_id, index, chunk))
                index += 1
                if len(tasks) == max(batch_size, 1):
                    await gather(*tasks)
                    logger.info(
                        f"Completed upload stream batch of size {batch_size} for file {file_id}."
                    )
                    tasks = []
        if tasks:
            await gather(*tasks)
            logger.info(
                f"Completed final upload stream batch of size {len(tasks)} for file {file_id}."
            )
        await self._http.post(f"{self._url}/files/{file_id}/complete", json={"id": file_id})
        logger.info(f"Completed upload stream for '{file_id}'.")

    async def upload_and_import(
        self, file_id: int, content: str | bytes, action_id: int, wait_for_completion: bool = True
    ) -> TaskStatus:
        """
        Convenience wrapper around `upload_file()` and `run_action()` to upload content to a file
        and run an import action in one call.
        :param file_id: The identifier of the file to upload to.
        :param content: The content to upload. **This Content will be compressed before uploading.
               If you are passing the Input as bytes, pass it uncompressed to avoid redundant
               work.**
        :param action_id: The identifier of the action to run after uploading the content.
        :param wait_for_completion: If True, the method will poll the import task status and not
               return until the task is complete. If False, it will spawn the import task and
               return immediately.
        """
        await self.upload_file(file_id, content)
        return await self.run_action(action_id, wait_for_completion)

    async def export_and_download(self, action_id: int) -> bytes:
        """
        Convenience wrapper around `run_action()` and `get_file()` to run an export action and
        download the exported content in one call.
        :param action_id: The identifier of the action to run.
        :return: The content of the exported file.
        """
        await self.run_action(action_id)
        return await self.get_file(action_id)

    async def get_task_summaries(self, action_id: int) -> list[TaskSummary]:
        """
        Retrieves the status of all tasks spawned by the specified action.
        :param action_id: The identifier of the action that was invoked.
        :return: The list of tasks spawned by the action.
        """
        return [
            TaskSummary.model_validate(e)
            for e in await self._http.get_paginated(
                f"{self._url}/{action_url(action_id)}/{action_id}/tasks", "tasks"
            )
        ]

    async def get_task_status(self, action_id: int, task_id: str) -> TaskStatus:
        """
        Retrieves the status of the specified task.
        :param action_id: The identifier of the action that was invoked.
        :param task_id: The identifier of the spawned task.
        :return: The status of the task.
        """
        return TaskStatus.model_validate(
            (
                await self._http.get(
                    f"{self._url}/{action_url(action_id)}/{action_id}/tasks/{task_id}"
                )
            ).get("task")
        )

    async def get_optimizer_log(self, action_id: int, task_id: str) -> bytes:
        """
        Retrieves the solution logs of the specified optimization action task.
        :param action_id: The identifier of the optimization action that was invoked.
        :param task_id: The Task identifier, sometimes also referred to as the Correlation Id.
        :return: The content of the solution logs.
        """
        return await self._http.get_binary(
            f"{self._url}/optimizeActions/{action_id}/tasks/{task_id}/solutionLogs"
        )

    async def _file_pre_check(self, file_id: int) -> int:
        file = next((f for f in await self.get_files() if f.id == file_id), None)
        if not file:
            raise InvalidIdentifierException(f"File {file_id} not found.")
        return file.chunk_count

    async def _upload_chunk(self, file_id: int, index: int, chunk: str | bytes) -> None:
        await self._http.put_binary_gzip(f"{self._url}/files/{file_id}/chunks/{index}", chunk)
        logger.debug(f"Chunk {index} loaded to file '{file_id}'.")

    async def _set_chunk_count(self, file_id: int, num_chunks: int) -> None:
        if not self.allow_file_creation and not (113000000000 <= file_id <= 113999999999):
            raise InvalidIdentifierException(
                f"File with Id {file_id} does not exist. If you want to dynamically create files "
                "to avoid this error, set `allow_file_creation=True` on the calling instance. "
                "Make sure you have understood the implications of this before doing so. "
            )
        response = await self._http.post(
            f"{self._url}/files/{file_id}", json={"chunkCount": num_chunks}
        )
        optionally_new_file = int(response.get("file").get("id"))
        if optionally_new_file != file_id:
            if self.allow_file_creation:
                logger.info(f"Created new file with name '{file_id}', Id is {optionally_new_file}.")
                return
            raise InvalidIdentifierException(
                f"File with Id {file_id} did not exist and was created in Anaplan. You may want to "
                f"ask a model builder to remove it. If you want to dynamically create files "
                "to avoid this error, set `allow_file_creation=True` on the calling instance. "
                "Make sure you have understood the implications of this before doing so."
            )
