import httpx

from ._base import _BaseClient
from ._models import ModelStatus


class _TransactionalClient(_BaseClient):
    def __init__(self, client: httpx.Client, model_id: str, timeout: int, retry_count: int) -> None:
        self._client = client
        self.model_id = model_id
        self.timeout = timeout
        super().__init__(retry_count)

    def list_views(self) -> list:
        return []

    def get_model_status(self) -> ModelStatus:
        return ModelStatus()

    def _get(self, url: str) -> dict[str, float | int | str | list | dict | bool]:
        return self._run_with_retry(self._client.get, url, timeout=self.timeout).json()
