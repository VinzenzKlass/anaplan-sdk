from anaplan_sdk import AsyncClient
from anaplan_sdk.models import ModelRevision, Revision, SyncTaskSummary


async def test_set_model_status(client: AsyncClient):
    await client.alm.change_model_status("online")


async def test_get_syncable_revisions(client: AsyncClient):
    revisions = await client.alm.list_syncable_revisions("327F80BA66344A1C84C69AE82C006CDE")
    assert isinstance(revisions, list)
    assert all(isinstance(rev, Revision) for rev in revisions)


async def test_get_latest_revision(client: AsyncClient):
    rev = await client.alm.get_latest_revision()
    assert isinstance(rev, Revision)


async def test_list_revisions(client: AsyncClient):
    revisions = await client.alm.list_revisions()
    assert isinstance(revisions, list)
    assert all(isinstance(rev, Revision) for rev in revisions)


async def test_list_models_for_revision(client: AsyncClient):
    model_revs = await client.alm.list_models_for_revision("44867AAA4DD94C6EB8A23690A0C11DF4")
    assert isinstance(model_revs, list)
    assert all(isinstance(rev, ModelRevision) for rev in model_revs)


async def test_list_sync_tasks(client: AsyncClient):
    tasks = await client.alm.list_sync_tasks()
    assert isinstance(tasks, list)
    assert all(isinstance(task, SyncTaskSummary) for task in tasks)
