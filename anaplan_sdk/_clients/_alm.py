import warnings

import httpx

from anaplan_sdk._base import _BaseClient
from anaplan_sdk.models import ModelRevision, Revision, SyncTask, User

warnings.filterwarnings("always", category=DeprecationWarning)


class _AlmClient(_BaseClient):
    def __init__(self, client: httpx.Client, model_id: str, retry_count: int) -> None:
        self._url = f"https://api.anaplan.com/2/0/models/{model_id}/alm"
        super().__init__(retry_count, client)

    def list_users(self) -> list[User]:
        """
        Lists all the Users in the authenticated users default tenant.
        :return: The List of Users.
        """
        warnings.warn(
            "`list_users()` on the ALM client is deprecated and will be removed in a "
            "future version. Use `list_users()` on the Audit client instead.",
            DeprecationWarning,
            stacklevel=1,
        )
        return [
            User.model_validate(e)
            for e in self._get("https://api.anaplan.com/2/0/users").get("users")
        ]

    def get_syncable_revisions(self, source_model_id: str) -> list[Revision]:
        """
        Use this call to return the list of revisions from your source model that can be
        synchronized to your target model.

        The returned list displays in descending order, by creation date and time. This is
        consistent with how revisions are displayed in the user interface (UI).
        :param source_model_id: The ID of the source model.
        :return: A list of revisions that can be synchronized to the target model.
        """
        return [
            Revision.model_validate(e)
            for e in self._get(
                f"{self._url}/syncableRevisions?sourceModelId={source_model_id}"
            ).get("revisions", [])
        ]

    def get_latest_revision(self) -> list[Revision]:
        """
        Use this call to return the latest revision for a specific model. The response is in the
        same format as in Getting a list of syncable revisions between two models.

        If a revision exists, the return list should contain one element only which is the
        latest revision.
        :return: The latest revision for a specific model.
        """
        return [
            Revision.model_validate(e)
            for e in self._get(f"{self._url}/latestRevision").get("revisions", [])
        ]

    def get_sync_tasks(self) -> list[SyncTask]:
        """
        Use this endpoint to return a list of sync tasks for a target model, where the tasks are
        either in progress, or they were completed within the last 48 hours.

        The list is in descending order of when the tasks were created.
        :return: A list of sync tasks for a target model.
        """
        return [
            SyncTask.model_validate(e) for e in self._get(f"{self._url}/syncTasks").get("tasks", [])
        ]

    def get_revisions(self) -> list[Revision]:
        """
        Use this call to return a list of revisions for a specific model.
        :return: A list of revisions for a specific model.
        """
        return [
            Revision.model_validate(e)
            for e in self._get(f"{self._url}/revisions").get("revisions", [])
        ]

    def get_models_for_revision(self, revision_id: str) -> list[ModelRevision]:
        """
        Use this call when you need a list of the models that had a specific revision applied
        to them.
        :param revision_id: The ID of the revision.
        :return: A list of models that had a specific revision applied to them.
        """
        return [
            ModelRevision.model_validate(e)
            for e in self._get(f"{self._url}/revisions/{revision_id}/appliedToModels").get(
                "appliedToModels", []
            )
        ]
