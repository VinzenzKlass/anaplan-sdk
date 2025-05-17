import sys
from os import getenv

import pytest

from anaplan_sdk import Client


@pytest.fixture(scope="session")
def client() -> Client:
    return Client(
        workspace_id=getenv("ANAPLAN_SDK_TEST_WORKSPACE_ID"),
        model_id=getenv("ANAPLAN_SDK_TEST_MODEL_ID"),
        certificate=getenv("ANAPLAN_SDK_TEST_CERT"),
        private_key=getenv("ANAPLAN_SDK_TEST_PK"),
        retry_count=3,
    )


@pytest.fixture(scope="session")
def broken_client() -> Client:
    return Client(
        workspace_id="",
        model_id="",
        certificate=getenv("ANAPLAN_SDK_TEST_CERT"),
        private_key=getenv("ANAPLAN_SDK_TEST_PK"),
        retry_count=1,
    )


@pytest.fixture(scope="session")
def test_list():
    py_version = sys.version.split(" ")[0]
    if "3.10" in py_version:
        return 101000000305
    if "3.11" in py_version:
        return 101000000306
    if "3.12" in py_version:
        return 101000000307
    return 101000000308


@pytest.fixture(scope="session")
def test_file():
    py_version = sys.version.split(" ")[0]
    if "3.10" in py_version:
        return 113000000065
    if "3.11" in py_version:
        return 113000000066
    if "3.12" in py_version:
        return 113000000067
    return 113000000068


@pytest.fixture(scope="session")
def test_action():
    py_version = sys.version.split(" ")[0]
    if "3.10" in py_version:
        return 118000000024
    if "3.11" in py_version:
        return 118000000023
    if "3.12" in py_version:
        return 118000000022
    return 118000000021


@pytest.fixture(scope="session")
def test_integration():
    py_version = sys.version.split(" ")[0]
    if "3.10" in py_version:
        return "44bd0bd4606b4f77b62e70d5ff617f3f"
    if "3.11" in py_version:
        return "dfcf1caace4f41748fc589e83c68c65a"
    if "3.12" in py_version:
        return "18e2c03b0bdf4593bdd964786891ead8"
    return "c5bd6fd4b9414ea0959795ccebc8126a"


@pytest.fixture(scope="session")
def test_notification():
    py_version = sys.version.split(" ")[0]
    if "3.10" in py_version:
        return "efc8e3340c054f00bc20dbab1719531f"
    if "3.11" in py_version:
        return "81f0e8c718ed47ada55ce9b88dad548f"
    if "3.12" in py_version:
        return "d90749ebb0e94692b4eaba1963cf0959"
    return "393d6e91e1874e28baccd7441d28ba36"


@pytest.fixture(scope="session")
def test_flow():
    py_version = sys.version.split(" ")[0]
    if "3.10" in py_version:
        return "8f9a377127844984b12775e9ca072108"
    if "3.11" in py_version:
        return "240a3d55754843be824cb4f97e48e061"
    if "3.12" in py_version:
        return "afc6cec5d4b343c6abb4f0b3d41f1f7f"
    return "61f2a2b05ac64598bfeb6d9eb7eff97a"


@pytest.fixture(scope="session")
def registry():
    return {"connections": [], "integrations": [], "flows": [], "run_id": None}
