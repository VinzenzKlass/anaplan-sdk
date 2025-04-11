from anaplan_sdk import Client


def test_get_revisions(client: Client):
    revs = client.alm.get_revisions()
    assert isinstance(revs, list)
    assert len(revs) > 0


def test_get_models_for_revision(client: Client):
    model_revs = client.alm.get_models_for_revision("44867AAA4DD94C6EB8A23690A0C11DF4")
    assert isinstance(model_revs, list)
    assert len(model_revs) > 0


def test_get_sync_tasks(client: Client):
    tasks = client.alm.get_sync_tasks()
    assert isinstance(tasks, list)


def test_get_syncable_revisions(client: Client):
    models = client.alm.get_syncable_revisions("327F80BA66344A1C84C69AE82C006CDE")
    assert isinstance(models, list)


def test_get_latest_revision(client: Client):
    revs = client.alm.get_latest_revision()
    assert isinstance(revs, list)
