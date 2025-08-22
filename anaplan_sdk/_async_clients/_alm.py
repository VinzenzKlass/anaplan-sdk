import logging
from typing import Literal, overload

from anaplan_sdk._services import _AsyncHttpService, sort_params
from anaplan_sdk.exceptions import AnaplanActionError
from anaplan_sdk.models import (
    ModelRevision,
    ReportTask,
    Revision,
    SummaryReport,
    SyncTask,
    TaskSummary,
)

logger = logging.getLogger("anaplan_sdk")


class _AsyncAlmClient:
    def __init__(self, http: _AsyncHttpService, model_id: str) -> None:
        self._http = http
        self._model_id = model_id
        self._url = f"https://api.anaplan.com/2/0/models/{model_id}"

    async def change_model_status(self, status: Literal["online", "offline"]) -> None:
        """
        Use this call to change the status of a model.
        :param status: The status of the model. Can be either "online" or "offline".
        """
        logger.info(f"Changed model status to '{status}' for model {self._model_id}.")
        await self._http.put(f"{self._url}/onlineStatus", json={"status": status})

    async def get_revisions(
        self,
        sort_by: Literal["id", "name", "applied_on", "created_on"] = "applied_on",
        descending: bool = True,
    ) -> list[Revision]:
        """
        Use this call to return a list of revisions for a specific model. By default, the results
        are returned from the most recently created revision to the oldest revision.
        :param sort_by: The field to sort the results by.
        :param descending: If True, the results will be sorted in descending order.
        :return: A list of revisions for a specific model.
        """
        res = await self._http.get(
            f"{self._url}/alm/revisions", params=sort_params(sort_by, descending)
        )
        return [Revision.model_validate(e) for e in res.get("revisions", [])]

    async def get_latest_revision(self) -> Revision | None:
        """
        Use this call to return the latest revision for a specific model. The response is in the
        same format as in Getting a list of syncable revisions between two models.

        If a revision exists, the return list should contain one element only which is the
        latest revision.
        :return: The latest revision for a specific model, or None if no revisions exist.
        """
        res = (await self._http.get(f"{self._url}/alm/latestRevision")).get("revisions")
        return Revision.model_validate(res[0]) if res else None

    async def get_syncable_revisions(self, source_model_id: str) -> list[Revision]:
        """
        Use this call to return the list of revisions from your source model that can be
        synchronized to your target model.

        The returned list displays in descending order, by creation date and time. This is
        consistent with how revisions are displayed in the user interface (UI).
        :param source_model_id: The ID of the source model.
        :return: A list of revisions that can be synchronized to the target model.
        """
        res = await self._http.get(
            f"{self._url}/alm/syncableRevisions?sourceModelId={source_model_id}"
        )
        return [Revision.model_validate(e) for e in res.get("revisions", [])]

    async def create_revision(self, name: str, description: str) -> Revision:
        """
        Create a new revision for the model.
        :param name: The name (title) of the revision.
        :param description: The description of the revision.
        :return: The created Revision Info.
        """
        res = await self._http.post(
            f"{self._url}/alm/revisions", json={"name": name, "description": description}
        )
        rev = Revision.model_validate(res["revision"])
        logger.info(f"Created revision '{name} ({rev.id})'for model {self._model_id}.")
        return rev

    async def get_sync_tasks(self) -> list[TaskSummary]:
        """
        List the sync tasks for a target mode. The returned the tasks are either in progress, or
        they completed within the last 48 hours.
        :return: A list of sync tasks in descending order of creation time.
        """
        res = await self._http.get(f"{self._url}/alm/syncTasks")
        return [TaskSummary.model_validate(e) for e in res.get("tasks", [])]

    async def get_sync_task(self, task_id: str) -> SyncTask:
        """
        Get the information for a specific sync task.
        :param task_id: The ID of the sync task.
        :return: The sync task information.
        """
        res = await self._http.get(f"{self._url}/alm/syncTasks/{task_id}")
        return SyncTask.model_validate(res["task"])

    async def sync_models(
        self,
        source_revision_id: str,
        source_model_id: str,
        target_revision_id: str,
        wait_for_completion: bool = True,
    ) -> SyncTask:
        """
        Create a synchronization task between two revisions. This will synchronize the
        source revision of the source model to the target revision of the target model. This will
        fail if the source revision is incompatible with the target revision.
        :param source_revision_id: The ID of the source revision.
        :param source_model_id: The ID of the source model.
        :param target_revision_id: The ID of the target revision.
        :param wait_for_completion: If True, the method will poll the task status and not return
               until the task is complete. If False, it will spawn the task and return immediately.
        :return: The created sync task.
        """
        payload = {
            "sourceRevisionId": source_revision_id,
            "sourceModelId": source_model_id,
            "targetRevisionId": target_revision_id,
        }
        res = await self._http.post(f"{self._url}/alm/syncTasks", json=payload)
        task = await self.get_sync_task(res["task"]["taskId"])
        logger.info(
            f"Started sync task '{task.id}' from Model '{source_model_id}' "
            f"(Revision '{source_revision_id}') to Model '{self._model_id}'."
        )
        if not wait_for_completion:
            return task
        task = await self._http.poll_task(self.get_sync_task, task.id)
        if not task.result.successful:
            msg = f"Sync task {task.id} completed with errors: {task.result.error}."
            logger.error(msg)
            raise AnaplanActionError(msg)
        logger.info(f"Sync task {task.id} completed successfully.")
        return task

    async def get_models_for_revision(self, revision_id: str) -> list[ModelRevision]:
        """
        Use this call when you need a list of the models that had a specific revision applied
        to them.
        :param revision_id: The ID of the revision.
        :return: A list of models that had a specific revision applied to them.
        """
        res = await self._http.get(f"{self._url}/alm/revisions/{revision_id}/appliedToModels")
        return [ModelRevision.model_validate(e) for e in res.get("appliedToModels", [])]

    async def create_comparison_report(
        self,
        source_revision_id: str,
        source_model_id: str,
        target_revision_id: str,
        wait_for_completion: bool = True,
    ) -> ReportTask:
        """
        Generate a full comparison report between two revisions. This will list all the changes made
        to the source revision compared to the target revision.
        :param source_revision_id: The ID of the source revision.
        :param source_model_id: The ID of the source model.
        :param target_revision_id: The ID of the target revision.
        :param wait_for_completion: If True, the method will poll the task status and not return
               until the task is complete. If False, it will spawn the task and return immediately.
        :return: The created report task summary.
        """
        payload = {
            "sourceRevisionId": source_revision_id,
            "sourceModelId": source_model_id,
            "targetRevisionId": target_revision_id,
        }
        res = await self._http.post(f"{self._url}/alm/comparisonReportTasks", json=payload)
        task = await self.get_comparison_report_task(res["task"]["taskId"])
        logger.info(
            f"Started Comparison Report task '{task.id}' between Model '{source_model_id}' "
            f"(Revision '{source_revision_id}') and Model '{self._model_id}'."
        )
        if not wait_for_completion:
            return task
        task = await self._http.poll_task(self.get_comparison_report_task, task.id)
        if not task.result.successful:
            msg = f"Comparison Report task {task.id} completed with errors: {task.result.error}."
            logger.error(msg)
            raise AnaplanActionError(msg)
        logger.info(f"Comparison Report task {task.id} completed successfully.")
        return task

    async def get_comparison_report_task(self, task_id: str) -> ReportTask:
        """
        Get the task information for a comparison report task.
        :param task_id: The ID of the comparison report task.
        :return: The report task information.
        """
        res = await self._http.get(f"{self._url}/alm/comparisonReportTasks/{task_id}")
        return ReportTask.model_validate(res["task"])

    async def get_comparison_report(self, task: ReportTask) -> bytes:
        """
        Get the report for a specific task.
        :param task: The report task object containing the task ID.
        :return: The binary content of the comparison report.
        """
        return await self._http.get_binary(
            f"{self._url}/alm/comparisonReports/"
            f"{task.result.target_revision_id}/{task.result.source_revision_id}"
        )

    @overload
    async def create_comparison_summary(
        self,
        source_revision_id: str,
        source_model_id: str,
        target_revision_id: str,
        wait_for_completion: Literal[True] = True,
    ) -> SummaryReport: ...

    @overload
    async def create_comparison_summary(
        self,
        source_revision_id: str,
        source_model_id: str,
        target_revision_id: str,
        wait_for_completion: Literal[False] = False,
    ) -> ReportTask: ...

    async def create_comparison_summary(
        self,
        source_revision_id: str,
        source_model_id: str,
        target_revision_id: str,
        wait_for_completion: bool = True,
    ) -> ReportTask | SummaryReport:
        """
        Generate a comparison summary between two revisions.
        :param source_revision_id: The ID of the source revision.
        :param source_model_id: The ID of the source model.
        :param target_revision_id: The ID of the target revision.
        :param wait_for_completion: If True, the method will poll the task status and not return
               until the task is complete. If False, it will spawn the task and return immediately.
        :return: The created summary task or the summary report, if `wait_for_completion` is True.
        """
        payload = {
            "sourceRevisionId": source_revision_id,
            "sourceModelId": source_model_id,
            "targetRevisionId": target_revision_id,
        }
        res = await self._http.post(f"{self._url}/alm/summaryReportTasks", json=payload)
        task = await self.get_comparison_summary_task(res["task"]["taskId"])
        logger.info(
            f"Started Comparison Summary task '{task.id}' between Model '{source_model_id}' "
            f"(Revision '{source_revision_id}') and Model '{self._model_id}'."
        )
        if not wait_for_completion:
            return task
        task = await self._http.poll_task(self.get_comparison_summary_task, task.id)
        if not task.result.successful:
            msg = f"Comparison Summary task {task.id} completed with errors: {task.result.error}."
            logger.error(msg)
            raise AnaplanActionError(msg)
        logger.info(f"Comparison Summary task {task.id} completed successfully.")
        return await self.get_comparison_summary(task)

    async def get_comparison_summary_task(self, task_id: str) -> ReportTask:
        """
        Get the task information for a comparison summary task.
        :param task_id: The ID of the comparison summary task.
        :return: The report task information.
        """
        res = await self._http.get(f"{self._url}/alm/summaryReportTasks/{task_id}")
        return ReportTask.model_validate(res["task"])

    async def get_comparison_summary(self, task: ReportTask) -> SummaryReport:
        """
        Get the comparison summary for a specific task.
        :param task: The summary task object containing the task ID.
        :return: The binary content of the comparison summary.
        """
        res = await self._http.get(
            f"{self._url}/alm/summaryReports/"
            f"{task.result.target_revision_id}/{task.result.source_revision_id}"
        )
        return SummaryReport.model_validate(res["summaryReport"])
