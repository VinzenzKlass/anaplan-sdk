If you need to go beyond the standard flows of importing and exporting data to and from Anaplan, you likely will need some functionality of the Transactional APIs. The Transactional APIs can provide a lot of Information about the Model, the data that resides in the model, ongoing Tasks etc. You can also use them to insert data directly into Lists and Modules or read data from Lists and Modules.

## Accessing the Namespace

All the methods for the Transactional APIs reside in a different namespace for better API navigability and comprehensiveness, but are accessible through the same client for convenience. For e.g., you can call the `.get_lists()` method like so:

```
import anaplan_sdk

anaplan = anaplan_sdk.Client(
    workspace_id="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    model_id="11111111111111111111111111111111",
    certificate="~/certs/anaplan.pem",
    private_key="~/keys/anaplan.pem",
)
lists = anaplan.tr.get_lists()
```

```
import anaplan_sdk

anaplan = anaplan_sdk.AsyncClient(
    workspace_id="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    model_id="11111111111111111111111111111111",
    certificate="~/certs/anaplan.pem",
    private_key="~/keys/anaplan.pem",
)
lists = await anaplan.tr.get_lists()
```

Note

While you can instantiate a [Client](https://vinzenzklass.github.io/anaplan-sdk/api/sync/sync_client/index.md) without the workspace or model parameters, trying to access the [Transactional Client](https://vinzenzklass.github.io/anaplan-sdk/api/sync/sync_transactional_client/index.md) on an instance without the `model_id` will raise a `ValueError`.

## Basic Usage

### Read List Items

```
products = anaplan.tr.get_list_items(101000000299)
```

```
products = await anaplan.tr.get_list_items(101000000299)
```

### Insert new List Items

These dicts must at least hold `code` or `id`and the name.

```
anaplan.tr.insert_list_items(
    101000000299,
    [
        {"code": "A", "name": "A"},
        {"code": "B", "name": "B"},
        {"code": "C", "name": "C"},
        {"code": "D", "name": "D"},
    ],
)
```

```
await anaplan.tr.insert_list_items(
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

You can manipulate individual cells in a module using the `update_module_data` method. This method takes a list of dictionaries, each specifying the "coordinates" as a combination of the module to write to, the line item to update and the list of dimensions. The combination of these three will uniquely identify the cell to be updated. The value to be written is specified in the `value` key of the dictionary. The Line Items and Dimensions can be specified by either their `id` or `name`. The `value` can be a string, number or boolean.

```
anaplan.tr.update_module_data(
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

```
await anaplan.tr.update_module_data(
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

Lists holding large sets of tr data that are frequently updated, will often produce a `List index limit` Warning. To automate this tedious task without losing any data, we can perform four simple steps:

1. Export the list data and either hold it in memory or save it.
1. Purge the list. This is necessary so the List Index can be reset. Attempting to reset the Index of a non-empty List will result in an error.
1. Reset the List Index.
1. Reimport the Data from Step one.

```
def reset_list_index(list_id: int) -> None:
    items = anaplan.tr.get_list_items(list_id, return_raw=True)
    for item in items:
        del item["id"]  # Specifying both "id" and "code" will cause an error.
    anaplan.tr.delete_list_items(list_id, items)
    anaplan.tr.reset_list_index(list_id)
    anaplan.tr.insert_list_items(list_id, items)
```

```
async def reset_list_index(list_id: int) -> None:
    items = await anaplan.tr.get_list_items(list_id, return_raw=True)
    for item in items:
        del item["id"]  # Specifying both "id" and "code" will cause an error.
    await anaplan.tr.delete_list_items(list_id, items)
    await anaplan.tr.reset_list_index(list_id)
    await anaplan.tr.insert_list_items(list_id, items)
```
