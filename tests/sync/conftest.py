import os
import sys
from os import getenv

import pytest

import anaplan_sdk


@pytest.fixture(scope="session")
def client():
    return anaplan_sdk.Client(
        workspace_id=getenv("ANAPLAN_SDK_TEST_WORKSPACE_ID"),
        model_id=getenv("ANAPLAN_SDK_TEST_MODEL_ID"),
        certificate=getenv("ANAPLAN_SDK_TEST_CERT"),
        private_key=getenv("ANAPLAN_SDK_TEST_PK"),
        retry_count=3,
    )


@pytest.fixture(scope="session")
def broken_client():
    return anaplan_sdk.Client(
        workspace_id="random",
        model_id="nonsense",
        certificate=os.getenv("ANAPLAN_SDK_TEST_CERT"),
        private_key=os.getenv("ANAPLAN_SDK_TEST_PK"),
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
