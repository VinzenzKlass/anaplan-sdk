import httpx

from ._base import _BaseClient
from ._models import ModelStatus


class _TransactionalClient(_BaseClient):
    def __init__(self, client: httpx.Client, model_id: str, retry_count: int) -> None:
        self._client = client
        self.model_id = model_id
        super().__init__(retry_count, client)

    def list_views(self) -> list:
        return []

    def get_model_status(self) -> ModelStatus:
        return ModelStatus()
