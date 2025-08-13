from asyncio import gather
from datetime import datetime
from uuid import uuid4

from anaplan_sdk import AsyncClient
from anaplan_sdk.models import ModelRevision, Revision, SyncTask, TaskSummary


async def test_change_model_status(client: AsyncClient):
    await client.alm.change_model_status("online")


async def test_list_revisions(client: AsyncClient):
    revisions = await client.alm.list_revisions()
    assert isinstance(revisions, list)
    assert all(isinstance(rev, Revision) for rev in revisions)


async def test_get_latest_revision(client: AsyncClient):
    rev = await client.alm.get_latest_revision()
    assert isinstance(rev, Revision)


async def test_list_syncable_revisions(client: AsyncClient):
    revisions = await client.alm.list_syncable_revisions("23485C42502B4830AB1C08CAD21FD116")
    assert isinstance(revisions, list)
    assert all(isinstance(rev, Revision) for rev in revisions)


async def test_create_revision(client: AsyncClient):
    src_client = AsyncClient.from_existing(client, model_id="23485C42502B4830AB1C08CAD21FD116")
    await src_client.transactional.insert_list_items(101000000004, [{"name": str(uuid4())}])
    name, desc = datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Test Sync Revision."
    revision = await client.alm.create_revision(name, desc)
    assert isinstance(revision, Revision)
    assert revision.name == name
    assert revision.description == desc


async def test_sync_models(client: AsyncClient):
    src_model = "23485C42502B4830AB1C08CAD21FD116"
    src = AsyncClient.from_existing(client, model_id=src_model)
    src_rev, latest_rev = await gather(
        src.alm.get_latest_revision(), client.alm.get_latest_revision()
    )
    sync_task = await client.alm.sync_models(
        source_revision_id=src_rev.id, source_model_id=src_model, target_revision_id=latest_rev.id
    )
    assert isinstance(sync_task, SyncTask)
    assert sync_task.result.source_revision_id == src_rev.id
    assert sync_task.result.target_revision_id == latest_rev.id


async def test_list_models_for_revision(client: AsyncClient):
    rev = await client.alm.get_latest_revision()
    model_revs = await client.alm.list_models_for_revision(rev.id)
    assert isinstance(model_revs, list)
    assert all(isinstance(rev, ModelRevision) for rev in model_revs)


async def test_list_sync_tasks(client: AsyncClient):
    tasks = await client.alm.list_sync_tasks()
    assert isinstance(tasks, list)
    assert all(isinstance(task, TaskSummary) for task in tasks)
