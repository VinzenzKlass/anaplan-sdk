import logging
import string
import sys
from os import getenv
from random import choices
from typing import Any

import pytest

from anaplan_sdk.models.cloud_works import (
    AnaplanSource,
    AnaplanTarget,
    AzureBlobConnectionInput,
    ConnectionInput,
    FileSource,
    FileSourceInput,
    FileTarget,
    IntegrationInput,
    IntegrationJob,
    IntegrationJobInput,
    IntegrationProcessInput,
    NotificationConfigInput,
    NotificationInput,
    NotificationItemInput,
    ScheduleInput,
    SingleIntegration,
    TableSource,
    TableTarget,
)
from anaplan_sdk.models.flows import FlowInput, FlowStepInput

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("anaplan_sdk").setLevel(logging.INFO)


@pytest.fixture(scope="session")
def py_version():
    return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"


@pytest.fixture(scope="session")
def list_items_long():
    return [{"name": i, "code": i} for i in range(200_000)]  # Force several batches


@pytest.fixture(scope="session")
def list_items_short():
    return [{"name": i, "code": i} for i in range(1_000)]  # Single batch


@pytest.fixture(scope="session")
def connection_id():
    return "8b2d5f3a2ff64f13ab52e5b993896386"


@pytest.fixture(scope="session")
def error_run_id():
    return "910a68fb814e4225ad683bdafb70ae65"


@pytest.fixture(scope="session")
def scim_user_id():
    return "38a0546fd5894c1fac87f8fb71566b3f"


@pytest.fixture
def name():
    return "Test_" + "".join(choices(string.ascii_uppercase + string.digits, k=12))


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
def integration_pydantic(name, connection_id):
    source = FileSourceInput(
        type="AzureBlob", connection_id=connection_id, file="dummy/liquor_sales.csv"
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
    source = FileSourceInput(
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
            "config": [{"type": "full_failure", "users": ["8a868cd97f8f98a3017fe45cbdc65e25"]}]
        },
    }


@pytest.fixture
def flow_pydantic(name):
    return FlowInput(
        name=name,
        steps=[
            FlowStepInput(referrer="840ccd8a279a454d99577d9538f24f09"),
            FlowStepInput(
                referrer="c0fa795faac047468a59c8dbe3752d75",
                depends_on=["840ccd8a279a454d99577d9538f24f09"],
            ),
        ],
    )


@pytest.fixture
def flow_dict(name):
    return {
        "name": name,
        "steps": [
            {"referrer": "840ccd8a279a454d99577d9538f24f09"},
            {
                "referrer": "c0fa795faac047468a59c8dbe3752d75",
                "dependsOn": ["840ccd8a279a454d99577d9538f24f09"],
            },
        ],
    }


@pytest.fixture(scope="session")
def integration_validator():
    def validate(integrations: list[SingleIntegration]):
        assert all(isinstance(i, SingleIntegration) for i in integrations)
        assert all(
            isinstance(i.jobs, list) and len(i.jobs) > 0 and isinstance(j, IntegrationJob)
            for i in integrations[1:]
            for j in i.jobs
        )
        process, gbq_import, gbq_export, s3_import, s3_export, az_import, az_export = integrations
        assert (
            isinstance(process.process_id, int)
            and (119000000000 > process.process_id >= 118000000000)
            and (process.jobs is None)
        )

        integration_configs = (
            (gbq_import, TableSource, AnaplanTarget),
            (gbq_export, AnaplanSource, TableTarget),
            (s3_import, FileSource, AnaplanTarget),
            (s3_export, AnaplanSource, FileTarget),
            (az_import, FileSource, AnaplanTarget),
            (az_export, AnaplanSource, FileTarget),
        )
        assert all(
            isinstance(integration.jobs[0].sources[0], source_type)
            and isinstance(integration.jobs[0].targets[0], target_type)
            for integration, source_type, target_type in integration_configs
        )

    return validate
