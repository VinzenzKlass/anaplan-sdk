import warnings
from concurrent.futures import ThreadPoolExecutor
from itertools import chain
from typing import Any

import httpx

from anaplan_sdk._base import _BaseClient
from anaplan_sdk.models import (
    InsertionResult,
    LineItem,
    List,
    ListItem,
    ListMetadata,
    ModelStatus,
    Module,
)


class _TransactionalClient(_BaseClient):
    def __init__(self, client: httpx.Client, model_id: str, retry_count: int) -> None:
        self._client = client
        self._url = f"https://api.anaplan.com/2/0/models/{model_id}"
        super().__init__(retry_count, client)

    def list_modules(self) -> list[Module]:
        """
        Lists all the Modules in the Model.
        :return: The List of Modules.
        """
        return [Module.model_validate(e) for e in self._get(f"{self._url}/modules").get("modules")]

    def get_model_status(self) -> ModelStatus:
        """
        Gets the current status of the Model.
        :return: The current status of the Mode.
        """
        return ModelStatus.model_validate(self._get(f"{self._url}/status").get("requestStatus"))

    def list_line_items(self, only_module_id: int | None = None) -> list[LineItem]:
        """
        Lists all the Line Items in the Model.
        :param only_module_id: If provided, only Line Items from this Module will be returned.
        :return: The List of Line Items.
        """
        url = (
            f"{self._url}/modules/{only_module_id}/lineItems?includeAll=true"
            if only_module_id
            else f"{self._url}/lineItems?includeAll=true"
        )
        return [LineItem.model_validate(e) for e in self._get(url).get("items")]

    def list_lists(self) -> list[List]:
        """
        Lists all the Lists in the Model.
        :return: All Lists on this Model.
        """
        return [List.model_validate(e) for e in self._get(f"{self._url}/lists").get("lists")]

    def get_list_metadata(self, list_id: int) -> ListMetadata:
        """
        Gets the metadata for a List.
        :param list_id: The ID of the List.
        :return: The Metadata for the List.
        """
        return ListMetadata.model_validate(
            self._get(f"{self._url}/lists/{list_id}").get("metadata")
        )

    def get_list_items(self, list_id: int) -> list[ListItem]:
        """
        Gets all the items in a List.
        :param list_id: The ID of the List.
        :return: The List of Items.
        """
        return [
            ListItem.model_validate(e)
            for e in self._get(f"{self._url}/lists/{list_id}/items?includeAll=true").get(
                "listItems"
            )
        ]

    def insert_list_items(
        self, list_id: int, items: list[dict[str, str | int | dict]]
    ) -> InsertionResult:
        """
        Insert new items to the given list. The items must be a list of dictionaries with at least
        the keys `code` and `name`. You can optionally pass further keys for parents, extra
        properties etc.
        :param list_id: The ID of the List.
        :param items: The items to insert into the List.
        :return: The result of the insertion, indicating how many items were added,
                 ignored or failed.
        """
        if len(items) <= 100_000:
            return InsertionResult.model_validate(
                self._post(f"{self._url}/lists/{list_id}/items?action=add", json={"items": items})
            )

        with ThreadPoolExecutor() as executor:
            responses = list(
                executor.map(
                    lambda chunk: self._post(
                        f"{self._url}/lists/{list_id}/items?action=add", json={"items": chunk}
                    ),
                    [items[i : i + 100_000] for i in range(0, len(items), 100_000)],
                )
            )

        failures, added, ignored, total = [], 0, 0, 0
        for res in responses:
            failures.append(res.get("failures", []))
            added += res.get("added", 0)
            total += res.get("total", 0)
            ignored += res.get("ignored", 0)

        return InsertionResult(
            added=added, ignored=ignored, total=total, failures=list(chain.from_iterable(failures))
        )

    def delete_list_items(self, list_id: int, items: list[dict[str, str | int]]) -> int:
        """
        Deletes items from a List.
        :param list_id: The ID of the List.
        :param items: The items to delete from the List. Must be a dict with either `code` or `id`
                      as the keys to identify the records to delete.
        """
        if len(items) <= 100_000:
            return self._post(
                f"{self._url}/lists/{list_id}/items?action=delete", json={"items": items}
            ).get("deleted", 0)

        with ThreadPoolExecutor() as executor:
            responses = list(
                executor.map(
                    lambda chunk: self._post(
                        f"{self._url}/lists/{list_id}/items?action=delete", json={"items": chunk}
                    ),
                    [items[i : i + 100_000] for i in range(0, len(items), 100_000)],
                )
            )

        return sum(res.get("deleted", 0) for res in responses)

    def reset_list_index(self, list_id: int) -> None:
        """
        Resets the index of a List. The List must be empty to do so.
        :param list_id: The ID of the List.
        """
        self._post_empty(f"{self._url}/lists/{list_id}/resetIndex")

    def write_to_module(self, module_id: int, data: list[dict[str, Any]]) -> int | dict[str, Any]:
        """
        Write the passed items to the specified module. If successful, the number of cells changed
        is returned, if only partially successful or unsuccessful, the response with the according
        details is returned instead. For more details,
        see: https://anaplan.docs.apiary.io/#UpdateModuleCellData.
        :param module_id: The ID of the Module.
        :param data: The data to write to the Module.
        :return: The number of cells changed or the response with the according error details.
        """
        res = self._post(f"{self._url}/modules/{module_id}/data", json=data)
        return res if "failures" in res else res["numberOfCellsChanged"]

    def add_items_to_list(
        self, list_id: int, items: list[dict[str, str | int | dict]]
    ) -> InsertionResult:
        warnings.warn(
            "`add_items_to_list()` is deprecated and will be removed in a future version. "
            "Use `insert_list_items()` instead.",
            DeprecationWarning,
            stacklevel=1,
        )
        return self.insert_list_items(list_id, items)
