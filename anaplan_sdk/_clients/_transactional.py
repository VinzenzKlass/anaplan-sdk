import logging
from concurrent.futures import ThreadPoolExecutor
from itertools import chain
from typing import Any, Literal, overload

from anaplan_sdk._services import _HttpService
from anaplan_sdk._utils import (
    parse_calendar_response,
    parse_insertion_response,
    sort_params,
    validate_dimension_id,
)
from anaplan_sdk.exceptions import InvalidIdentifierException
from anaplan_sdk.models import (
    CurrentPeriod,
    Dimension,
    DimensionWithCode,
    FiscalYear,
    InsertionResult,
    LineItem,
    List,
    ListDeletionResult,
    ListItem,
    ListMetadata,
    Model,
    ModelCalendar,
    ModelStatus,
    Module,
    View,
    ViewInfo,
)

SortBy = Literal["id", "name"] | None

logger = logging.getLogger("anaplan_sdk")


class _TransactionalClient:
    def __init__(self, http: _HttpService, model_id: str) -> None:
        self._http = http
        self._url = f"https://api.anaplan.com/2/0/models/{model_id}"
        self._model_id = model_id

    def get_model_details(self) -> Model:
        """
        Retrieves the Model details for the current Model.
        :return: The Model details.
        """
        return Model.model_validate(
            self._http.get(self._url, params={"modelDetails": "true"})["model"]
        )

    def get_model_status(self) -> ModelStatus:
        """
        Gets the current status of the Model.
        :return: The current status of the Mode.
        """
        return ModelStatus.model_validate(
            self._http.get(f"{self._url}/status").get("requestStatus")
        )

    def wake_model(self) -> None:
        """Wake up the current model."""
        self._http.post_empty(f"{self._url}/open", headers={"Content-Type": "application/text"})
        logger.info(f"Woke up model '{self._model_id}'.")

    def close_model(self) -> None:
        """Close the current model."""
        self._http.post_empty(f"{self._url}/close", headers={"Content-Type": "application/text"})
        logger.info(f"Closed model '{self._model_id}'.")

    def get_modules(self, sort_by: SortBy = None, descending: bool = False) -> list[Module]:
        """
        Lists all the Modules in the Model.
        :param sort_by: The field to sort the results by.
        :param descending: If True, the results will be sorted in descending order.
        :return: The List of Modules.
        """
        res = self._http.get_paginated(
            f"{self._url}/modules", "modules", params=sort_params(sort_by, descending)
        )
        return [Module.model_validate(e) for e in res]

    def get_views(
        self, sort_by: Literal["id", "module_id", "name"] | None = None, descending: bool = False
    ) -> list[View]:
        """
        Lists all the Views in the Model. This will include all Modules and potentially other saved
        views.
        :param sort_by: The field to sort the results by.
        :param descending: If True, the results will be sorted in descending order.
        :return: The List of Views.
        """
        params = {"includesubsidiaryviews": True} | sort_params(sort_by, descending)
        return [
            View.model_validate(e)
            for e in self._http.get_paginated(f"{self._url}/views", "views", params=params)
        ]

    def get_view_info(self, view_id: int) -> ViewInfo:
        """
        Gets the detailed information about a View.
        :param view_id: The ID of the View.
        :return: The information about the View.
        """
        return ViewInfo.model_validate(self._http.get(f"{self._url}/views/{view_id}"))

    def get_line_items(self, only_module_id: int | None = None) -> list[LineItem]:
        """
        Lists all the Line Items in the Model.
        :param only_module_id: If provided, only Line Items from this Module will be returned.
        :return: All Line Items on this Model or only from the specified Module.
        """
        url = (
            f"{self._url}/modules/{only_module_id}/lineItems?includeAll=true"
            if only_module_id
            else f"{self._url}/lineItems?includeAll=true"
        )
        return [LineItem.model_validate(e) for e in self._http.get(url).get("items", [])]

    def get_lists(self, sort_by: SortBy = None, descending: bool = False) -> list[List]:
        """
        Lists all the Lists in the Model.
        :param sort_by: The field to sort the results by.
        :param descending: If True, the results will be sorted in descending order.
        :return: All Lists on this model.
        """
        res = self._http.get_paginated(
            f"{self._url}/lists", "lists", params=sort_params(sort_by, descending)
        )
        return [List.model_validate(e) for e in res]

    def get_list_metadata(self, list_id: int) -> ListMetadata:
        """
        Gets the metadata for a List.
        :param list_id: The ID of the List.
        :return: The Metadata for the List.
        """
        return ListMetadata.model_validate(
            self._http.get(f"{self._url}/lists/{list_id}").get("metadata")
        )

    @overload
    def get_list_items(
        self, list_id: int, return_raw: Literal[False] = False
    ) -> list[ListItem]: ...

    @overload
    def get_list_items(
        self, list_id: int, return_raw: Literal[True] = True
    ) -> list[dict[str, Any]]: ...

    def get_list_items(
        self, list_id: int, return_raw: bool = False
    ) -> list[ListItem] | list[dict[str, Any]]:
        """
        Gets all the items in a List.
        :param list_id: The ID of the List.
        :param return_raw: If True, returns the items as a list of dictionaries instead of ListItem
               objects. If you use the result of this call in a DataFrame or you simply pass on the
               data, you will want to set this to avoid unnecessary (de-)serialization.
        :return: All items in the List.
        """
        res = self._http.get(f"{self._url}/lists/{list_id}/items?includeAll=true")
        if return_raw:
            return res.get("listItems", [])
        return [ListItem.model_validate(e) for e in res.get("listItems", [])]

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
        if not items:
            return InsertionResult(added=0, ignored=0, failures=[], total=0)
        if len(items) <= 100_000:
            result = InsertionResult.model_validate(
                self._http.post(
                    f"{self._url}/lists/{list_id}/items?action=add", json={"items": items}
                )
            )
            logger.info(f"Inserted {result.added} items into list '{list_id}'.")
            return result

        with ThreadPoolExecutor() as executor:
            responses = list(
                executor.map(
                    lambda chunk: self._http.post(
                        f"{self._url}/lists/{list_id}/items?action=add", json={"items": chunk}
                    ),
                    [items[i : i + 100_000] for i in range(0, len(items), 100_000)],
                )
            )
        result = parse_insertion_response(responses)
        logger.info(f"Inserted {result.added} items into list '{list_id}'.")
        return result

    def delete_list_items(
        self, list_id: int, items: list[dict[str, str | int]]
    ) -> ListDeletionResult:
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
                      as the keys to identify the records to delete. Specifying both will error.
        :return: The result of the deletion, indicating how many items were deleted or failed.
        """
        if not items:
            return ListDeletionResult(deleted=0, failures=[])
        if len(items) <= 100_000:
            res = self._http.post(
                f"{self._url}/lists/{list_id}/items?action=delete", json={"items": items}
            )
            info = ListDeletionResult.model_validate(res)
            logger.info(f"Deleted {info.deleted} items from list '{list_id}'.")
            return info

        with ThreadPoolExecutor() as executor:
            responses = list(
                executor.map(
                    lambda chunk: self._http.post(
                        f"{self._url}/lists/{list_id}/items?action=delete", json={"items": chunk}
                    ),
                    [items[i : i + 100_000] for i in range(0, len(items), 100_000)],
                )
            )
        info = ListDeletionResult(
            deleted=sum(res.get("deleted", 0) for res in responses),
            failures=list(chain.from_iterable(res.get("failures", []) for res in responses)),
        )
        logger.info(f"Deleted {info} items from list '{list_id}'.")
        return info

    def reset_list_index(self, list_id: int) -> None:
        """
        Resets the index of a List. The List must be empty to do so.
        :param list_id: The ID of the List.
        """
        self._http.post_empty(f"{self._url}/lists/{list_id}/resetIndex")
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
        res = self._http.post(f"{self._url}/modules/{module_id}/data", json=data)
        if "failures" not in res:
            logger.info(f"Updated {res['numberOfCellsChanged']} cells in module '{module_id}'.")
        return res if "failures" in res else res["numberOfCellsChanged"]

    def get_current_period(self) -> CurrentPeriod:
        """
        Gets the current period of the model.
        :return: The current period of the model.
        """
        res = self._http.get(f"{self._url}/currentPeriod")
        return CurrentPeriod.model_validate(res["currentPeriod"])

    def set_current_period(self, date: str) -> CurrentPeriod:
        """
        Sets the current period of the model to the given date.
        :param date: The date to set the current period to, in the format 'YYYY-MM-DD'.
        :return: The updated current period of the model.
        """
        res = self._http.put(f"{self._url}/currentPeriod", {"date": date})
        logger.info(f"Set current period to '{date}'.")
        return CurrentPeriod.model_validate(res["currentPeriod"])

    def set_current_fiscal_year(self, year: str) -> FiscalYear:
        """
        Sets the current fiscal year of the model.
        :param year: The fiscal year to set, in the format specified in the model, e.g. FY24.
        :return: The updated fiscal year of the model.
        """
        res = self._http.put(f"{self._url}/modelCalendar/fiscalYear", {"year": year})
        logger.info(f"Set current fiscal year to '{year}'.")
        return FiscalYear.model_validate(res["modelCalendar"]["fiscalYear"])

    def get_model_calendar(self) -> ModelCalendar:
        """
        Get the calendar settings of the model.
        :return: The calendar settings of the model.
        """
        return parse_calendar_response(self._http.get(f"{self._url}/modelCalendar"))

    def get_dimension_items(self, dimension_id: int) -> list[DimensionWithCode]:
        """
        Get all items in a dimension. This will fail if the dimensions holds more than 1_000_000
        items. Valid Dimensions are:

        - Lists (101xxxxxxxxx)
        - List Subsets (109xxxxxxxxx)
        - Line Item Subsets (114xxxxxxxxx)
        - Users (101999999999)
        For lists and users, you should prefer using the `get_list_items` and `get_users` methods,
        respectively, instead.
        :param dimension_id: The ID of the dimension to list items for.
        :return: A list of Dimension items.
        """
        res = self._http.get(f"{self._url}/dimensions/{validate_dimension_id(dimension_id)}/items")
        return [DimensionWithCode.model_validate(e) for e in res.get("items", [])]

    def lookup_dimension_items(
        self, dimension_id: int, codes: list[str] = None, names: list[str] = None
    ) -> list[DimensionWithCode]:
        """
        Looks up items in a dimension by their codes or names. If both are provided, both will be
        searched for. You must provide at least one of `codes` or `names`. Valid Dimensions to
        lookup are:

        - Lists (101xxxxxxxxx)
        - Time (20000000003)
        - Version (20000000020)
        - Users (101999999999)
        :param dimension_id: The ID of the dimension to lookup items for.
        :param codes: A list of codes to lookup in the dimension.
        :param names: A list of names to lookup in the dimension.
        :return: A list of Dimension items that match the provided codes or names.
        """
        if not codes and not names:
            raise ValueError("At least one of 'codes' or 'names' must be provided.")
        if not (
            dimension_id == 101999999999
            or 101000000000 <= dimension_id < 102000000000
            or dimension_id == 20000000003
            or dimension_id == 20000000020
        ):
            raise InvalidIdentifierException(
                "Invalid dimension_id. Must be a List (101xxxxxxxxx), Time (20000000003), "
                "Version (20000000020), or Users (101999999999)."
            )
        res = self._http.post(
            f"{self._url}/dimensions/{dimension_id}/items", json={"codes": codes, "names": names}
        )
        return [DimensionWithCode.model_validate(e) for e in res.get("items", [])]

    def get_view_dimension_items(self, view_id: int, dimension_id: int) -> list[Dimension]:
        """
        Get the members of a dimension that are part of the given View. This call returns data as
        filtered by the page builder when they configure the view. This call respects hidden items,
        filtering selections, and Selective Access. If the view contains hidden or filtered items,
        these do not display in the response. This will fail if the dimensions holds more than
        1_000_000 items. The response returns Items within a flat list (no hierarchy) and order
        is not guaranteed.
        :param view_id: The ID of the View.
        :param dimension_id: The ID of the Dimension to get items for.
        :return: A list of Dimensions used in the View.
        """
        res = self._http.get(f"{self._url}/views/{view_id}/dimensions/{dimension_id}/items")
        return [Dimension.model_validate(e) for e in res.get("items", [])]

    def get_line_item_dimensions(self, line_item_id: int) -> list[Dimension]:
        """
        Get the dimensions of a Line Item. This will return all dimensions that are used in the
        Line Item.
        :param line_item_id: The ID of the Line Item.
        :return: A list of Dimensions used in the Line Item.
        """
        res = self._http.get(f"{self._url}/lineItems/{line_item_id}/dimensions")
        return [Dimension.model_validate(e) for e in res.get("dimensions", [])]
