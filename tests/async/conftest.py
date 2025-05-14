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
def test_notification():
    py_version = sys.version.split(" ")[0]
    if "3.10" in py_version:
        return "a01030cc2b64427a8b2deb06ce7fb75c"
    if "3.11" in py_version:
        return "7d21530daed54603a6dfcd27dfdd55d9"
    if "3.12" in py_version:
        return "20abed8b1a11478393cad6fe58ed6436"
    return "00d305418bfa4e05bd677f630e165269"


@pytest.fixture(scope="session")
def test_flow():
    py_version = sys.version.split(" ")[0]
    if "3.10" in py_version:
        return "af21d6cf4ba547b4a28923e152e3b963"
    if "3.11" in py_version:
        return "4110523f770941deb63033ca5557735d"
    if "3.12" in py_version:
        return "be0c54753f9b4427a676fb9b7b4896cd"
    return "66d8614664cb490e869684e56796a6a8"


@pytest.fixture(scope="session")
def registry():
    return {"connections": [], "integrations": [], "flows": [], "run_id": None}
