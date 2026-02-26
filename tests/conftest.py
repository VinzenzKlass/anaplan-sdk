import logging
import os
import random
import string
import sys
import time
from dataclasses import dataclass
from random import choices
from typing import Any, Callable

import pytest

import anaplan_sdk.models.cloud_works as cwm
from anaplan_sdk.models.flows import FlowInput, FlowStepInput

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("anaplan_sdk").setLevel(logging.INFO)


@dataclass(slots=True, frozen=True, eq=False)
class PyVersionConfig:
    workspace_id: str
    model_id: str
    alm_model_id_async: str
    alm_src_model_id_async: str
    test_integration_async: str
    test_notification_async: str
    test_flow_async: str
    alm_model_id_sync: str
    alm_src_model_id_sync: str
    test_integration_sync: str
    test_notification_sync: str
    test_flow_sync: str
    connection_id: str = "8b2d5f3a2ff64f13ab52e5b993896386"
    error_run_id: str = "910a68fb814e4225ad683bdafb70ae65"
    scim_user_id: str = "38a0546fd5894c1fac87f8fb71566b3f"


@pytest.fixture(autouse=True)
def random_delay_between_tests():
    yield
    time.sleep(random.uniform(0, 3))  # Avoid hitting rate limit too often


@pytest.fixture(scope="session")
def config() -> PyVersionConfig:
    py_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    workspace_id = "8a81b09d599f3c6e0159f605560c2630"
    if "3.10" in py_version:
        return PyVersionConfig(
            workspace_id=workspace_id,
            model_id="060D1DD6C9D04DD4BF03BA96C1C4B93C",
            alm_model_id_async="174F0F20D5A84FF09C812E95B8E50997",
            alm_src_model_id_async="C852660C6AF547258FB6B97D4942AB27",
            test_integration_async="840ccd8a279a454d99577d9538f24f09",
            test_notification_async="bfe29c0ff7434bde96c94ce1ec1b8e0a",
            test_flow_async="35e19e2f0f594d589f07fd8ba98c30a8",
            alm_model_id_sync="7538F3BE46B94F208C6AF5051919E56E",
            alm_src_model_id_sync="662239743F56420EBECAE7EE0659475C",
            test_integration_sync="44bd0bd4606b4f77b62e70d5ff617f3f",
            test_notification_sync="efc8e3340c054f00bc20dbab1719531f",
            test_flow_sync="8f9a377127844984b12775e9ca072108",
        )
    if "3.11" in py_version:
        return PyVersionConfig(
            workspace_id=workspace_id,
            model_id="D2D29CEE237C422099D83DCC4338CEA6",
            alm_model_id_async="FFBB7D26E61040EBB5CACD80F7F8A01B",
            alm_src_model_id_async="C042E6A3F0334DEC9C826E1E12947789",
            test_integration_async="c0fa795faac047468a59c8dbe3752d75",
            test_notification_async="e2c709c74998460c8688b641cde07cd3",
            test_flow_async="0ca27f18a3f04a1382ecd1745609329b",
            alm_model_id_sync="5C31E832E0B04567B5A8784B25AF3572",
            alm_src_model_id_sync="4FCB1B5224F64339AADC7B322E1663EF",
            test_integration_sync="dfcf1caace4f41748fc589e83c68c65a",
            test_notification_sync="81f0e8c718ed47ada55ce9b88dad548f",
            test_flow_sync="240a3d55754843be824cb4f97e48e061",
        )
    if "3.12" in py_version:
        return PyVersionConfig(
            workspace_id=workspace_id,
            model_id="6EE2A426C16B464193498C1FE28972D1",
            alm_model_id_async="FDB11C592E9445D78337F01BABC89880",
            alm_src_model_id_async="E130519009E54304A54D8D9F1C6D2725",
            test_integration_async="0204ea3261c8431e9e36ff1239c16247",
            test_notification_async="e0f3d33a9c114e3a9c0e0908cffdb5e3",
            test_flow_async="c9fd9841222d43d9886758ba4db4c340",
            alm_model_id_sync="7F51D466D915425CA80BEDF54BF364AE",
            alm_src_model_id_sync="A68B26D67D00443FB8A3428CC83E427D",
            test_integration_sync="18e2c03b0bdf4593bdd964786891ead8",
            test_notification_sync="d90749ebb0e94692b4eaba1963cf0959",
            test_flow_sync="afc6cec5d4b343c6abb4f0b3d41f1f7f",
        )
    if "3.13" in py_version:
        return PyVersionConfig(
            workspace_id=workspace_id,
            model_id="A7A1F7D149054E3080C95C8A085738B5",
            alm_model_id_async="0CBB17195E5D445A9A3692F481D66CBE",
            alm_src_model_id_async="12A4D6B9A816481F83F795F857407049",
            test_integration_async="cf9e1cf27a0f4eddb37a2a4807fd0ffc",
            test_notification_async="e57b5620f006444a9324baaa4bd891ff",
            test_flow_async="c330ca2eda974650bd99fea50b0e3acd",
            alm_model_id_sync="33A804FE8FE34AC291A6E866CA6B2284",
            alm_src_model_id_sync="5327704441464F36B4B05C6BF9DFACD2",
            test_integration_sync="c5bd6fd4b9414ea0959795ccebc8126a",
            test_notification_sync="393d6e91e1874e28baccd7441d28ba36",
            test_flow_sync="61f2a2b05ac64598bfeb6d9eb7eff97a",
        )
    if "3.14" in py_version:
        return PyVersionConfig(
            workspace_id=workspace_id,
            model_id="1D1741C3DD1042A68D8336B328C2324E",
            alm_model_id_async="C48A0D162C964C02964E2EB78190D480",
            alm_src_model_id_async="37DEEDC7D5F2434BBBF836251B90CE23",
            test_integration_async="1eaee08c758e44948805632e766ec0ee",
            test_notification_async="6da7d462645744c39c5b17405daf10c1",
            test_flow_async="e95f6ed1fc2f4c02820edebb919e20b4",
            alm_model_id_sync="06520A761F0B4ECF8AED011A6B7DADCA",
            alm_src_model_id_sync="704A4A635CF1429E91B9C712B848F114",
            test_integration_sync="132704f947044cae8713d9a95da1ba15",
            test_notification_sync="a03de322708b4451b8117544197a8808",
            test_flow_sync="68c07638382244cda4e2d997ddc0b05b",
        )

    logging.fatal(f"Unsupported Python version: {py_version}")
    exit(1)


@pytest.fixture(scope="session")
def model_ids_for_py_version(config: PyVersionConfig) -> tuple[str, str]:
    return config.workspace_id, config.model_id


@pytest.fixture(scope="session")
def list_items_long() -> list[dict[str, Any]]:
    return [{"name": i, "code": i} for i in range(200_000)]  # Force several batches


@pytest.fixture(scope="session")
def list_items_short() -> list[dict[str, Any]]:
    return [{"name": i, "code": i} for i in range(1_000)]  # Single batch


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
def integration_pydantic(name: str, config: PyVersionConfig) -> cwm.IntegrationInput:
    source = cwm.FileSourceInput(
        type="AzureBlob", connection_id=config.connection_id, file="dummy/liquor_sales.csv"
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
def multi_step_integration_pydantic(name: str, config: PyVersionConfig) -> cwm.IntegrationInput:
    source = cwm.FileSourceInput(
        type="AzureBlob", connection_id=config.connection_id, file="dummy/liquor_sales.csv"
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
def integration_dict(name: str, config: PyVersionConfig) -> dict[str, Any]:
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
                        "connectionId": config.connection_id,
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
def multi_step_integration_dict(name: str, config: PyVersionConfig) -> dict[str, Any]:
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
                        "connectionId": config.connection_id,
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
                        "connectionId": config.connection_id,
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
