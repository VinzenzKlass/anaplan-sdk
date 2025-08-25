from os import getenv

import pytest

from anaplan_sdk import AsyncClient


@pytest.fixture(scope="session")
def client() -> AsyncClient:
    return AsyncClient(
        workspace_id=getenv("ANAPLAN_SDK_TEST_WORKSPACE_ID"),
        model_id=getenv("ANAPLAN_SDK_TEST_MODEL_ID"),
        certificate=getenv("ANAPLAN_SDK_TEST_CERT"),
        private_key=getenv("ANAPLAN_SDK_TEST_PK"),
        retry_count=3,
        backoff=5,
        timeout=120,
    )


@pytest.fixture(scope="session")
def client_small_pages() -> AsyncClient:
    return AsyncClient(
        workspace_id=getenv("ANAPLAN_SDK_TEST_WORKSPACE_ID"),
        model_id=getenv("ANAPLAN_SDK_TEST_MODEL_ID"),
        certificate=getenv("ANAPLAN_SDK_TEST_CERT"),
        private_key=getenv("ANAPLAN_SDK_TEST_PK"),
        page_size=100,
        retry_count=3,
        backoff=5,
        timeout=120,
    )


@pytest.fixture(scope="session")
def alm_src_client(client: AsyncClient, alm_src_model_id) -> AsyncClient:
    return client.with_model(alm_src_model_id)


@pytest.fixture(scope="session")
def alm_client(client: AsyncClient, alm_model_id) -> AsyncClient:
    return client.with_model(alm_model_id)


@pytest.fixture(scope="session")
def broken_client():
    return AsyncClient(
        workspace_id="",
        model_id="",
        certificate=getenv("ANAPLAN_SDK_TEST_CERT"),
        private_key=getenv("ANAPLAN_SDK_TEST_PK"),
        retry_count=1,
    )


@pytest.fixture(scope="session")
def test_list(py_version):
    if "3.10" in py_version:
        return 101000000309
    if "3.11" in py_version:
        return 101000000310
    if "3.12" in py_version:
        return 101000000311
    return 101000000312


@pytest.fixture(scope="session")
def test_file(py_version):
    if "3.10" in py_version:
        return 113000000061
    if "3.11" in py_version:
        return 113000000062
    if "3.12" in py_version:
        return 113000000063
    return 113000000064


@pytest.fixture(scope="session")
def test_action(py_version):
    if "3.10" in py_version:
        return 118000000028
    if "3.11" in py_version:
        return 118000000027
    if "3.12" in py_version:
        return 118000000026
    return 118000000025


@pytest.fixture(scope="session")
def alm_src_model_id(py_version):
    if "3.10" in py_version:
        return "C852660C6AF547258FB6B97D4942AB27"
    if "3.11" in py_version:
        return "C042E6A3F0334DEC9C826E1E12947789"
    if "3.12" in py_version:
        return "E130519009E54304A54D8D9F1C6D2725"
    return "12A4D6B9A816481F83F795F857407049"


@pytest.fixture(scope="session")
def alm_model_id(py_version):
    if "3.10" in py_version:
        return "174F0F20D5A84FF09C812E95B8E50997"
    if "3.11" in py_version:
        return "FFBB7D26E61040EBB5CACD80F7F8A01B"
    if "3.12" in py_version:
        return "FDB11C592E9445D78337F01BABC89880"
    return "0CBB17195E5D445A9A3692F481D66CBE"


@pytest.fixture(scope="session")
def test_integration(py_version):
    if "3.10" in py_version:
        return "840ccd8a279a454d99577d9538f24f09"
    if "3.11" in py_version:
        return "c0fa795faac047468a59c8dbe3752d75"
    if "3.12" in py_version:
        return "0204ea3261c8431e9e36ff1239c16247"
    return "cf9e1cf27a0f4eddb37a2a4807fd0ffc"


@pytest.fixture(scope="session")
def test_notification(py_version):
    if "3.10" in py_version:
        return "bfe29c0ff7434bde96c94ce1ec1b8e0a"
    if "3.11" in py_version:
        return "e2c709c74998460c8688b641cde07cd3"
    if "3.12" in py_version:
        return "e0f3d33a9c114e3a9c0e0908cffdb5e3"
    return "e57b5620f006444a9324baaa4bd891ff"


@pytest.fixture(scope="session")
def test_flow(py_version):
    if "3.10" in py_version:
        return "35e19e2f0f594d589f07fd8ba98c30a8"
    if "3.11" in py_version:
        return "0ca27f18a3f04a1382ecd1745609329b"
    if "3.12" in py_version:
        return "c9fd9841222d43d9886758ba4db4c340"
    return "c330ca2eda974650bd99fea50b0e3acd"


@pytest.fixture(scope="session")
def registry():
    return {"connections": [], "integrations": [], "flows": [], "run_id": None}
