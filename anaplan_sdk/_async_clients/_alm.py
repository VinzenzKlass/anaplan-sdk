import httpx

from anaplan_sdk._base import _AsyncBaseClient
from anaplan_sdk.models import Revision, SyncTask


class _AsyncAlmClient(_AsyncBaseClient):
    def __init__(self, client: httpx.AsyncClient, model_id: str, retry_count: int) -> None:
        self._client = client
        self._url = f"https://api.anaplan.com/2/0/models/{model_id}/alm"
        super().__init__(retry_count, client)

    async def get_syncable_revisions(self, source_model_id: str) -> list[Revision]:
        revs = (
            await self._get(f"{self._url}/syncableRevisions?sourceModelId={source_model_id}")
        ).get("revisions", [])
        return [Revision.model_validate(e) for e in revs] if revs else []

    async def get_latest_revision(self) -> list[Revision]:
        return [
            Revision.model_validate(e)
            for e in (await self._get(f"{self._url}/latestRevision")).get("revisions", [])
        ]

    async def get_sync_tasks(self) -> list[SyncTask]:
        return [
            SyncTask.model_validate(e)
            for e in (await self._get(f"{self._url}/syncTasks")).get("tasks", [])
        ]
