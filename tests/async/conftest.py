import os

import pytest

from anaplan_sdk import AsyncClient
from tests.conftest import PyVersionConfig


@pytest.fixture(scope="session")
def client(config: PyVersionConfig) -> AsyncClient:
    return AsyncClient(
        workspace_id=config.workspace_id,
        model_id=config.model_id,
        certificate=os.environ["ANAPLAN_SDK_TEST_CERT"],
        private_key=os.environ["ANAPLAN_SDK_TEST_PK"],
        retry_count=3,
        backoff=10,
        timeout=120,
    )


@pytest.fixture(scope="session")
def client_small_pages(config: PyVersionConfig) -> AsyncClient:
    return AsyncClient(
        workspace_id=config.workspace_id,
        model_id=config.model_id,
        certificate=os.environ["ANAPLAN_SDK_TEST_CERT"],
        private_key=os.environ["ANAPLAN_SDK_TEST_PK"],
        page_size=100,
        retry_count=3,
        backoff=5,
        timeout=120,
    )


@pytest.fixture(scope="session")
def alm_client(client: AsyncClient, config: PyVersionConfig) -> AsyncClient:
    return client.with_model(config.alm_model_id_async)


@pytest.fixture(scope="session")
def alm_src_client(client: AsyncClient, config: PyVersionConfig) -> AsyncClient:
    return client.with_model(config.alm_src_model_id_async)


@pytest.fixture(scope="session")
def test_integration_ids(config: PyVersionConfig) -> list[str]:
    return [
        config.test_integration_async,
        "040a5b1572d74e14adbbc8bada248f41",
        "7839b6bd6c0649acad13cf9d38a374f6",
        "fc24f171c6ba49b49b19b4502f98e62d",
        "a1b5719444444e678eb3b6bbcc137e1a",
        "d1108b906b9c4447b5a62af8f2938a5d",
        "7fede57c307b46d394b892456bc2083e",
    ]


@pytest.fixture(scope="session")
def broken_client() -> AsyncClient:
    return AsyncClient(
        workspace_id="",
        model_id="",
        certificate=os.environ["ANAPLAN_SDK_TEST_CERT"],
        private_key=os.environ["ANAPLAN_SDK_TEST_PK"],
        retry_count=1,
    )


@pytest.fixture(scope="session")
def registry() -> dict[str, list[dict[str, str]] | None]:
    return {"connections": [], "integrations": [], "flows": [], "run_id": None}
