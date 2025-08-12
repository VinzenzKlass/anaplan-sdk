from typing import Literal

import httpx

from anaplan_sdk._base import _AsyncBaseClient
from anaplan_sdk.models import ModelRevision, ReportTask, Revision, SyncTask, TaskSummary


class _AsyncAlmClient(_AsyncBaseClient):
    def __init__(self, client: httpx.AsyncClient, model_id: str, retry_count: int) -> None:
        self._url = f"https://api.anaplan.com/2/0/models/{model_id}"
        super().__init__(retry_count, client)

    async def change_model_status(self, status: Literal["online", "offline"]) -> None:
        """
        Use this call to change the status of a model.
        :param status: The status of the model. Can be either "online" or "offline".
        """
        await self._put(f"{self._url}/onlineStatus", json={"status": status})

    async def list_revisions(self) -> list[Revision]:
        """
        Use this call to return a list of revisions for a specific model.
        :return: A list of revisions for a specific model.
        """
        res = await self._get(f"{self._url}/alm/revisions")
        return [Revision.model_validate(e) for e in res.get("revisions", [])]

    async def get_latest_revision(self) -> Revision | None:
        """
        Use this call to return the latest revision for a specific model. The response is in the
        same format as in Getting a list of syncable revisions between two models.

        If a revision exists, the return list should contain one element only which is the
        latest revision.
        :return: The latest revision for a specific model, or None if no revisions exist.
        """
        res = (await self._get(f"{self._url}/alm/latestRevision")).get("revisions")
        return Revision.model_validate(res[0]) if res else None

    async def list_syncable_revisions(self, source_model_id: str) -> list[Revision]:
        """
        Use this call to return the list of revisions from your source model that can be
        synchronized to your target model.

        The returned list displays in descending order, by creation date and time. This is
        consistent with how revisions are displayed in the user interface (UI).
        :param source_model_id: The ID of the source model.
        :return: A list of revisions that can be synchronized to the target model.
        """
        res = await self._get(f"{self._url}/alm/syncableRevisions?sourceModelId={source_model_id}")
        return [Revision.model_validate(e) for e in res.get("revisions", [])]

    async def create_revision(self, name: str, description: str) -> Revision:
        res = await self._post(
            f"{self._url}/alm/revisions", json={"name": name, "description": description}
        )
        return Revision.model_validate(res["revision"])

    async def list_sync_tasks(self) -> list[TaskSummary]:
        """
        List the sync tasks for a target mode. The returned the tasks are either in progress, or
        they completed within the last 48 hours.
        :return: A list of sync tasks in descending order of creation time.
        """
        res = await self._get(f"{self._url}/alm/syncTasks")
        return [TaskSummary.model_validate(e) for e in res.get("tasks", [])]

    async def get_sync_task(self, task_id: str) -> SyncTask:
        res = await self._get(f"{self._url}/alm/syncTasks/{task_id}")
        return SyncTask.model_validate(res["task"])

    async def create_sync_task(
        self, source_revision_id: str, source_model_id: str, target_revision_id: str
    ) -> TaskSummary:
        payload = {
            "sourceRevisionId": source_revision_id,
            "sourceModelId": source_model_id,
            "targetRevisionId": target_revision_id,
        }
        res = await self._post(f"{self._url}/alm/syncTasks", json=payload)
        return TaskSummary.model_validate(res["task"])

    async def list_models_for_revision(self, revision_id: str) -> list[ModelRevision]:
        """
        Use this call when you need a list of the models that had a specific revision applied
        to them.
        :param revision_id: The ID of the revision.
        :return: A list of models that had a specific revision applied to them.
        """
        res = await self._get(f"{self._url}/alm/revisions/{revision_id}/appliedToModels")
        return [ModelRevision.model_validate(e) for e in res.get("appliedToModels", [])]

    async def create_comparison_report(
        self, source_revision_id: str, source_model_id: str, target_revision_id: str
    ) -> TaskSummary:
        """
        Generate a full comparison report between two revisions. This will list all the changes made
        to the source revision compared to the target revision.
        :param source_revision_id: The ID of the source revision.
        :param source_model_id: The ID of the source model.
        :param target_revision_id: The ID of the target revision.
        :return: The created report task summary.
        """
        payload = {
            "sourceRevisionId": source_revision_id,
            "sourceModelId": source_model_id,
            "targetRevisionId": target_revision_id,
        }
        res = await self._post(f"{self._url}/alm/comparisonReportTasks", json=payload)
        return TaskSummary.model_validate(res["task"])

    async def get_comparison_report_task_info(self, task_id: str) -> ReportTask:
        """
        Get the task information for a comparison report task.
        :param task_id: The ID of the comparison report task.
        :return: The report task information.
        """
        res = await self._get(f"{self._url}/alm/comparisonReportTasks/{task_id}")
        return ReportTask.model_validate(res["task"])

    async def get_comparison_report(self, task: ReportTask) -> bytes:
        """
        Get the report for a specific task.
        :param task: The report task object containing the task ID.
        :return: The binary content of the comparison report.
        """
        return await self._get_binary(
            f"{self._url}/alm/comparisonReports/"
            f"{task.result.target_revision_id}/{task.result.source_revision_id}"
        )
