from time import sleep
from typing import Literal

import httpx

from anaplan_sdk._base import _BaseClient
from anaplan_sdk.models import ModelRevision, ReportTask, Revision, SyncTask, TaskSummary
from anaplan_sdk.models._alm import SummaryReport


class _AlmClient(_BaseClient):
    def __init__(
        self, client: httpx.Client, model_id: str, retry_count: int, status_poll_delay: int
    ) -> None:
        self.status_poll_delay = status_poll_delay
        self._url = f"https://api.anaplan.com/2/0/models/{model_id}"
        super().__init__(retry_count, client)

    def change_model_status(self, status: Literal["online", "offline"]) -> None:
        """
        Use this call to change the status of a model.
        :param status: The status of the model. Can be either "online" or "offline".
        """
        self._put(f"{self._url}/onlineStatus", json={"status": status})

    def list_revisions(self) -> list[Revision]:
        """
        Use this call to return a list of revisions for a specific model.
        :return: A list of revisions for a specific model.
        """
        res = self._get(f"{self._url}/alm/revisions")
        return [Revision.model_validate(e) for e in res.get("revisions", [])]

    def get_latest_revision(self) -> Revision | None:
        """
        Use this call to return the latest revision for a specific model. The response is in the
        same format as in Getting a list of syncable revisions between two models.

        If a revision exists, the return list should contain one element only which is the
        latest revision.
        :return: The latest revision for a specific model, or None if no revisions exist.
        """
        res = (self._get(f"{self._url}/alm/latestRevision")).get("revisions")
        return Revision.model_validate(res[0]) if res else None

    def list_syncable_revisions(self, source_model_id: str) -> list[Revision]:
        """
        Use this call to return the list of revisions from your source model that can be
        synchronized to your target model.

        The returned list displays in descending order, by creation date and time. This is
        consistent with how revisions are displayed in the user interface (UI).
        :param source_model_id: The ID of the source model.
        :return: A list of revisions that can be synchronized to the target model.
        """
        res = self._get(f"{self._url}/alm/syncableRevisions?sourceModelId={source_model_id}")
        return [Revision.model_validate(e) for e in res.get("revisions", [])]

    def create_revision(self, name: str, description: str) -> Revision:
        """
        Create a new revision for the model.
        :param name: The name (title) of the revision.
        :param description: The description of the revision.
        :return: The created Revision Info.
        """
        res = self._post(
            f"{self._url}/alm/revisions", json={"name": name, "description": description}
        )
        return Revision.model_validate(res["revision"])

    def list_sync_tasks(self) -> list[TaskSummary]:
        """
        List the sync tasks for a target mode. The returned the tasks are either in progress, or
        they completed within the last 48 hours.
        :return: A list of sync tasks in descending order of creation time.
        """
        res = self._get(f"{self._url}/alm/syncTasks")
        return [TaskSummary.model_validate(e) for e in res.get("tasks", [])]

    def get_sync_task(self, task_id: str) -> SyncTask:
        """
        Get the information for a specific sync task.
        :param task_id: The ID of the sync task.
        :return: The sync task information.
        """
        res = self._get(f"{self._url}/alm/syncTasks/{task_id}")
        return SyncTask.model_validate(res["task"])

    def sync_models(
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
        res = self._post(f"{self._url}/alm/syncTasks", json=payload)
        sync_task = self.get_sync_task(res["task"]["taskId"])
        if not wait_for_completion:
            return sync_task
        while (sync_task := self.get_sync_task(sync_task.id)).task_state != "COMPLETE":
            sleep(self.status_poll_delay)
        return sync_task

    def list_models_for_revision(self, revision_id: str) -> list[ModelRevision]:
        """
        Use this call when you need a list of the models that had a specific revision applied
        to them.
        :param revision_id: The ID of the revision.
        :return: A list of models that had a specific revision applied to them.
        """
        res = self._get(f"{self._url}/alm/revisions/{revision_id}/appliedToModels")
        return [ModelRevision.model_validate(e) for e in res.get("appliedToModels", [])]

    def create_comparison_report(
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
        res = self._post(f"{self._url}/alm/comparisonReportTasks", json=payload)
        task = self.get_comparison_report_task(res["task"]["taskId"])
        if not wait_for_completion:
            return task
        while (task := self.get_comparison_report_task(task.id)).task_state != "COMPLETE":
            sleep(self.status_poll_delay)
        return task

    def get_comparison_report_task(self, task_id: str) -> ReportTask:
        """
        Get the task information for a comparison report task.
        :param task_id: The ID of the comparison report task.
        :return: The report task information.
        """
        res = self._get(f"{self._url}/alm/comparisonReportTasks/{task_id}")
        return ReportTask.model_validate(res["task"])

    def get_comparison_report(self, task: ReportTask) -> bytes:
        """
        Get the report for a specific task.
        :param task: The report task object containing the task ID.
        :return: The binary content of the comparison report.
        """
        return self._get_binary(
            f"{self._url}/alm/comparisonReports/"
            f"{task.result.target_revision_id}/{task.result.source_revision_id}"
        )

    def create_comparison_summary(
        self,
        source_revision_id: str,
        source_model_id: str,
        target_revision_id: str,
        wait_for_completion: bool = True,
    ) -> ReportTask:
        """
        Generate a comparison summary between two revisions.
        :param source_revision_id: The ID of the source revision.
        :param source_model_id: The ID of the source model.
        :param target_revision_id: The ID of the target revision.
        :param wait_for_completion: If True, the method will poll the task status and not return
               until the task is complete. If False, it will spawn the task and return immediately.
        :return: The created summary task.
        """
        payload = {
            "sourceRevisionId": source_revision_id,
            "sourceModelId": source_model_id,
            "targetRevisionId": target_revision_id,
        }
        res = self._post(f"{self._url}/alm/summaryReportTasks", json=payload)
        task = self.get_comparison_summary_task(res["task"]["taskId"])
        if not wait_for_completion:
            return task
        while (task := self.get_comparison_summary_task(task.id)).task_state != "COMPLETE":
            sleep(self.status_poll_delay)
        return task

    def get_comparison_summary_task(self, task_id: str) -> ReportTask:
        """
        Get the task information for a comparison summary task.
        :param task_id: The ID of the comparison summary task.
        :return: The report task information.
        """
        res = self._get(f"{self._url}/alm/summaryReportTasks/{task_id}")
        return ReportTask.model_validate(res["task"])

    def get_comparison_summary(self, task: ReportTask) -> SummaryReport:
        """
        Get the comparison summary for a specific task.
        :param task: The summary task object containing the task ID.
        :return: The binary content of the comparison summary.
        """
        res = self._get(
            f"{self._url}/alm/summaryReports/"
            f"{task.result.target_revision_id}/{task.result.source_revision_id}"
        )
        return SummaryReport.model_validate(res)
