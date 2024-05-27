import logging

logger = logging.getLogger("anaplan_sdk")


class AsyncClient:
    def __init__(self, workspace_id: str, model_id: str):
        ...
