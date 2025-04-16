import logging

import pytest

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("anaplan_sdk").setLevel(logging.INFO)


@pytest.fixture(scope="session")
def list_items_long():
    return [{"name": i, "code": i} for i in range(200_000)]  # Force several batches


@pytest.fixture(scope="session")
def list_items_short():
    return [{"name": i, "code": i} for i in range(1_000)]  # Single batch
