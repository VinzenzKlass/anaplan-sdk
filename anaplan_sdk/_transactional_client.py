import httpx

from ._base import _BaseClient
from .models import ModelStatus, LineItem, List, ListMetadata, ListItem, InsertionResult, Module


class _TransactionalClient(_BaseClient):
    def __init__(self, client: httpx.Client, model_id: str, retry_count: int) -> None:
        self._client = client
        self._url = f"https://api.anaplan.com/2/0/models/{model_id}"
        super().__init__(retry_count, client)

    def list_modules(self) -> list[Module]:
        """
        Lists all the Modules in the Model.
        :return: All Modules on this model as a list of :py:class:`Module`.
        """
        return [Module.model_validate(e) for e in self._get(f"{self._url}/modules").get("modules")]

    def get_model_status(self) -> ModelStatus:
        """
        Gets the current status of the Model.
        :return: The current status of the Model as a :py:class:`ModelStatus`.
        """
        return ModelStatus.model_validate(self._get(f"{self._url}/status").get("requestStatus"))

    def list_line_items(self, only_module_id: int | None = None) -> list[LineItem]:
        """
        Lists all the Line Items in the Model.
        :param only_module_id: If provided, only Line Items from this Module will be returned.
        :return: All Line Items on this model as a list of :py:class:`LineItem`.
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
        :return: All Lists on this model as a list of :py:class:`List`.
        """
        return [List.model_validate(e) for e in self._get(f"{self._url}/lists").get("lists")]

    def get_list_metadata(self, list_id: int) -> ListMetadata:
        """
        Gets the metadata for a List.
        :param list_id: The ID of the List.
        :return: The metadata for the List as a :py:class:`ListMetadata`.
        """
        return ListMetadata.model_validate(
            self._get(f"{self._url}/lists/{list_id}").get("metadata")
        )

    def get_list_items(self, list_id: int) -> list[ListItem]:
        """
        Gets all the items in a List.
        :param list_id: The ID of the List.
        :return: All items in the List as a list of :py:class:`ListItem`.
        """
        return [
            ListItem.model_validate(e)
            for e in self._get(f"{self._url}/lists/{list_id}/items?includeAll=true").get(
                "listItems"
            )
        ]

    def add_items_to_list(
        self, list_id: int, items: list[dict[str, str | dict]]
    ) -> InsertionResult:
        """
        Adds items to a List.
        :param list_id: The ID of the List.
        :param items: The items to add to the List.
        :return: The result of the insertion as an :py:class:`InsertionResult`.
        """
        # TODO: Paginate by 100k records.
        return InsertionResult.model_validate(
            self._post(f"{self._url}/lists/{list_id}/items?action=add", json={"items": items})
        )

    def delete_list_items(self, list_id: int, items: list[dict[str, str | int]]) -> None:
        """
        Deletes items from a List.
        :param list_id: The ID of the List.
        :param items: The items to delete from the List. Must be a dict with either `code` or `id`
                      as the keys to identify the records to delete.
        """
        self._post(f"{self._url}/lists/{list_id}/items?action=delete", json={"items": items})

    def reset_list_index(self, list_id: int) -> None:
        """
        Resets the index of a List. The List must be empty to do so.
        :param list_id: The ID of the List.
        """
        self._post_empty(f"{self._url}/lists/{list_id}/resetIndex")
