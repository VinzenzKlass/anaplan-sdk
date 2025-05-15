If you need to go beyond the standard flows of importing and exporting data to and from Anaplan, you likely will need
some functionality of the Transactional APIs. The Transactional APIs can provide a lot of Information about the Model,
the data that resides in the model, ongoing Tasks etc. You can also use them to insert data directly into Lists and
Modules or read data from Lists and Modules. Whenever the need to do so arises, always consider if the same could be
achieved using the Bulk API first.

## Accessing the Namespace

All the methods for the Transactional APIs reside in a different namespace for better API navigability and
comprehensiveness, but are accessible through the same client for convenience. For e.g., you can call
the `.list_lists()` method like so:

=== "Synchronous"
    ```python
    import anaplan_sdk
    
    anaplan = anaplan_sdk.Client(
        workspace_id="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
        model_id="11111111111111111111111111111111",
        certificate="~/certs/anaplan.pem",
        private_key="~/keys/anaplan.pem",
    )
    lists = anaplan.transactional.list_lists()
    ```
=== "Asynchronous"
    ```python
    import anaplan_sdk
    
    anaplan = anaplan_sdk.AsyncClient(
        workspace_id="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
        model_id="11111111111111111111111111111111",
        certificate="~/certs/anaplan.pem",
        private_key="~/keys/anaplan.pem",
    )
    lists = await anaplan.transactional.list_lists()
    ```

For brevity, if you need to access only the Transactional API or need to do so repeatedly, you can assign the
Transactional Client to its own variable.

=== "Synchronous"
    ```python
    anaplan = anaplan_sdk.Client(
        workspace_id="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
        model_id="11111111111111111111111111111111",
        certificate="~/certs/anaplan.pem",
        private_key="~/keys/anaplan.pem",
    )
    trans_anaplan = anaplan.transactional
    lists = trans_anaplan.list_lists()
    modules = trans_anaplan.list_modules()
    ```
=== "Asynchronous"
    ```python
    anaplan = anaplan_sdk.AsyncClient(
        workspace_id="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
        model_id="11111111111111111111111111111111",
        certificate="~/certs/anaplan.pem",
        private_key="~/keys/anaplan.pem",
    )
    trans_anaplan = anaplan.transactional
    lists, modules = await gather(
       trans_anaplan.list_lists(), trans_anaplan.list_modules()
    )
    ```

???+ note
    While you can instantiate a [Client](../api/sync/sync_client.md) without the workspace or model parameters, trying to access
    the [Transactional Client](../api/sync/sync_transactional_client.md) on an instance without the `model_id` will raise a `ValueError`.

## Basic Usage

### Read List Items

=== "Synchronous"
    ```python
    products = anaplan.transactional.get_list_items(101000000299)
    ```
=== "Asynchronous"
    ```python
    products = await anaplan.transactional.get_list_items(101000000299)
    ```

### Insert new List Items

These dicts must at least hold `code` or `id`and the name.

=== "Synchronous"
    ```python
    anaplan.transactional.insert_list_items(
        101000000299,
        [
            {"code": "A", "name": "A"},
            {"code": "B", "name": "B"},
            {"code": "C", "name": "C"},
            {"code": "D", "name": "D"},
        ],
    )
    ```
=== "Asynchronous"
    ```python
    await anaplan.transactional.insert_list_items(
        101000000299,
        [
            {"code": "A", "name": "A"},
            {"code": "B", "name": "B"},
            {"code": "C", "name": "C"},
            {"code": "D", "name": "D"},
        ],
    )
    ```

### Update Module Data

You can manipulate individual cells in a module using the `update_module_data` method. This method takes a list of
dictionaries, each specifying the "coordinates" as a combination of the module to write to, the line item to update and
the list of dimensions. The combination of these three will uniquely identify the cell to be updated. The value to be
written is specified in the `value` key of the dictionary. The Line Items and Dimensions can be specified by either
their `id` or `name`. The `value` can be a string, number or boolean.

=== "Synchronous"
    ```python
    anaplan.transactional.update_module_data(
        101000000299,
        [
            {
                "lineItemName": "Products",
                "dimensions": [
                    {"dimensionName": "Product", "itemCode": "18"},
                    {"dimensionName": "Time", "itemName": "Jan 21"},
                ],
                "value": 1000,
            },
            {
                "lineItemName": "Sales",
                "dimensions": [
                    {"dimensionName": "Region", "itemName": "Uganda"},
                    {"dimensionName": "Time", "itemName": "Jan 21"},
                ],
                "value": 1000,
            },
        ],
    )
    ```
=== "Asynchronous"
    ```python
    await anaplan.transactional.update_module_data(
        101000000299,
        [
            {
                "lineItemName": "Products",
                "dimensions": [
                    {"dimensionName": "Product", "itemCode": "18"},
                    {"dimensionName": "Time", "itemName": "Jan 21"},
                ],
                "value": 1000,
            },
            {
                "lineItemName": "Sales",
                "dimensions": [
                    {"dimensionName": "Region", "itemName": "Uganda"},
                    {"dimensionName": "Time", "itemName": "Jan 21"},
                ],
                "value": 1000,
            },
        ],
    )
    ```

## Applications

### Resetting List Index w/o data loss

Lists holding large sets of transactional data that are frequently updated, will often produce a `List index limit`
Warning. To automate this tedious task without losing any data, we can perform four simple steps:

1. Export the list data and either hold it in memory or save it.
2. Purge the list. This is necessary so the List Index can be reset. Attempting to reset the Index of a non-empty List
   will result in an error.
3. Reset the List Index.
4. Reimport the Data from Step one.

=== "Synchronous"
    ```python
    items = anaplan.transactional.get_list_items(101000000000)
    anaplan.transactional.delete_list_items(
        101000000000, [{"id": e.id} for e in items]
    )
    anaplan.transactional.reset_list_index(101000000000)
    result = anaplan.transactional.insert_list_items(
        101000000008, [e.model_dump() for e in items] # Reimport all fields.
    )
    ```
=== "Asynchronous"
    ```python
    items = await anaplan.transactional.get_list_items(101000000000)
    await anaplan.transactional.delete_list_items(
        101000000000, [{"id": e.id} for e in items]
    )
    await anaplan.transactional.reset_list_index(101000000000)
    result = await anaplan.transactional.insert_list_items(
        101000000008, [e.model_dump() for e in items] # Reimport all fields. 
    )
    ```
