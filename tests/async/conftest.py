import sys
from os import getenv

import pytest

import anaplan_sdk


@pytest.fixture(scope="session")
def client():
    return anaplan_sdk.AsyncClient(
        workspace_id=getenv("ANAPLAN_SDK_TEST_WORKSPACE_ID"),
        model_id=getenv("ANAPLAN_SDK_TEST_MODEL_ID"),
        certificate=getenv("ANAPLAN_SDK_TEST_CERT"),
        private_key=getenv("ANAPLAN_SDK_TEST_PK"),
        retry_count=3,
    )


@pytest.fixture(scope="session")
def broken_client():
    return anaplan_sdk.AsyncClient(
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
