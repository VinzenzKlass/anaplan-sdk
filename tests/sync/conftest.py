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
        return "21a23d6831d245d9bc853b3524859079"
    if "3.11" in py_version:
        return "5fa07479c0bf4fb984caa15e44fb6154"
    if "3.12" in py_version:
        return "aa6a18a8f2f1437eb0ea23defb23b1ff"
    return "6a36d7ea069a400a8e634d19d83a8dfe"


@pytest.fixture(scope="session")
def test_notification():
    py_version = sys.version.split(" ")[0]
    if "3.10" in py_version:
        return "3c685465471e4b19ac10b65b01b96aa9"
    if "3.11" in py_version:
        return "63c259ce444d4989b0b648bd3526713f"
    if "3.12" in py_version:
        return "ebc03ce9e50148d6831b339250e89bc2"
    return "5a87a2fcb59f4d15962f81ec53c8b1dc"


@pytest.fixture(scope="session")
def registry():
    return {"connections": [], "integrations": [], "run_id": None}
