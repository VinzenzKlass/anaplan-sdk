import logging
import os
import string
import sys
from random import choices
from typing import Any, Callable

import pytest

import anaplan_sdk.models.cloud_works as cwm
from anaplan_sdk.models.flows import FlowInput, FlowStepInput

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("anaplan_sdk").setLevel(logging.INFO)


@pytest.fixture(scope="session")
def model_ids_for_py_version(py_version: str) -> tuple[str, str]:
    demo_tenant_id = "8a81b09d599f3c6e0159f605560c2630"
    if "3.10" in py_version:
        return demo_tenant_id, "060D1DD6C9D04DD4BF03BA96C1C4B93C"
    if "3.11" in py_version:
        return demo_tenant_id, "D2D29CEE237C422099D83DCC4338CEA6"
    if "3.12" in py_version:
        return demo_tenant_id, "6EE2A426C16B464193498C1FE28972D1"
    if "3.13" in py_version:
        return demo_tenant_id, "A7A1F7D149054E3080C95C8A085738B5"
    if "3.14" in py_version:
        return demo_tenant_id, "1D1741C3DD1042A68D8336B328C2324E"

    logging.fatal(f"Unsupported Python version: {py_version}")
    exit(1)


@pytest.fixture(scope="session")
def py_version() -> str:
    return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"


@pytest.fixture(scope="session")
def list_items_long() -> list[dict[str, int]]:
    return [{"name": i, "code": i} for i in range(200_000)]  # Force several batches


@pytest.fixture(scope="session")
def list_items_short() -> list[dict[str, int]]:
    return [{"name": i, "code": i} for i in range(1_000)]  # Single batch


@pytest.fixture(scope="session")
def connection_id() -> str:
    return "8b2d5f3a2ff64f13ab52e5b993896386"


@pytest.fixture(scope="session")
def error_run_id() -> str:
    return "910a68fb814e4225ad683bdafb70ae65"


@pytest.fixture(scope="session")
def scim_user_id() -> str:
    return "38a0546fd5894c1fac87f8fb71566b3f"


@pytest.fixture
def name() -> str:
    return "Test_" + "".join(choices(string.ascii_uppercase + string.digits, k=12))


@pytest.fixture
def az_blob_connection(name: str) -> cwm.ConnectionInput:
    return cwm.ConnectionInput(
        type="AzureBlob",
        body=cwm.AzureBlobConnectionInput(
            storage_account_name=os.environ["AZ_STORAGE_ACCOUNT"],
            container_name="raw",
            name=name,
            sas_token=os.environ["AZ_STORAGE_SAS_TOKEN"],
        ),
    )


@pytest.fixture
def az_blob_connection_dict(name: str) -> dict[str, Any]:
    return {
        "type": "AzureBlob",
        "body": {
            "storageAccountName": os.environ["AZ_STORAGE_ACCOUNT"],
            "containerName": "raw",
            "name": name,
            "sasToken": os.environ["AZ_STORAGE_SAS_TOKEN"],
        },
    }


@pytest.fixture
def integration_pydantic(name: str, connection_id: str) -> cwm.IntegrationInput:
    source = cwm.FileSourceInput(
        type="AzureBlob", connection_id=connection_id, file="dummy/liquor_sales.csv"
    )
    target = cwm.AnaplanTarget(action_id=112000000064, file_id=113000000055)
    return cwm.IntegrationInput(
        name=name,
        workspace_id=os.environ["ANAPLAN_SDK_TEST_WORKSPACE_ID"],
        model_id=os.environ["ANAPLAN_SDK_TEST_MODEL_ID"],
        jobs=[
            cwm.IntegrationJobInput(type="AzureBlobToAnaplan", sources=[source], targets=[target])
        ],
    )


@pytest.fixture
def multi_step_integration_pydantic(name: str, connection_id: str) -> cwm.IntegrationInput:
    source = cwm.FileSourceInput(
        type="AzureBlob", connection_id=connection_id, file="dummy/liquor_sales.csv"
    )
    target = cwm.AnaplanTarget(action_id=112000000064, file_id=113000000055)
    job = cwm.IntegrationJobInput(type="AzureBlobToAnaplan", sources=[source], targets=[target])
    return cwm.IntegrationInput(
        name=name,
        process_id=118000000012,
        workspace_id=os.environ["ANAPLAN_SDK_TEST_WORKSPACE_ID"],
        model_id=os.environ["ANAPLAN_SDK_TEST_MODEL_ID"],
        jobs=[job, job],
    )


@pytest.fixture
def process_integration_pydantic(name: str) -> cwm.IntegrationProcessInput:
    return cwm.IntegrationProcessInput(
        name=name,
        process_id=118000000012,
        workspace_id=os.environ["ANAPLAN_SDK_TEST_WORKSPACE_ID"],
        model_id=os.environ["ANAPLAN_SDK_TEST_MODEL_ID"],
    )


@pytest.fixture
def integration_dict(name: str, connection_id: str) -> dict[str, Any]:
    return {
        "name": name,
        "version": "2.0",
        "workspaceId": os.environ["ANAPLAN_SDK_TEST_WORKSPACE_ID"],
        "modelId": os.environ["ANAPLAN_SDK_TEST_MODEL_ID"],
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
def multi_step_integration_dict(name: str, connection_id: str) -> dict[str, Any]:
    return {
        "name": name,
        "version": "2.0",
        "workspaceId": os.environ["ANAPLAN_SDK_TEST_WORKSPACE_ID"],
        "modelId": os.environ["ANAPLAN_SDK_TEST_MODEL_ID"],
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
def process_integration_dict(name: str) -> dict[str, Any]:
    return {
        "name": name,
        "version": "2.0",
        "processId": 118000000012,
        "workspaceId": os.environ["ANAPLAN_SDK_TEST_WORKSPACE_ID"],
        "modelId": os.environ["ANAPLAN_SDK_TEST_MODEL_ID"],
    }


@pytest.fixture
def schedule_pydantic(name: str) -> cwm.ScheduleInput:
    return cwm.ScheduleInput(
        name=name,
        timezone="Europe/Paris",
        start_date="2027-01-01",
        end_date="2029-01-01",
        days_of_week=[0, 2, 5],
        type="daily",
        time="12:00",
    )


@pytest.fixture
def schedule_dict(name: str) -> dict[str, Any]:
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
def notification_pydantic(name: str) -> cwm.NotificationInput:
    return cwm.NotificationInput(
        integration_ids=[],
        channels=["in_app"],
        notifications=cwm.NotificationConfigInput(
            config=[
                cwm.NotificationItemInput(
                    type="full_failure", users=["8a868cd97f8f98a3017fe45cbdc65e25"]
                )
            ]
        ),
    )


@pytest.fixture
def notification_dict(name: str) -> dict[str, Any]:
    return {
        "integrationIds": [],
        "channels": ["in_app"],
        "notifications": {
            "config": [{"type": "full_failure", "users": ["8a868cd97f8f98a3017fe45cbdc65e25"]}]
        },
    }


@pytest.fixture
def flow_pydantic(name: str) -> FlowInput:
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
def flow_dict(name: str) -> dict[str, Any]:
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
def integration_validator() -> Callable[[list[cwm.SingleIntegration]], None]:
    def validate(integrations: list[cwm.SingleIntegration]) -> None:
        assert all(isinstance(i, cwm.SingleIntegration) for i in integrations)
        assert all(
            isinstance(i.jobs, list) and len(i.jobs) > 0 and isinstance(j, cwm.IntegrationJob)
            for i in integrations[1:]
            for j in i.jobs  # pyright: ignore[reportOptionalIterable]
        )
        process, gbq_import, gbq_export, s3_import, s3_export, az_import, az_export = integrations
        assert (
            isinstance(process.process_id, int)
            and (119000000000 > process.process_id >= 118000000000)
            and (process.jobs is None)
        )

        integration_configs = (
            (gbq_import, cwm.TableSource, cwm.AnaplanTarget),
            (gbq_export, cwm.AnaplanSource, cwm.TableTarget),
            (s3_import, cwm.FileSource, cwm.AnaplanTarget),
            (s3_export, cwm.AnaplanSource, cwm.FileTarget),
            (az_import, cwm.FileSource, cwm.AnaplanTarget),
            (az_export, cwm.AnaplanSource, cwm.FileTarget),
        )
        assert all(
            isinstance(integration.jobs[0].sources[0], source_type)  # pyright: ignore
            and isinstance(integration.jobs[0].targets[0], target_type)  # pyright: ignore
            for integration, source_type, target_type in integration_configs
        )

    return validate
