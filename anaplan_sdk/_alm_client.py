import httpx

from ._base import _BaseClient
from .models import Revision, SyncTask


class _AlmClient(_BaseClient):
    def __init__(self, client: httpx.Client, model_id: str, retry_count: int) -> None:
        self._client = client
        self._url = f"https://api.anaplan.com/2/0/models/{model_id}/alm"
        super().__init__(retry_count, client)

    def get_syncable_revisions(self, source_model_id: str) -> list[Revision]:
        return [
            Revision.model_validate(e)
            for e in self._get(
                f"{self._url}/syncableRevisions?sourceModelId={source_model_id}"
            ).get("revisions", [])
        ]

    def get_latest_revision(self) -> list[Revision]:
        return [
            Revision.model_validate(e)
            for e in self._get(f"{self._url}/latestRevision").get("revisions", [])
        ]

    def get_sync_tasks(self) -> list[SyncTask]:
        return [
            SyncTask.model_validate(e) for e in self._get(f"{self._url}/syncTasks").get("tasks", [])
        ]
