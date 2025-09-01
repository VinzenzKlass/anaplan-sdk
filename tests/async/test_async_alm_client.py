from asyncio import gather
from datetime import datetime
from uuid import uuid4

from anaplan_sdk import AsyncClient
from anaplan_sdk.models import (
    ModelRevision,
    ReportTask,
    Revision,
    SummaryReport,
    SyncTask,
    TaskSummary,
)


async def test_change_model_status(alm_client: AsyncClient):
    await alm_client.alm.change_model_status("offline")


async def test_list_revisions(alm_client: AsyncClient):
    revisions = await alm_client.alm.get_revisions()
    assert isinstance(revisions, list)
    assert all(isinstance(rev, Revision) for rev in revisions)


async def test_get_latest_revision(alm_client: AsyncClient):
    rev = await alm_client.alm.get_latest_revision()
    assert isinstance(rev, Revision)


async def test_list_syncable_revisions(alm_client: AsyncClient, alm_src_model_id: str):
    revisions = await alm_client.alm.get_syncable_revisions(alm_src_model_id)
    assert isinstance(revisions, list)
    assert all(isinstance(rev, Revision) for rev in revisions)


async def test_create_revision(alm_src_client: AsyncClient):
    await alm_src_client.tr.insert_list_items(
        101000000005, [{"name": str(uuid4()), "code": str(uuid4())}]
    )
    name, desc = datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Test Sync Revision."
    revision = await alm_src_client.alm.create_revision(name, desc)
    assert isinstance(revision, Revision)
    assert revision.name == name
    assert revision.description == desc


async def test_create_comparison_summary_task(
    alm_client: AsyncClient, alm_src_client: AsyncClient, alm_src_model_id: str
):
    src_rev, latest_rev = await gather(
        alm_src_client.alm.get_latest_revision(), alm_client.alm.get_latest_revision()
    )
    report_task = await alm_client.alm.create_comparison_summary(
        src_rev.id, alm_src_model_id, latest_rev.id, False
    )
    assert isinstance(report_task, ReportTask)


async def test_create_comparison_summary(
    alm_client: AsyncClient, alm_src_client: AsyncClient, alm_src_model_id: str
):
    src_rev, latest_rev = await gather(
        alm_src_client.alm.get_latest_revision(), alm_client.alm.get_latest_revision()
    )
    report = await alm_client.alm.create_comparison_summary(
        src_rev.id, alm_src_model_id, latest_rev.id
    )
    assert isinstance(report, SummaryReport)
    assert sum((report.totals.created, report.totals.modified, report.totals.deleted)) > 0


async def test_create_comparison_report(
    alm_client: AsyncClient, alm_src_client: AsyncClient, alm_src_model_id: str
):
    src_rev, latest_rev = await gather(
        alm_src_client.alm.get_latest_revision(), alm_client.alm.get_latest_revision()
    )
    report_task = await alm_client.alm.create_comparison_report(
        src_rev.id, alm_src_model_id, latest_rev.id
    )
    assert isinstance(report_task, ReportTask)
    report = await alm_client.alm.get_comparison_report(report_task)
    assert report is not None


async def test_sync_models(
    alm_client: AsyncClient, alm_src_client: AsyncClient, alm_src_model_id: str
):
    src_rev, latest_rev = await gather(
        alm_src_client.alm.get_latest_revision(), alm_client.alm.get_latest_revision()
    )
    sync_task = await alm_client.alm.sync_models(src_rev.id, alm_src_model_id, latest_rev.id)
    assert isinstance(sync_task, SyncTask)
    assert sync_task.result.source_revision_id == src_rev.id
    assert sync_task.result.target_revision_id == latest_rev.id


async def test_list_models_for_revision(alm_client: AsyncClient):
    rev = await alm_client.alm.get_latest_revision()
    model_revs = await alm_client.alm.get_models_for_revision(rev.id)
    assert isinstance(model_revs, list)
    assert all(isinstance(rev, ModelRevision) for rev in model_revs)


async def test_list_sync_tasks(alm_client: AsyncClient):
    tasks = await alm_client.alm.get_sync_tasks()
    assert isinstance(tasks, list)
    assert all(isinstance(task, TaskSummary) for task in tasks)
