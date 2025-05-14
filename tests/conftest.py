import logging
import string
from os import getenv
from random import choices
from typing import Any

import pytest

from anaplan_sdk.models.cloud_works import (
    AnaplanTarget,
    AzureBlobConnectionInput,
    ConnectionInput,
    FileSource,
    IntegrationInput,
    IntegrationJobInput,
    IntegrationProcessInput,
    NotificationConfigInput,
    NotificationInput,
    NotificationItemInput,
    ScheduleInput,
)
from anaplan_sdk.models.flows import FlowInput, FlowStepInput

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("anaplan_sdk").setLevel(logging.INFO)


@pytest.fixture(scope="session")
def list_items_long():
    return [{"name": i, "code": i} for i in range(200_000)]  # Force several batches


@pytest.fixture(scope="session")
def list_items_short():
    return [{"name": i, "code": i} for i in range(1_000)]  # Single batch


@pytest.fixture(scope="session")
def connection_id():
    return "35006b13dc574649a35d7910ab09c32a"


@pytest.fixture(scope="session")
def error_run_id():
    return "672e8fa8a4ab49fe812efa09f270f564"


@pytest.fixture
def name():
    return "Test_" + "".join(choices(string.ascii_uppercase + string.digits, k=6))


@pytest.fixture
def az_blob_connection(name):
    return ConnectionInput(
        type="AzureBlob",
        body=AzureBlobConnectionInput(
            storage_account_name=getenv("AZ_STORAGE_ACCOUNT"),
            container_name="raw",
            name=name,
            sas_token=getenv("AZ_STORAGE_SAS_TOKEN"),
        ),
    )


@pytest.fixture
def az_blob_connection_dict(name):
    return {
        "type": "AzureBlob",
        "body": {
            "storageAccountName": getenv("AZ_STORAGE_ACCOUNT"),
            "containerName": "raw",
            "name": name,
            "sasToken": getenv("AZ_STORAGE_SAS_TOKEN"),
        },
    }


@pytest.fixture
def integration_pydantic(name):
    source = FileSource(
        type="AzureBlob",
        connection_id="35006b13dc574649a35d7910ab09c32a",
        file="dummy/liquor_sales.csv",
    )
    target = AnaplanTarget(action_id=112000000064, file_id=113000000055)
    return IntegrationInput(
        name=name,
        workspace_id=getenv("ANAPLAN_SDK_TEST_WORKSPACE_ID"),
        model_id=getenv("ANAPLAN_SDK_TEST_MODEL_ID"),
        jobs=[IntegrationJobInput(type="AzureBlobToAnaplan", sources=[source], targets=[target])],
    )


@pytest.fixture
def multi_step_integration_pydantic(name, connection_id):
    source = FileSource(
        type="AzureBlob", connection_id=connection_id, file="dummy/liquor_sales.csv"
    )
    target = AnaplanTarget(action_id=112000000064, file_id=113000000055)
    job = IntegrationJobInput(type="AzureBlobToAnaplan", sources=[source], targets=[target])
    return IntegrationInput(
        name=name,
        process_id=118000000012,
        workspace_id=getenv("ANAPLAN_SDK_TEST_WORKSPACE_ID"),
        model_id=getenv("ANAPLAN_SDK_TEST_MODEL_ID"),
        jobs=[job, job],
    )


@pytest.fixture
def process_integration_pydantic(name):
    return IntegrationProcessInput(
        name=name,
        process_id=118000000012,
        workspace_id=getenv("ANAPLAN_SDK_TEST_WORKSPACE_ID"),
        model_id=getenv("ANAPLAN_SDK_TEST_MODEL_ID"),
    )


@pytest.fixture
def integration_dict(name, connection_id):
    return {
        "name": name,
        "version": "2.0",
        "workspaceId": getenv("ANAPLAN_SDK_TEST_WORKSPACE_ID"),
        "modelId": getenv("ANAPLAN_SDK_TEST_MODEL_ID"),
        "nuxVisible": False,
        "jobs": [
            {
                "type": "AzureBlobToAnaplan",
                "sources": [
                    {
                        "connectionId": connection_id,
                        "type": "AzureBlob",
                        "file": "dummy/liquor_sales.csv",
                    }
                ],
                "targets": [
                    {"type": "Anaplan", "actionId": "112000000001", "fileId": "112000000001"}
                ],
            }
        ],
    }


@pytest.fixture
def multi_step_integration_dict(name, connection_id) -> dict[str, Any]:
    return {
        "name": name,
        "version": "2.0",
        "workspaceId": getenv("ANAPLAN_SDK_TEST_WORKSPACE_ID"),
        "modelId": getenv("ANAPLAN_SDK_TEST_MODEL_ID"),
        "processId": "118000000012",
        "nuxVisible": False,
        "jobs": [
            {
                "type": "AzureBlobToAnaplan",
                "sources": [
                    {
                        "connectionId": connection_id,
                        "type": "AzureBlob",
                        "file": "dummy/liquor_sales.csv",
                    }
                ],
                "targets": [
                    {"type": "Anaplan", "actionId": "112000000064", "fileId": "113000000055"}
                ],
            },
            {
                "type": "AzureBlobToAnaplan",
                "sources": [
                    {
                        "connectionId": connection_id,
                        "type": "AzureBlob",
                        "file": "dummy/liquor_sales.csv",
                    }
                ],
                "targets": [
                    {"type": "Anaplan", "actionId": "112000000064", "fileId": "113000000055"}
                ],
            },
        ],
    }


@pytest.fixture
def process_integration_dict(name):
    return {
        "name": name,
        "version": "2.0",
        "processId": 118000000012,
        "workspaceId": getenv("ANAPLAN_SDK_TEST_WORKSPACE_ID"),
        "modelId": getenv("ANAPLAN_SDK_TEST_MODEL_ID"),
    }


@pytest.fixture
def schedule_pydantic(name):
    return ScheduleInput(
        name=name,
        timezone="Europe/Paris",
        start_date="2027-01-01",
        end_date="2029-01-01",
        days_of_week=[0, 2, 5],
        type="daily",
        time="12:00",
    )


@pytest.fixture
def schedule_dict(name):
    return {
        "name": name,
        "type": "daily",
        "timezone": "Europe/Paris",
        "time": "12:00",
        "daysOfWeek": [0, 2, 5],
        "startDate": "2027-01-01",
        "endDate": "2029-01-01",
    }


@pytest.fixture
def notification_pydantic(name):
    return NotificationInput(
        integration_ids=[],
        channels=["in_app"],
        notifications=NotificationConfigInput(
            config=[
                NotificationItemInput(
                    type="full_failure", users=["8a868cd97f8f98a3017fe45cbdc65e25"]
                )
            ]
        ),
    )


@pytest.fixture
def notification_dict(name):
    return {
        "integrationIds": [],
        "channels": ["in_app"],
        "notifications": {
            "config": [
                {
                    "type": "full_failure",
                    "users": ["8a868cd97f8f98a3017fe45cbdc65e25"],
                }
            ],
        },
    }


@pytest.fixture
def flow_pydantic(name):
    return FlowInput(
        name=name,
        steps=[
            FlowStepInput(referrer="157a5b07afe645c2a0d80df3a05e3ad9"),
            FlowStepInput(
                referrer="0405cf9a04874beda3ebe22ed871098c",
                depends_on=["157a5b07afe645c2a0d80df3a05e3ad9"],
            ),
        ],
    )


@pytest.fixture
def flow_dict(name):
    return {
        "name": name,
        "steps": [
            {"referrer": "157a5b07afe645c2a0d80df3a05e3ad9"},
            {
                "referrer": "0405cf9a04874beda3ebe22ed871098c",
                "dependsOn": ["157a5b07afe645c2a0d80df3a05e3ad9"],
            },
        ],
    }
