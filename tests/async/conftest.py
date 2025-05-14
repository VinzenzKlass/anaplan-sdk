import sys
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
    )


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
def test_list():
    py_version = sys.version.split(" ")[0]
    if "3.10" in py_version:
        return 101000000309
    if "3.11" in py_version:
        return 101000000310
    if "3.12" in py_version:
        return 101000000311
    return 101000000312


@pytest.fixture(scope="session")
def test_file():
    py_version = sys.version.split(" ")[0]
    if "3.10" in py_version:
        return 113000000061
    if "3.11" in py_version:
        return 113000000062
    if "3.12" in py_version:
        return 113000000063
    return 113000000064


@pytest.fixture(scope="session")
def test_action():
    py_version = sys.version.split(" ")[0]
    if "3.10" in py_version:
        return 118000000028
    if "3.11" in py_version:
        return 118000000027
    if "3.12" in py_version:
        return 118000000026
    return 118000000025


@pytest.fixture(scope="session")
def test_integration():
    py_version = sys.version.split(" ")[0]
    if "3.10" in py_version:
        return "157a5b07afe645c2a0d80df3a05e3ad9"
    if "3.11" in py_version:
        return "0405cf9a04874beda3ebe22ed871098c"
    if "3.12" in py_version:
        return "56798825a4484a06b82fe371f0c5699c"
    return "d49a2d72cdde43b88478b502dbef6dd2"


@pytest.fixture(scope="session")
def registry():
    return {
        "connections": [],
        "integrations": [],
        "run_id": None,
        "notification": None,
    }
