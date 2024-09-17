"""
Asynchronous Client.
"""

import logging
import time
from asyncio import gather
from copy import copy

import httpx
from typing_extensions import Self

from anaplan_sdk._auth import AnaplanBasicAuth, AnaplanCertAuth, get_certificate, get_private_key
from anaplan_sdk._base import _AsyncBaseClient, action_url
from anaplan_sdk.exceptions import AnaplanActionError, InvalidIdentifierException
from anaplan_sdk.models import Action, Export, File, Import, Model, Process, Workspace

from ._alm import _AsyncAlmClient
from ._transactional import _AsyncTransactionalClient

logging.getLogger("httpx").setLevel(logging.CRITICAL)
logger = logging.getLogger("anaplan_sdk")


class AsyncClient(_AsyncBaseClient):
    """
    An asynchronous Client for pythonic access to the
    [Anaplan Integration API v2](https://anaplan.docs.apiary.io/). This Client provides high-level
    abstractions over the API, so you can deal with python objects and simple functions rather than
    implementation details like http, json, compression, chunking etc.


    For more information, quick start guides and detailed instructions refer to:
    [Anaplan SDK](https://vinzenzklass.github.io/anaplan-sdk).
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
        timeout: float = 30,
        retry_count: int = 2,
        status_poll_delay: int = 1,
        upload_chunk_size: int = 25_000_000,
        allow_file_creation: bool = False,
    ) -> None:
        """
        An asynchronous Client for pythonic access to the Anaplan Integration API v2:
        https://anaplan.docs.apiary.io/. This Client provides high-level abstractions over the API,
        so you can deal with python objects and simple functions rather than implementation details
        like http, json, compression, chunking etc.


        For more information, quick start guides and detailed instructions refer to:
        https://vinzenzklass.github.io/anaplan-sdk.

        :param workspace_id: The Anaplan workspace Id. You can copy this from the browser URL or
                             find them using an HTTP Client like Postman, Paw, Insomnia etc.
        :param model_id: The identifier of the model.
        :param user_email: A valid email registered with the Anaplan Workspace you are attempting
                           to access. **The associated user must have Workspace Admin privileges**
        :param password: Password for the given `user_email`. This is not suitable for production
                         setups. If you intend to use this in production, acquire a client
                         certificate as described under: https://help.anaplan.com/procure-ca-certificates-47842267-2cb3-4e38-90bf-13b1632bcd44
        :param certificate: The absolute path to the client certificate file or the certificate
                            itself.
        :param private_key: The absolute path to the private key file or the private key itself.
        :param private_key_password: The password to access the private key if there is one.
        :param timeout: The timeout in seconds for the HTTP requests.
        :param retry_count: The number of times to retry an HTTP request if it fails. Set this to 0
                            to never retry. Defaults to 2, meaning each HTTP Operation will be
                            tried a total number of 2 times.
        :param status_poll_delay: The delay between polling the status of a task.
        :param upload_chunk_size: The size of the chunks to upload. This is the maximum size of
                                  each chunk. Defaults to 25MB.
        :param allow_file_creation: Whether to allow the creation of new files. Defaults to False
                            since this is typically unintentional and may well be unwanted
                            behaviour in the API altogether. A file that is created this
                            way will not be referenced by any action in anaplan until
                            manually assigned so there is typically no value in dynamically
                            creating new files and uploading content to them.
        """
        if not ((user_email and password) or (certificate and private_key)):
            raise ValueError(
                "Must provide `certificate` and `private_key` or `user_email` and `password`."
                "If you Private Key is Password protected, must also pass `private_key_password`."
            )
        self._client = httpx.AsyncClient(
            auth=(
                AnaplanCertAuth(
                    get_certificate(certificate), get_private_key(private_key, private_key_password)
                )
                if certificate
                else AnaplanBasicAuth(user_email=user_email, password=password)
            ),
            timeout=timeout,
        )
        self._retry_count = retry_count
        self._url = f"https://api.anaplan.com/2/0/workspaces/{workspace_id}/models/{model_id}"
        self._transactional_client = (
            _AsyncTransactionalClient(self._client, model_id, retry_count) if model_id else None
        )
        self._alm_client = (
            _AsyncAlmClient(self._client, model_id, self._retry_count) if model_id else None
        )
        self.status_poll_delay = status_poll_delay
        self.upload_chunk_size = upload_chunk_size
        self.allow_file_creation = allow_file_creation
        super().__init__(retry_count, self._client)

    @classmethod
    def from_existing(cls, existing: Self, workspace_id: str, model_id: str) -> Self:
        """
        Create a new instance of the Client from an existing instance. This is useful if you want
        to interact with multiple models or workspaces in the same script but share the same
        authentication and configuration. This creates a shallow copy of the existing client and
        update the relevant attributes to the new workspace and model.
        :param existing: The existing instance to copy.
        :param workspace_id: The workspace Id to use.
        :param model_id: The model Id to use.
        :return: A new instance of the Client.
        """
        client = copy(existing)
        client._url = f"https://api.anaplan.com/2/0/workspaces/{workspace_id}/models/{model_id}"
        client._transactional_client = _AsyncTransactionalClient(
            existing._client, model_id, existing._retry_count
        )
        return client

    @property
    def transactional(self) -> _AsyncTransactionalClient:
        """
        The Transactional Client provides access to the Anaplan Transactional API. This is useful
        for more advanced use cases where you need to interact with the Anaplan Model in a more
        granular way.

        If you instantiated the client without the field `model_id`, this will raise a
        :py:class:`ValueError`, since none of the endpoints can be invoked without the model Id.
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

    async def list_workspaces(self) -> list[Workspace]:
        """
        Lists all the Workspaces the authenticated user has access to.
        :return: The List of Workspaces.
        """
        return [
            Workspace.model_validate(e)
            for e in (
                await self._get("https://api.anaplan.com/2/0/workspaces?tenantDetails=true")
            ).get("workspaces", [])
        ]

    async def list_models(self) -> list[Model]:
        """
        Lists all the Models the authenticated user has access to.
        :return: The List of Models.
        """
        return [
            Model.model_validate(e)
            for e in (await self._get("https://api.anaplan.com/2/0/models?modelDetails=true")).get(
                "models", []
            )
        ]

    async def list_files(self) -> list[File]:
        """
        Lists all the Files in the Model.
        :return: The List of Files.
        """
        return [
            File.model_validate(e) for e in (await self._get(f"{self._url}/files")).get("files", [])
        ]

    async def list_actions(self) -> list[Action]:
        """
        Lists all the Actions in the Model. This will only return the Actions listed under
        `Other Actions` in Anaplan. For Imports, exports, and processes, see their respective
        methods instead.
        :return: The List of Actions.
        """
        return [
            Action.model_validate(e)
            for e in (await self._get(f"{self._url}/actions")).get("actions", [])
        ]

    async def list_processes(self) -> list[Process]:
        """
        Lists all the Processes in the Model.
        :return: The List of Processes.
        """
        return [
            Process.model_validate(e)
            for e in (await self._get(f"{self._url}/processes")).get("processes", [])
        ]

    async def list_imports(self) -> list[Import]:
        """
        Lists all the Imports in the Model.
        :return: The List of Imports.
        """
        return [
            Import.model_validate(e)
            for e in (await self._get(f"{self._url}/imports")).get("imports", [])
        ]

    async def list_exports(self) -> list[Export]:
        """
        Lists all the Exports in the Model.
        :return: The List of Exports.
        """
        return [
            Export.model_validate(e)
            for e in (await self._get(f"{self._url}/exports")).get("exports", [])
        ]

    async def run_action(self, action_id: int) -> None:
        """
        Runs the specified Anaplan Action and validates the spawned task. If the Action fails or
        completes with errors, will raise an :py:class:`AnaplanActionError`. Failed Tasks are
        usually not something you can recover from at runtime and often require manual changes in
        Anaplan, i.e. updating the mapping of an Import or similar. So, for convenience, this will
        raise an Exception to handle - if you for e.g. think that one of the uploaded chunks may
        have been dropped and simply retrying with new data may help - and not return the task
        status information that needs to be handled by the caller.

        If you need more information or control, you can use `invoke_action()` and
        `get_task_status()`.
        :param action_id: The identifier of the Action to run. Can be any Anaplan Invokable;
                          Processes, Imports, Exports, Other Actions.
        """
        task_id = await self.invoke_action(action_id)
        task_status = await self.get_task_status(action_id, task_id)

        while "COMPLETE" not in task_status.get("taskState"):
            time.sleep(self.status_poll_delay)
            task_status = await self.get_task_status(action_id, task_id)

        if task_status.get("taskState") == "COMPLETE" and not task_status.get("result").get(
            "successful"
        ):
            raise AnaplanActionError(f"Task '{task_id}' completed with errors.")

        logger.info(f"Task '{task_id}' completed successfully.")

    async def get_file(self, file_id: int) -> bytes:
        """
        Retrieves the content of the specified file.
        :param file_id: The identifier of the file to retrieve.
        :return: The content of the file.
        """
        file = next(filter(lambda f: f.id == file_id, await self.list_files()), None)
        if not file:
            raise InvalidIdentifierException(f"File {file_id} not found.")
        chunk_count = file.chunk_count
        if chunk_count <= 1:
            return await self._get_binary(f"{self._url}/files/{file_id}")
        logger.info(f"File {file_id} has {chunk_count} chunks.")
        return b"".join(
            await gather(
                *[
                    self._get_binary(f"{self._url}/files/{file_id}/chunks/{i}")
                    for i in range(chunk_count)
                ]
            )
        )

    async def upload_file(self, file_id: int, content: str | bytes) -> None:
        """
        Uploads the content to the specified file. If there are several chunks, upload of
        individual chunks are concurrent.

        :param file_id: The identifier of the file to upload to.
        :param content: The content to upload. **This Content will be compressed before uploading.
                        If you are passing the Input as bytes, pass it uncompressed to avoid
                        redundant work.**
        """
        if isinstance(content, str):
            content = content.encode()
        chunks = [
            content[i : i + self.upload_chunk_size]
            for i in range(0, len(content), self.upload_chunk_size)
        ]
        logger.info(f"Content will be uploaded in {len(chunks)} chunks.")
        await self._set_chunk_count(file_id, len(chunks))
        await gather(
            *[self._upload_chunk(file_id, index, chunk) for index, chunk in enumerate(chunks)]
        )

    async def upload_and_import(self, file_id: int, content: str | bytes, action_id: int) -> None:
        """
        Convenience wrapper around `upload_file()` and `run_action()` to upload content to a file
        and run an import action in one call.
        :param file_id: The identifier of the file to upload to.
        :param content: The content to upload. **This Content will be compressed before uploading.
                        If you are passing the Input as bytes, pass it uncompressed to avoid
                        redundant work.**
        :param action_id: The identifier of the action to run after uploading the content.
        """
        await self.upload_file(file_id, content)
        await self.run_action(action_id)

    async def export_and_download(self, action_id: int) -> bytes:
        """
        Convenience wrapper around `run_action()` a     nd `get_file()` to run an export action and
        download the exported content in one call.
        :param action_id: The identifier of the action to run.
        :return: The content of the exported file.
        """
        await self.run_action(action_id)
        return await self.get_file(action_id)

    async def get_task_status(
        self, action_id: int, task_id: str
    ) -> dict[str, float | int | str | list | dict | bool]:
        """
        Retrieves the status of the specified task.
        :param action_id: The identifier of the action that was invoked.
        :param task_id: The identifier of the spawned task.
        :return: The status of the task as returned by the API. For more information
                 see: https://anaplan.docs.apiary.io.
        """
        return (
            await self._get(f"{self._url}/{action_url(action_id)}/{action_id}/tasks/{task_id}")
        ).get("task")

    async def invoke_action(self, action_id: int) -> str:
        """
        You may want to consider using `run_action()` instead.

        Invokes the specified Anaplan Action and returns the spawned Task identifier. This is
        useful if you want to handle the Task status yourself or if you want to run multiple
        Actions in parallel.
        :param action_id: The identifier of the Action to run. Can be any Anaplan Invokable.
        :return: The identifier of the spawned Task.
        """
        response = await self._post(
            f"{self._url}/{action_url(action_id)}/{action_id}/tasks", json={"localeName": "en_US"}
        )
        task_id = response.get("task").get("taskId")
        logger.info(f"Invoked Action '{action_id}', spawned Task: '{task_id}'.")
        return task_id

    async def _upload_chunk(self, file_id: int, index: int, chunk: bytes) -> None:
        await self._run_with_retry(
            self._put_binary_gzip, f"{self._url}/files/{file_id}/chunks/{index}", content=chunk
        )
        logger.info(f"Chunk {index} loaded to file '{file_id}'.")

    async def _set_chunk_count(self, file_id: int, num_chunks: int) -> None:
        if not self.allow_file_creation and not (113000000000 <= file_id <= 113999999999):
            raise InvalidIdentifierException(
                f"File with Id {file_id} does not exist. If you want to dynamically create files "
                "to avoid this error, set `allow_file_creation=True` on the calling instance. "
                "Make sure you have understood the implications of this before doing so. "
            )
        response = await self._post(f"{self._url}/files/{file_id}", json={"chunkCount": num_chunks})
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
