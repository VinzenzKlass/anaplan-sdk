import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Any

import httpx

from anaplan_sdk._base import _BaseClient, parse_calendar_response, parse_insertion_response
from anaplan_sdk.models import (
    CurrentPeriod,
    FiscalYear,
    InsertionResult,
    LineItem,
    List,
    ListItem,
    ListMetadata,
    Model,
    ModelCalendar,
    ModelStatus,
    Module,
    View,
    ViewInfo,
)

logger = logging.getLogger("anaplan_sdk")


class _TransactionalClient(_BaseClient):
    def __init__(self, client: httpx.Client, model_id: str, retry_count: int) -> None:
        self._url = f"https://api.anaplan.com/2/0/models/{model_id}"
        self._model_id = model_id
        super().__init__(retry_count, client)

    def get_model_details(self) -> Model:
        """
        Retrieves the Model details for the current Model.
        :return: The Model details.
        """
        return Model.model_validate(self._get(self._url, params={"modelDetails": "true"})["model"])

    def get_model_status(self) -> ModelStatus:
        """
        Gets the current status of the Model.
        :return: The current status of the Mode.
        """
        return ModelStatus.model_validate(self._get(f"{self._url}/status").get("requestStatus"))

    def wake_model(self) -> None:
        """Wake up the current model."""
        self._post_empty(f"{self._url}/open", headers={"Content-Type": "application/text"})
        logger.info(f"Woke up model '{self._model_id}'.")

    def close_model(self) -> None:
        """Close the current model."""
        self._post_empty(f"{self._url}/close", headers={"Content-Type": "application/text"})
        logger.info(f"Closed model '{self._model_id}'.")

    def list_modules(self) -> list[Module]:
        """
        Lists all the Modules in the Model.
        :return: The List of Modules.
        """
        return [
            Module.model_validate(e) for e in self._get_paginated(f"{self._url}/modules", "modules")
        ]

    def list_views(self) -> list[View]:
        """
        Lists all the Views in the Model. This will include all Modules and potentially other saved
        views.
        :return: The List of Views.
        """
        return [View.model_validate(e) for e in self._get_paginated(f"{self._url}/views", "views")]

    def get_view_info(self, view_id: int) -> ViewInfo:
        """
        Gets the detailed information about a View.
        :param view_id: The ID of the View.
        :return: The information about the View.
        """
        return ViewInfo.model_validate(self._get(f"{self._url}/views/{view_id}"))

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
        return [LineItem.model_validate(e) for e in self._get(url).get("items", [])]

    def list_lists(self) -> list[List]:
        """
        Lists all the Lists in the Model.
        :return: All Lists on this model.
        """
        return [List.model_validate(e) for e in self._get_paginated(f"{self._url}/lists", "lists")]

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
                "listItems", []
            )
        ]

    def insert_list_items(
        self, list_id: int, items: list[dict[str, str | int | dict]]
    ) -> InsertionResult:
        """
        Insert new items to the given list. The items must be a list of dictionaries with at least
        the keys `code` and `name`. You can optionally pass further keys for parents, extra
        properties etc. If you pass a long list, it will be split into chunks of 100,000 items, the
        maximum allowed by the API.

        **Warning**: If one or some of the requests timeout during large batch operations, the
        operation may actually complete on the server. Retries for these chunks will then report
        these items as "ignored" rather than "added", leading to misleading results. The results in
        Anaplan will be correct, but this function may report otherwise. Be generous with your
        timeouts and retries if you are using this function for large batch operations.

        :param list_id: The ID of the List.
        :param items: The items to insert into the List.
        :return: The result of the insertion, indicating how many items were added,
                 ignored or failed.
        """
        if len(items) <= 100_000:
            result = InsertionResult.model_validate(
                self._post(f"{self._url}/lists/{list_id}/items?action=add", json={"items": items})
            )
            logger.info(f"Inserted {result.added} items into list '{list_id}'.")
            return result

        with ThreadPoolExecutor() as executor:
            responses = list(
                executor.map(
                    lambda chunk: self._post(
                        f"{self._url}/lists/{list_id}/items?action=add", json={"items": chunk}
                    ),
                    [items[i : i + 100_000] for i in range(0, len(items), 100_000)],
                )
            )
        result = parse_insertion_response(responses)
        logger.info(f"Inserted {result.added} items into list '{list_id}'.")
        return result

    def delete_list_items(self, list_id: int, items: list[dict[str, str | int]]) -> int:
        """
        Deletes items from a List. If you pass a long list, it will be split into chunks of 100,000
        items, the maximum allowed by the API.

        **Warning**: If one or some of the requests timeout during large batch operations, the
        operation may actually complete on the server. Retries for these chunks will then report
        none of these items as deleted, since on the retry none are removed, leading to misleading
        results. The results in Anaplan will be correct, but this function may report otherwise.
        Be generous with your timeouts and retries if you are using this function for large batch
        operations.

        :param list_id: The ID of the List.
        :param items: The items to delete from the List. Must be a dict with either `code` or `id`
                      as the keys to identify the records to delete.
        """
        if len(items) <= 100_000:
            deleted_count = self._post(
                f"{self._url}/lists/{list_id}/items?action=delete", json={"items": items}
            ).get("deleted", 0)
            logger.info(f"Deleted {deleted_count} items from list '{list_id}'.")
            return deleted_count

        with ThreadPoolExecutor() as executor:
            responses = list(
                executor.map(
                    lambda chunk: self._post(
                        f"{self._url}/lists/{list_id}/items?action=delete", json={"items": chunk}
                    ),
                    [items[i : i + 100_000] for i in range(0, len(items), 100_000)],
                )
            )

        deleted_count = sum(res.get("deleted", 0) for res in responses)
        logger.info(f"Deleted {deleted_count} items from list '{list_id}'.")
        return deleted_count

    def reset_list_index(self, list_id: int) -> None:
        """
        Resets the index of a List. The List must be empty to do so.
        :param list_id: The ID of the List.
        """
        self._post_empty(f"{self._url}/lists/{list_id}/resetIndex")
        logger.info(f"Reset index for list '{list_id}'.")

    def update_module_data(
        self, module_id: int, data: list[dict[str, Any]]
    ) -> int | dict[str, Any]:
        """
        Write the passed items to the specified module. If successful, the number of cells changed
        is returned, if only partially successful or unsuccessful, the response with the according
        details is returned instead.

        **You can update a maximum of 100,000 cells or 15 MB of data (whichever is lower) in a
        single request.** You must chunk your data accordingly. This is not done by this SDK,
        since it is discouraged. For larger imports, you should use the Bulk API instead.

        For more details see: https://anaplan.docs.apiary.io/#UpdateModuleCellData.
        :param module_id: The ID of the Module.
        :param data: The data to write to the Module.
        :return: The number of cells changed or the response with the according error details.
        """
        res = self._post(f"{self._url}/modules/{module_id}/data", json=data)
        if "failures" not in res:
            logger.info(f"Updated {res['numberOfCellsChanged']} cells in module '{module_id}'.")
        return res if "failures" in res else res["numberOfCellsChanged"]

    def get_current_period(self) -> CurrentPeriod:
        """
        Gets the current period of the model.
        :return: The current period of the model.
        """
        res = self._get(f"{self._url}/currentPeriod")
        return CurrentPeriod.model_validate(res["currentPeriod"])

    def set_current_period(self, date: str) -> CurrentPeriod:
        """
        Sets the current period of the model to the given date.
        :param date: The date to set the current period to, in the format 'YYYY-MM-DD'.
        :return: The updated current period of the model.
        """
        res = self._put(f"{self._url}/currentPeriod", {"date": date})
        logger.info(f"Set current period to '{date}'.")
        return CurrentPeriod.model_validate(res["currentPeriod"])

    def set_current_fiscal_year(self, year: str) -> FiscalYear:
        """
        Sets the current fiscal year of the model.
        :param year: The fiscal year to set, in the format specified in the model, e.g. FY24.
        :return: The updated fiscal year of the model.
        """
        res = self._put(f"{self._url}/modelCalendar/fiscalYear", {"year": year})
        logger.info(f"Set current fiscal year to '{year}'.")
        return FiscalYear.model_validate(res["modelCalendar"]["fiscalYear"])

    def get_model_calendar(self) -> ModelCalendar:
        """
        Get the calendar settings of the model.
        :return: The calendar settings of the model.
        """
        return parse_calendar_response(self._get(f"{self._url}/modelCalendar"))
