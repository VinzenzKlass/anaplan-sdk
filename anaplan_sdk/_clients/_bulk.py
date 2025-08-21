import logging
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
from copy import copy
from typing import Iterator

import httpx
from typing_extensions import Self

from anaplan_sdk._auth import _create_auth
from anaplan_sdk._services import _HttpService, action_url
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

from ._alm import _AlmClient
from ._audit import _AuditClient
from ._cloud_works import _CloudWorksClient
from ._transactional import _TransactionalClient

logger = logging.getLogger("anaplan_sdk")


class Client:
    """
    Synchronous Anaplan Client. For guides and examples
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
        upload_parallel: bool = True,
        upload_chunk_size: int = 25_000_000,
        allow_file_creation: bool = False,
        **httpx_kwargs,
    ) -> None:
        """
        Synchronous Anaplan Client. For guides and examples
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
        :param backoff: The initial backoff time in seconds for the retry mechanism. This is the
               time to wait before the first retry.
        :param backoff_factor: The factor by which the backoff time is multiplied after each retry.
               For example, if the initial backoff is 1 second and the factor is 2, the second
               retry will wait 2 seconds, the third retry will wait 4 seconds, and so on.
               number of 2 times.
        :param page_size: The number of items to return per page when paginating through results.
               Defaults to 5000. This is the maximum number of items that can be returned per
               request. If you pass a value greater than 5000, it will be capped to 5000.
        :param status_poll_delay: The delay between polling the status of a task.
        :param upload_parallel: Whether to upload chunks in parallel when uploading files.
        :param upload_chunk_size: The size of the chunks to upload. This is the maximum size of
               each chunk. Defaults to 25MB.
        :param allow_file_creation: Whether to allow the creation of new files. Defaults to False
               since this is typically unintentional and may well be unwanted behaviour in the API
               altogether. A file that is created this way will not be referenced by any action in
               anaplan until manually assigned so there is typically no value in dynamically
               creating new files and uploading content to them.
        :param httpx_kwargs: Additional keyword arguments to pass to the `httpx.Client`.
               This can be used to set additional options such as proxies, headers, etc. See
               https://www.python-httpx.org/api/#client for the full list of arguments.
        """
        auth = auth or _create_auth(
            token=token,
            user_email=user_email,
            password=password,
            certificate=certificate,
            private_key=private_key,
            private_key_password=private_key_password,
        )
        _client = httpx.Client(auth=auth, timeout=timeout, **httpx_kwargs)
        self._http = _HttpService(
            _client,
            retry_count=retry_count,
            backoff=backoff,
            backoff_factor=backoff_factor,
            page_size=page_size,
            poll_delay=status_poll_delay,
        )
        self._retry_count = retry_count
        self._workspace_id = workspace_id
        self._model_id = model_id
        self._url = f"https://api.anaplan.com/2/0/workspaces/{workspace_id}/models/{model_id}"
        self._transactional_client = (
            _TransactionalClient(self._http, model_id) if model_id else None
        )
        self._alm_client = _AlmClient(self._http, model_id) if model_id else None
        self._cloud_works = _CloudWorksClient(self._http)
        self._thread_count = multiprocessing.cpu_count()
        self._audit = _AuditClient(self._http)
        self.status_poll_delay = status_poll_delay
        self.upload_parallel = upload_parallel
        self.upload_chunk_size = upload_chunk_size
        self.allow_file_creation = allow_file_creation
        logger.debug(f"Initialized Client with workspace_id={workspace_id}, model_id={model_id}")

    @classmethod
    def from_existing(
        cls, existing: Self, *, workspace_id: str | None = None, model_id: str | None = None
    ) -> Self:
        """
        Create a new instance of the Client from an existing instance. This is useful if you want
        to interact with multiple models or workspaces in the same script but share the same
        authentication and configuration. This creates a shallow copy of the existing client and
        optionally updates the relevant attributes to the new workspace and model. You can provide
        either a new workspace Id or a new model Id, or both. If you do not provide one of them,
        the existing value will be used. If you omit both, the new instance will be an identical
        copy of the existing instance.

        :param existing: The existing instance to copy.
        :param workspace_id: The workspace Id to use or None to use the existing workspace Id.
        :param model_id: The model Id to use or None to use the existing model Id.
        :return: A new instance of the Client.
        """
        client = copy(existing)
        new_ws_id = workspace_id or existing._workspace_id
        new_model_id = model_id or existing._model_id
        logger.debug(
            f"Creating a new AsyncClient from existing instance "
            f"with workspace_id={new_ws_id}, model_id={new_model_id}."
        )
        client._url = f"https://api.anaplan.com/2/0/workspaces/{new_ws_id}/models/{new_model_id}"
        client._transactional_client = _TransactionalClient(existing._http, new_model_id)
        client._alm_client = _AlmClient(existing._http, new_model_id)
        return client

    @property
    def audit(self) -> _AuditClient:
        """
        The Audit Client provides access to the Anaplan Audit API.
        For details, see https://vinzenzklass.github.io/anaplan-sdk/guides/audit/.
        """
        return self._audit

    @property
    def cw(self) -> _CloudWorksClient:
        """
        The Cloud Works Client provides access to the Anaplan Cloud Works API.
        For details, see https://vinzenzklass.github.io/anaplan-sdk/guides/cloud_works/.
        """
        return self._cloud_works

    @property
    def tr(self) -> _TransactionalClient:
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
    def alm(self) -> _AlmClient:
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

    def get_workspaces(self, search_pattern: str | None = None) -> list[Workspace]:
        """
        Lists all the Workspaces the authenticated user has access to.
        :param search_pattern: Optional filter for workspaces. When provided, case-insensitive
               matches workspaces with names containing this string. When None (default),
               returns all workspaces.
        :return: The List of Workspaces.
        """
        params = {"tenantDetails": "true"}
        if search_pattern:
            params["s"] = search_pattern
        return [
            Workspace.model_validate(e)
            for e in self._http.get_paginated(
                "https://api.anaplan.com/2/0/workspaces", "workspaces", params=params
            )
        ]

    def get_models(self, search_pattern: str | None = None) -> list[Model]:
        """
        Lists all the Models the authenticated user has access to.
        :param search_pattern: Optionally filter for specific models. When provided,
               case-insensitive matches model names containing this string.
               You can use the wildcards `%` for 0-n characters, and `_` for exactly 1 character.
               When None (default), returns all models.
        :return: The List of Models.
        """
        params = {"modelDetails": "true"}
        if search_pattern:
            params["s"] = search_pattern
        return [
            Model.model_validate(e)
            for e in self._http.get_paginated(
                "https://api.anaplan.com/2/0/models", "models", params=params
            )
        ]

    def delete_models(self, model_ids: list[str]) -> ModelDeletionResult:
        """
        Delete the given Models. Models need to be closed before they can be deleted. If one of the
        deletions fails, the other deletions will still be attempted and may complete.
        :param model_ids: The list of Model identifiers to delete.
        :return:
        """
        logger.info(f"Deleting Models: {', '.join(model_ids)}.")
        res = self._http.post(
            f"https://api.anaplan.com/2/0/workspaces/{self._workspace_id}/bulkDeleteModels",
            json={"modelIdsToDelete": model_ids},
        )
        return ModelDeletionResult.model_validate(res)

    def get_files(self) -> list[File]:
        """
        Lists all the Files in the Model.
        :return: The List of Files.
        """
        return [
            File.model_validate(e) for e in self._http.get_paginated(f"{self._url}/files", "files")
        ]

    def get_actions(self) -> list[Action]:
        """
        Lists all the Actions in the Model. This will only return the Actions listed under
        `Other Actions` in Anaplan. For Imports, exports, and processes, see their respective
        methods instead.
        :return: The List of Actions.
        """
        return [
            Action.model_validate(e)
            for e in self._http.get_paginated(f"{self._url}/actions", "actions")
        ]

    def get_processes(self) -> list[Process]:
        """
        Lists all the Processes in the Model.
        :return: The List of Processes.
        """
        return [
            Process.model_validate(e)
            for e in self._http.get_paginated(f"{self._url}/processes", "processes")
        ]

    def get_imports(self) -> list[Import]:
        """
        Lists all the Imports in the Model.
        :return: The List of Imports.
        """
        return [
            Import.model_validate(e)
            for e in self._http.get_paginated(f"{self._url}/imports", "imports")
        ]

    def get_exports(self) -> list[Export]:
        """
        Lists all the Exports in the Model.
        :return: The List of Exports.
        """
        return [
            Export.model_validate(e)
            for e in (self._http.get(f"{self._url}/exports")).get("exports", [])
        ]

    def run_action(self, action_id: int, wait_for_completion: bool = True) -> TaskStatus:
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
        res = self._http.post(f"{self._url}/{action_url(action_id)}/{action_id}/tasks", json=body)
        task_id = res["task"]["taskId"]
        logger.info(f"Invoked Action '{action_id}', spawned Task: '{task_id}'.")

        if not wait_for_completion:
            return TaskStatus.model_validate(self.get_task_status(action_id, task_id))
        status = self._http.poll_task(self.get_task_status, action_id, task_id)
        if status.task_state == "COMPLETE" and not status.result.successful:
            logger.error(f"Task '{task_id}' completed with errors.")
            raise AnaplanActionError(f"Task '{task_id}' completed with errors.")

        logger.info(f"Task '{task_id}' of Action '{action_id}' completed successfully.")
        return status

    def get_file(self, file_id: int) -> bytes:
        """
        Retrieves the content of the specified file.
        :param file_id: The identifier of the file to retrieve.
        :return: The content of the file.
        """
        chunk_count = self._file_pre_check(file_id)
        logger.info(f"File {file_id} has {chunk_count} chunks.")
        if chunk_count <= 1:
            return self._http.get_binary(f"{self._url}/files/{file_id}")
        with ThreadPoolExecutor(max_workers=self._thread_count) as executor:
            chunks = executor.map(
                self._http.get_binary,
                (f"{self._url}/files/{file_id}/chunks/{i}" for i in range(chunk_count)),
            )
            return b"".join(chunks)

    def get_file_stream(self, file_id: int, batch_size: int = 1) -> Iterator[bytes]:
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
        chunk_count = self._file_pre_check(file_id)
        logger.info(f"File {file_id} has {chunk_count} chunks.")
        if chunk_count <= 1:
            yield self._http.get_binary(f"{self._url}/files/{file_id}")
            return

        with ThreadPoolExecutor(max_workers=batch_size) as executor:
            for batch_start in range(0, chunk_count, batch_size):
                batch_chunks = executor.map(
                    self._http.get_binary,
                    (
                        f"{self._url}/files/{file_id}/chunks/{i}"
                        for i in range(batch_start, min(batch_start + batch_size, chunk_count))
                    ),
                )
                for chunk in batch_chunks:
                    yield chunk

    def upload_file(self, file_id: int, content: str | bytes) -> None:
        """
        Uploads the content to the specified file. If there are several chunks, upload of
        individual chunks are uploaded concurrently.

        :param file_id: The identifier of the file to upload to.
        :param content: The content to upload. **This Content will be compressed before uploading.
               If you are passing the Input as bytes, pass it uncompressed.**
        """
        if isinstance(content, str):
            content = content.encode()
        chunks = [
            content[i : i + self.upload_chunk_size]
            for i in range(0, len(content), self.upload_chunk_size)
        ]
        logger.info(f"Content for file '{file_id}' will be uploaded in {len(chunks)} chunks.")
        self._set_chunk_count(file_id, len(chunks))
        if self.upload_parallel:
            with ThreadPoolExecutor(max_workers=self._thread_count) as executor:
                executor.map(
                    self._upload_chunk, (file_id,) * len(chunks), range(len(chunks)), chunks
                )
        else:
            for index, chunk in enumerate(chunks):
                self._upload_chunk(file_id, index, chunk)
        logger.info(f"Completed upload for file '{file_id}'.")

    def upload_file_stream(
        self, file_id: int, content: Iterator[str | bytes], batch_size: int = 1
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
        self._set_chunk_count(file_id, -1)
        indices, chunks = [], []
        with ThreadPoolExecutor(max_workers=batch_size) as executor:
            for index, chunk in enumerate(content):
                indices.append(index)
                chunks.append(chunk)
                if len(indices) == max(batch_size, 1):
                    list(
                        executor.map(self._upload_chunk, (file_id,) * len(indices), indices, chunks)
                    )
                    logger.info(
                        f"Completed upload stream batch of size {batch_size} for file {file_id}."
                    )
                    indices, chunks = [], []

            if indices:
                executor.map(self._upload_chunk, (file_id,) * len(indices), indices, chunks)
        logger.info(
            f"Completed final upload stream batch of size {len(indices)} for file {file_id}."
        )
        self._http.post(f"{self._url}/files/{file_id}/complete", json={"id": file_id})
        logger.info(f"Completed upload stream for '{file_id}'.")

    def upload_and_import(
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
        self.upload_file(file_id, content)
        return self.run_action(action_id, wait_for_completion)

    def export_and_download(self, action_id: int) -> bytes:
        """
        Convenience wrapper around `run_action()` and `get_file()` to run an export action and
        download the exported content in one call.
        :param action_id: The identifier of the action to run.
        :return: The content of the exported file.
        """
        self.run_action(action_id)
        return self.get_file(action_id)

    def get_task_summaries(self, action_id: int) -> list[TaskSummary]:
        """
        Retrieves the status of all tasks spawned by the specified action.
        :param action_id: The identifier of the action that was invoked.
        :return: The list of tasks spawned by the action.
        """
        return [
            TaskSummary.model_validate(e)
            for e in self._http.get_paginated(
                f"{self._url}/{action_url(action_id)}/{action_id}/tasks", "tasks"
            )
        ]

    def get_task_status(self, action_id: int, task_id: str) -> TaskStatus:
        """
        Retrieves the status of the specified task.
        :param action_id: The identifier of the action that was invoked.
        :param task_id: The identifier of the spawned task.
        :return: The status of the task.
        """
        return TaskStatus.model_validate(
            self._http.get(f"{self._url}/{action_url(action_id)}/{action_id}/tasks/{task_id}").get(
                "task"
            )
        )

    def get_optimizer_log(self, action_id: int, task_id: str) -> bytes:
        """
        Retrieves the solution logs of the specified optimization action task.
        :param action_id: The identifier of the optimization action that was invoked.
        :param task_id: The Task identifier, sometimes also referred to as the Correlation Id.
        :return: The content of the solution logs.
        """
        return self._http.get_binary(
            f"{self._url}/optimizeActions/{action_id}/tasks/{task_id}/solutionLogs"
        )

    def _file_pre_check(self, file_id: int) -> int:
        file = next((f for f in self.get_files() if f.id == file_id), None)
        if not file:
            raise InvalidIdentifierException(f"File {file_id} not found.")
        return file.chunk_count

    def _upload_chunk(self, file_id: int, index: int, chunk: str | bytes) -> None:
        self._http.put_binary_gzip(f"{self._url}/files/{file_id}/chunks/{index}", chunk)
        logger.debug(f"Chunk {index} loaded to file '{file_id}'.")

    def _set_chunk_count(self, file_id: int, num_chunks: int) -> None:
        logger.debug(f"Setting chunk count for file '{file_id}' to {num_chunks}.")
        if not self.allow_file_creation and not (113000000000 <= file_id <= 113999999999):
            raise InvalidIdentifierException(
                f"File with Id {file_id} does not exist. If you want to dynamically create files "
                "to avoid this error, set `allow_file_creation=True` on the calling instance. "
                "Make sure you have understood the implications of this before doing so. "
            )
        response = self._http.post(f"{self._url}/files/{file_id}", json={"chunkCount": num_chunks})
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
