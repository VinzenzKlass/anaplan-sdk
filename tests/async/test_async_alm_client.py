from anaplan_sdk import AsyncClient


async def test_set_model_status(client: AsyncClient):
    await client.alm.change_model_status("online")


async def test_get_syncable_revisions(client: AsyncClient):
    models = await client.alm.list_syncable_revisions("327F80BA66344A1C84C69AE82C006CDE")
    assert isinstance(models, list)


async def test_get_latest_revision(client: AsyncClient):
    revs = await client.alm.get_latest_revision()
    assert isinstance(revs, list)


async def test_get_revisions(client: AsyncClient):
    revs = await client.alm.list_revisions()
    assert isinstance(revs, list)
    assert len(revs) > 0


async def test_get_models_for_revision(client: AsyncClient):
    model_revs = await client.alm.list_models_for_revision("44867AAA4DD94C6EB8A23690A0C11DF4")
    assert isinstance(model_revs, list)
    assert len(model_revs) > 0


async def test_get_sync_tasks(client: AsyncClient):
    tasks = await client.alm.list_sync_tasks()
    assert isinstance(tasks, list)
