import os

import anaplan_sdk

client = anaplan_sdk.Client(
    workspace_id=os.getenv("ANAPLAN_SDK_TEST_WORKSPACE_ID"),
    model_id=os.getenv("ANAPLAN_SDK_TEST_MODEL_ID"),
    certificate=os.getenv("ANAPLAN_SDK_TEST_CERT"),
    private_key=os.getenv("ANAPLAN_SDK_TEST_PK"),
    retry_count=3,
).alm


def test_get_revisions():
    revs = client.get_revisions()
    assert isinstance(revs, list)
    assert len(revs) > 0


def test_get_models_for_revision():
    model_revs = client.get_models_for_revision("44867AAA4DD94C6EB8A23690A0C11DF4")
    assert isinstance(model_revs, list)
    assert len(model_revs) > 0


def test_get_sync_tasks():
    tasks = client.get_sync_tasks()
    assert isinstance(tasks, list)


def test_get_syncable_revisions():
    models = client.get_syncable_revisions("327F80BA66344A1C84C69AE82C006CDE")
    assert isinstance(models, list)


def test_get_latest_revision():
    revs = client.get_latest_revision()
    assert isinstance(revs, list)
