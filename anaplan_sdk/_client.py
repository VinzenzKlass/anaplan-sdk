import base64
import gzip
import logging
import os
import time
from concurrent.futures import ThreadPoolExecutor

import httpx
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from httpx import HTTPStatusError, HTTPError
from tenacity import retry, retry_if_exception_type, stop_after_attempt

from ._exceptions import (
    InvalidCredentialsException,
    InvalidIdentifierException,
    AnaplanActionError,
    ReAuthException,
)
from ._types import Import, Export, Process, File, Action, List, Workspace, Model

logger = logging.getLogger("anaplan_sdk")


class Client:
    """
    A synchronous Client for pythonic access to the Anaplan Integration API v2:
    https://anaplan.docs.apiary.io/. This Client provides high-level abstractions over the API, so
    you can deal with python objects and simple functions rather than implementation details like
    http, json, compression, chunking etc.


    For more information, quick start guides and detailed instructions refer to:
    https://vinzenzklass.github.io/anaplan-sdk.
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
        timeout: int = 30,
        status_poll_delay: int = 1,
        upload_parallel: bool = True,
        upload_chunk_size: int = 25_000_000,
    ) -> None:
        """
        A synchronous Client for pythonic access to the Anaplan Integration API v2:
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
        :param timeout: The timeout for the HTTP requests.
        :param status_poll_delay: The delay between polling the status of a task.
        :param upload_parallel: Whether to upload the chunks in parallel. Defaults to True. **If
                                you are heavily network bound or are experiencing rate limiting
                                issues, set this to False.**
        :param upload_chunk_size: The size of the chunks to upload. This is the maximum size of
                                  each chunk. Defaults to 25MB.
        """
        if not ((user_email and password) or (certificate and private_key)):
            raise ValueError(
                "Either `certificate` and `private_key` or `user_email` and `password` must be "
                "provided."
            )
        self._client = httpx.Client()
        self._auth_url = "https://auth.anaplan.com/token/authenticate"
        self._base_url = "https://api.anaplan.com/2/0/workspaces"
        self.workspace_id = workspace_id
        self.model_id = model_id
        self.user_email = user_email
        self.password = password
        self.certificate = certificate
        self.private_key = private_key
        self.private_key_password = private_key_password
        self.timeout = timeout
        self.status_poll_delay = status_poll_delay
        self.upload_parallel = upload_parallel
        self.upload_chunk_size = upload_chunk_size
        try:
            self._auth_token = self._cert_auth() if certificate else self._basic_auth()
        except HTTPStatusError as error:
            if error.response.status_code == 401:
                raise InvalidCredentialsException from error
            raise error

    def list_workspaces(self) -> list[Workspace]:
        """
        Lists all the Workspaces the authenticated user has access to.
        :return: All Workspaces as a list of :py:class:`Workspace`.
        """
        response = self._get(f"{self._base_url}?tenantDetails=true")
        return [
            Workspace(
                id=e.get("id"),
                name=e.get("name"),
                active=e.get("active"),
                size_allowance=int(e.get("sizeAllowance")),
                current_size=int(e.get("currentSize")),
            )
            for e in response.get("workspaces")
        ]

    def list_models(self) -> list[Model]:
        """
        Lists all the Models the authenticated user has access to.
        :return: All Models in the Workspace as a list of :py:class:`Model`.
        """
        response = self._get(
            f"{self._base_url.replace('/workspaces', '/models')}?modelDetails=true"
        )
        return [
            Model(
                id=e.get("id"),
                name=e.get("name"),
                active_state=e.get("activeState"),
                last_saved_serial_number=int(e.get("lastSavedSerialNumber")),
                last_modified_by_user_guid=e.get("lastModifiedByUserGuid"),
                memory_usage=int(e.get("memoryUsage", 0)),
                current_workspace_id=e.get("currentWorkspaceId"),
                current_workspace_name=e.get("currentWorkspaceName"),
                model_url=e.get("modelUrl"),
                category_values=e.get("categoryValues"),
                iso_creation_date=e.get("isoCreationDate"),
                last_modified=e.get("lastModified"),
            )
            for e in response.get("models")
        ]

    def list_actions(self) -> list[Action]:
        """
        Lists all the Actions in the Model. This will only return the Actions listed under
        `Other Actions` in Anaplan. For Imports, exports, and processes, see their respective
        methods instead.

        :return: All Actions on this model as a list of :py:class:`Action`.
        """
        response = self._get(f"{self._base_url}/{self.workspace_id}/models/{self.model_id}/actions")
        return [
            Action(id=int(e.get("id")), name=e.get("name"), type=e.get("actionType"))
            for e in response.get("actions")
        ]

    def list_imports(self) -> list[Import]:
        """
        Lists all the Imports in the Model.
        :return: All Imports on this model as a list of :py:class:`Import`.
        """
        response = self._get(f"{self._base_url}/{self.workspace_id}/models/{self.model_id}/imports")
        return [
            Import(
                id=int(e.get("id")),
                type=e.get("importType"),
                name=e.get("name"),
                source_id=int(e.get("importDataSourceId")) if e.get("importDataSourceId") else None,
            )
            for e in response.get("imports")
        ]

    def list_exports(self) -> list[Export]:
        """
        Lists all the Exports in the Model.
        :return: All Exports on this model as a list of :py:class:`Export`.
        """
        response = self._get(f"{self._base_url}/{self.workspace_id}/models/{self.model_id}/exports")
        return [
            Export(
                id=int(e.get("id")),
                name=e.get("name"),
                type=e.get("exportType"),
                format=e.get("exportFormat"),
                encoding=e.get("encoding"),
                layout=e.get("layout"),
            )
            for e in response.get("exports")
        ]

    def list_processes(self) -> list[Process]:
        """
        Lists all the Processes in the Model.
        :return: All Processes on this model as a list of :py:class:`Process`.
        """
        response = self._get(
            f"{self._base_url}/{self.workspace_id}/models/{self.model_id}/processes"
        )
        return [Process(id=int(e.get("id")), name=e.get("name")) for e in response.get("processes")]

    def list_files(self) -> list[File]:
        """
        Lists all the Files in the Model.
        :return: All Files on this model as a list of :py:class:`File`.
        """
        response = self._get(f"{self._base_url}/{self.workspace_id}/models/{self.model_id}/files")
        return [
            File(
                id=int(e.get("id")),
                name=e.get("name"),
                chunk_count=e.get("chunkCount"),
                delimiter=e.get("delimiter"),
                encoding=e.get("encoding"),
                first_data_row=e.get("firstDataRow"),
                format=e.get("format"),
                header_row=e.get("headerRow"),
                separator=e.get("separator"),
            )
            for e in response.get("files")
        ]

    def list_lists(self) -> list[List]:
        """
        Lists all the Lists in the Model.
        :return: All Lists on this model as a list of :py:class:`List`.
        """
        response = self._get(f"{self._base_url}/{self.workspace_id}/models/{self.model_id}/lists")
        return [List(id=int(e.get("id")), name=e.get("name")) for e in response.get("lists")]

    def run_action(self, action_id: int) -> None:
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
        task_id = self.invoke_action(action_id)
        task_status = self.get_task_status(action_id, task_id)

        while "COMPLETE" not in task_status.get("taskState"):
            time.sleep(self.status_poll_delay)
            task_status = self.get_task_status(action_id, task_id)

        if task_status.get("taskState") == "COMPLETE" and not task_status.get("result").get(
            "successful"
        ):
            raise AnaplanActionError(f"Task '{task_id}' completed with errors.")

    def get_file(self, file_id: int) -> bytes:
        """
        Retrieves the content of the specified file.
        :param file_id: The identifier of the file to retrieve.
        :return: The content of the file.
        """
        return self._get_binary(
            f"{self._base_url}/{self.workspace_id}/models/{self.model_id}/files/{file_id}"
        )

    def upload_file(self, file_id: int, content: str | bytes) -> None:
        """
        Uploads the content to the specified file. If `upload_parallel` is set to True on the
        instance you are invoking this from, will attempt to upload the chunks in parallel for
        better performance. If you are network bound or are experiencing rate limiting issues, set
        `upload_parallel` to False.

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
        self._set_chunk_count(file_id, len(chunks))
        if self.upload_parallel:
            with ThreadPoolExecutor(max_workers=4) as executor:
                executor.map(
                    self._upload_chunk, (file_id,) * len(chunks), range(len(chunks)), chunks
                )
        else:
            for index, chunk in enumerate(chunks):
                self._upload_chunk(file_id, index, chunk)
        logger.info(f"Content loaded to  File '{file_id}'.")

    def get_task_status(
        self, action_id: int, task_id: str
    ) -> dict[str, float | int | str | list | dict | bool]:
        """
        Retrieves the status of the specified task.
        :param action_id: The identifier of the action that was invoked.
        :param task_id: The identifier of the spawned task.
        :return: The status of the task as returned by the API. For more information
                 see: https://anaplan.docs.apiary.io.
        """
        return self._get(
            f"{self._base_url}/{self.workspace_id}/models/{self.model_id}/"
            f"{self._determine_action_type(action_id)}/{action_id}/tasks/{task_id}"
        ).get("task")

    def invoke_action(self, action_id: int) -> str:
        """
        You may want to consider using `run_action()` instead.

        Invokes the specified Anaplan Action and returns the spawned Task identifier. This is
        useful if you want to handle the Task status yourself or if you want to run multiple
        Actions in parallel.
        :param action_id:
        :return:
        """
        response = self._post(
            f"{self._base_url}/{self.workspace_id}/models/{self.model_id}/"
            f"{self._determine_action_type(action_id)}/{action_id}/tasks",
            json={"localeName": "en_US"},
        )
        task_id = response.get("task").get("taskId")
        logger.info(f"Invoked Action '{action_id}', spawned Task: '{task_id}'.")
        return task_id

    @retry(retry=retry_if_exception_type(ReAuthException), stop=stop_after_attempt(2))
    def _upload_chunk(self, file_id: int, index: int, chunk: bytes) -> None:
        try:
            response = self._client.put(
                f"{self._base_url}/{self.workspace_id}/models/{self.model_id}/files/{file_id}/"
                f"chunks/{index}",
                headers={
                    "Authorization": f"AnaplanAuthToken {self._auth_token}",
                    "Content-Type": "application/x-gzip",
                },
                content=gzip.compress(chunk),
                timeout=self.timeout,
            )
            response.raise_for_status()
        except HTTPError as error:
            self._recover_or_raise(error)

    def _set_chunk_count(self, file_id: int, num_chunks: int) -> None:
        self._post(
            f"{self._base_url}/{self.workspace_id}/models/{self.model_id}/files/{file_id}",
            json={"chunkCount": num_chunks},
        )

    def _basic_auth(self) -> str:
        credentials = base64.b64encode(f"{self.user_email}:{self.password}".encode()).decode()
        response = self._client.post(
            self._auth_url, headers={"Authorization": f"Basic {credentials}"}, timeout=self.timeout
        )
        response.raise_for_status()
        logger.info("Authentication Token created.")
        return response.json().get("tokenInfo").get("tokenValue")

    def _cert_auth(self) -> str:
        message = os.urandom(150)
        encoded_cert = base64.b64encode(self._get_certificate()).decode()
        encoded_string = base64.b64encode(message).decode()
        encoded_signed_string = base64.b64encode(
            self._get_private_key().sign(message, padding.PKCS1v15(), hashes.SHA512())
        ).decode()
        payload = {"encodedData": encoded_string, "encodedSignedData": encoded_signed_string}
        response = self._client.post(
            self._auth_url,
            headers={
                "Authorization": f"CACertificate {encoded_cert}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        logger.info("Authentication Token created.")
        return response.json().get("tokenInfo").get("tokenValue")

    @retry(retry=retry_if_exception_type(ReAuthException), stop=stop_after_attempt(2))
    def _get(self, url: str) -> dict[str, float | int | str | list | dict | bool]:
        try:
            response = self._client.get(
                url,
                headers={"Authorization": f"AnaplanAuthToken {self._auth_token}"},
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.json()
        except HTTPError as error:
            self._recover_or_raise(error)

    @retry(retry=retry_if_exception_type(ReAuthException), stop=stop_after_attempt(2))
    def _get_binary(self, url: str) -> bytes:
        try:
            response = self._client.get(
                url,
                headers={"Authorization": f"AnaplanAuthToken {self._auth_token}"},
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.content
        except HTTPError as error:
            self._recover_or_raise(error)

    @retry(retry=retry_if_exception_type(ReAuthException), stop=stop_after_attempt(2))
    def _post(
        self, url: str, json: dict | None = None
    ) -> dict[str, float | int | str | list | dict | bool]:
        try:
            return self._client.post(
                url,
                headers={
                    "Authorization": f"AnaplanAuthToken {self._auth_token}",
                    "Content-Type": "application/json",
                },
                json=json,
                timeout=self.timeout,
            ).json()
        except HTTPError as error:
            self._recover_or_raise(error)

    def _recover_or_raise(self, error: HTTPError) -> None:
        if isinstance(error, HTTPStatusError):
            if error.response.status_code == 401:
                self._auth_token = self._auth_token = (
                    self._cert_auth() if self.certificate else self._basic_auth()
                )
                raise ReAuthException from error
            if error.response.status_code == 404:
                raise InvalidIdentifierException from error

    def _get_certificate(self) -> bytes:
        if isinstance(self.certificate, str):
            if os.path.isfile(self.certificate):
                with open(self.certificate, "rb") as f:
                    return f.read()
            return self.certificate.encode()
        return self.certificate

    def _get_private_key(self) -> RSAPrivateKey:
        if isinstance(self.private_key, str):
            if os.path.isfile(self.certificate):
                with open(self.private_key, "rb") as f:
                    data = f.read()
            else:
                data = self.private_key.encode()
        else:
            data = self.private_key

        password = None
        if self.private_key_password:
            if isinstance(self.private_key_password, str):
                password = self.private_key_password.encode()
            else:
                password = self.private_key_password
        return serialization.load_pem_private_key(data, password, backend=default_backend())

    @staticmethod
    def _determine_action_type(action_id: int) -> str:
        if 12000000000 <= action_id < 113000000000:
            return "imports"
        if 116000000000 <= action_id < 117000000000:
            return "exports"
        if 117000000000 <= action_id < 118000000000:
            return "actions"
        if 118000000000 <= action_id < 119000000000:
            return "processes"
        raise InvalidIdentifierException(f"'{action_id}' is not a valid identifier.")
