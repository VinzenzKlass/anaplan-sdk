import logging
import string
from os import getenv
from random import choices

import pytest

from anaplan_sdk.models.cloud_works import AzureBlobConnectionInput, ConnectionInput

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("anaplan_sdk").setLevel(logging.INFO)


@pytest.fixture(scope="session")
def list_items_long():
    return [{"name": i, "code": i} for i in range(200_000)]  # Force several batches


@pytest.fixture(scope="session")
def list_items_short():
    return [{"name": i, "code": i} for i in range(1_000)]  # Single batch


@pytest.fixture
def connection_name():
    return "".join(choices(string.ascii_uppercase + string.digits, k=12))


@pytest.fixture
def connection_id():
    return "9d5556bf5a934d6cae3e3cf9c620853b"


@pytest.fixture
def integration_id():
    return "339dce4f797a435d98cee35bed781d28"


@pytest.fixture
def az_blob_connection(connection_name):
    return ConnectionInput(
        type="AzureBlob",
        body=AzureBlobConnectionInput(
            storage_account_name=getenv("AZ_STORAGE_ACCOUNT"),
            container_name="raw",
            name=connection_name,
            sas_token=getenv("AZ_STORAGE_SAS_TOKEN"),
        ),
    )


@pytest.fixture
def az_blob_connection_dict(connection_name):
    return {
        "type": "AzureBlob",
        "body": {
            "storageAccountName": getenv("AZ_STORAGE_ACCOUNT"),
            "containerName": "raw",
            "name": connection_name,
            "sasToken": getenv("AZ_STORAGE_SAS_TOKEN"),
        },
    }
