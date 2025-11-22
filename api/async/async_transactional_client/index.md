Note

This Class is not meant to be instantiated directly, but rather accessed through the `tr` Property on an instance of [AsyncClient](https://vinzenzklass.github.io/anaplan-sdk/api/async/async_client/index.md). For more details, see the [Guide](https://vinzenzklass.github.io/anaplan-sdk/guides/transactional/index.md).

## get_model_details

```
get_model_details() -> Model
```

Retrieves the Model details for the current Model.

Returns:

| Type    | Description        |
| ------- | ------------------ |
| `Model` | The Model details. |

## get_model_status

```
get_model_status() -> ModelStatus
```

Gets the current status of the Model.

Returns:

| Type          | Description                      |
| ------------- | -------------------------------- |
| `ModelStatus` | The current status of the Model. |

## wake_model

```
wake_model() -> None
```

Wake up the current model.

## close_model

```
close_model() -> None
```

Close the current model.

## get_modules

```
get_modules(sort_by: SortBy = None, descending: bool = False) -> list[Module]
```

Lists all the Modules in the Model.

Parameters:

| Name         | Type     | Description                                              | Default |
| ------------ | -------- | -------------------------------------------------------- | ------- |
| `sort_by`    | `SortBy` | The field to sort the results by.                        | `None`  |
| `descending` | `bool`   | If True, the results will be sorted in descending order. | `False` |

Returns:

| Type           | Description          |
| -------------- | -------------------- |
| `list[Module]` | The List of Modules. |

## get_views

```
get_views(
    sort_by: Literal["id", "module_id", "name"] | None = None,
    descending: bool = False,
) -> list[View]
```

Lists all the Views in the Model. This will include all Modules and potentially other saved views.

Parameters:

| Name         | Type                                 | Description                                              | Default                           |
| ------------ | ------------------------------------ | -------------------------------------------------------- | --------------------------------- |
| `sort_by`    | \`Literal['id', 'module_id', 'name'] | None\`                                                   | The field to sort the results by. |
| `descending` | `bool`                               | If True, the results will be sorted in descending order. | `False`                           |

Returns:

| Type         | Description        |
| ------------ | ------------------ |
| `list[View]` | The List of Views. |

## get_view_info

```
get_view_info(view_id: int) -> ViewInfo
```

Gets the detailed information about a View.

Parameters:

| Name      | Type  | Description         | Default    |
| --------- | ----- | ------------------- | ---------- |
| `view_id` | `int` | The ID of the View. | *required* |

Returns:

| Type       | Description                     |
| ---------- | ------------------------------- |
| `ViewInfo` | The information about the View. |

## get_line_items

```
get_line_items(only_module_id: int | None = None) -> list[LineItem]
```

Lists all the Line Items in the Model.

Parameters:

| Name             | Type  | Description | Default                                                         |
| ---------------- | ----- | ----------- | --------------------------------------------------------------- |
| `only_module_id` | \`int | None\`      | If provided, only Line Items from this Module will be returned. |

Returns:

| Type             | Description                                                     |
| ---------------- | --------------------------------------------------------------- |
| `list[LineItem]` | All Line Items on this Model or only from the specified Module. |

## get_lists

```
get_lists(sort_by: SortBy = None, descending: bool = False) -> list[List]
```

Lists all the Lists in the Model.

Parameters:

| Name         | Type     | Description                                              | Default |
| ------------ | -------- | -------------------------------------------------------- | ------- |
| `sort_by`    | `SortBy` | The field to sort the results by.                        | `None`  |
| `descending` | `bool`   | If True, the results will be sorted in descending order. | `False` |

Returns:

| Type         | Description              |
| ------------ | ------------------------ |
| `list[List]` | All Lists on this model. |

## get_list_metadata

```
get_list_metadata(list_id: int) -> ListMetadata
```

Gets the metadata for a List.

Parameters:

| Name      | Type  | Description         | Default    |
| --------- | ----- | ------------------- | ---------- |
| `list_id` | `int` | The ID of the List. | *required* |

Returns:

| Type           | Description                |
| -------------- | -------------------------- |
| `ListMetadata` | The metadata for the List. |

## get_list_items

```
get_list_items(
    list_id: int, return_raw: Literal[False] = False
) -> list[ListItem]
```

```
get_list_items(
    list_id: int, return_raw: Literal[True] = True
) -> list[dict[str, Any]]
```

```
get_list_items(
    list_id: int, return_raw: bool = False
) -> list[ListItem] | list[dict[str, Any]]
```

Gets all the items in a List.

Parameters:

| Name         | Type   | Description                                                                                                                                                                                                                            | Default    |
| ------------ | ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| `list_id`    | `int`  | The ID of the List.                                                                                                                                                                                                                    | *required* |
| `return_raw` | `bool` | If True, returns the items as a list of dictionaries instead of ListItem objects. If you use the result of this call in a DataFrame or you simply pass on the data, you will want to set this to avoid unnecessary (de-)serialization. | `False`    |

Returns:

| Type             | Description              |
| ---------------- | ------------------------ |
| \`list[ListItem] | list\[dict[str, Any]\]\` |

## insert_list_items

```
insert_list_items(
    list_id: int, items: list[dict[str, str | int | dict[str, Any]]]
) -> InsertionResult
```

Insert new items to the given list. The items must be a list of dictionaries with at least the keys `code` and `name`. You can optionally pass further keys for parents, extra properties etc. If you pass a long list, it will be split into chunks of 100,000 items, the maximum allowed by the API.

**Warning**: If one or some of the requests timeout during large batch operations, the operation may actually complete on the server. Retries for these chunks will then report these items as "ignored" rather than "added", leading to misleading results. The results in Anaplan will be correct, but this function may report otherwise. Be generous with your timeouts and retries if you are using this function for large batch operations.

Parameters:

| Name      | Type                   | Description         | Default              |
| --------- | ---------------------- | ------------------- | -------------------- |
| `list_id` | `int`                  | The ID of the List. | *required*           |
| `items`   | \`list\[dict\[str, str | int                 | dict[str, Any]\]\]\` |

Returns:

| Type              | Description                                                                           |
| ----------------- | ------------------------------------------------------------------------------------- |
| `InsertionResult` | The result of the insertion, indicating how many items were added, ignored or failed. |

## delete_list_items

```
delete_list_items(
    list_id: int, items: list[dict[str, str | int]]
) -> ListDeletionResult
```

Deletes items from a List. If you pass a long list, it will be split into chunks of 100,000 items, the maximum allowed by the API.

**Warning**: If one or some of the requests timeout during large batch operations, the operation may actually complete on the server. Retries for these chunks will then report none of these items as deleted, since on the retry none are removed, leading to misleading results. The results in Anaplan will be correct, but this function may report otherwise. Be generous with your timeouts and retries if you are using this function for large batch operations.

Parameters:

| Name      | Type                   | Description         | Default                                                                                                                                             |
| --------- | ---------------------- | ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `list_id` | `int`                  | The ID of the List. | *required*                                                                                                                                          |
| `items`   | \`list\[dict\[str, str | int\]\]\`           | The items to delete from the List. Must be a dict with either code or id as the keys to identify the records to delete. Specifying both will error. |

Returns:

| Type                 | Description                                                                   |
| -------------------- | ----------------------------------------------------------------------------- |
| `ListDeletionResult` | The result of the deletion, indicating how many items were deleted or failed. |

## reset_list_index

```
reset_list_index(list_id: int) -> None
```

Resets the index of a List. The List must be empty to do so.

Parameters:

| Name      | Type  | Description         | Default    |
| --------- | ----- | ------------------- | ---------- |
| `list_id` | `int` | The ID of the List. | *required* |

## update_module_data

```
update_module_data(
    module_id: int, data: list[dict[str, Any]]
) -> int | dict[str, Any]
```

Write the passed items to the specified module. If successful, the number of cells changed is returned, if only partially successful or unsuccessful, the response with the according details is returned instead.

**You can update a maximum of 100,000 cells or 15 MB of data (whichever is lower) in a single request.** You must chunk your data accordingly. This is not done by this SDK, since it is discouraged. For larger imports, you should use the Bulk API instead.

For more details see: https://anaplan.docs.apiary.io/#UpdateModuleCellData.

Parameters:

| Name        | Type                   | Description                      | Default    |
| ----------- | ---------------------- | -------------------------------- | ---------- |
| `module_id` | `int`                  | The ID of the Module.            | *required* |
| `data`      | `list[dict[str, Any]]` | The data to write to the Module. | *required* |

Returns:

| Type  | Description      |
| ----- | ---------------- |
| \`int | dict[str, Any]\` |

## get_current_period

```
get_current_period() -> CurrentPeriod
```

Gets the current period of the model.

Returns:

| Type            | Description                      |
| --------------- | -------------------------------- |
| `CurrentPeriod` | The current period of the model. |

## set_current_period

```
set_current_period(date: str) -> CurrentPeriod
```

Sets the current period of the model to the given date.

Parameters:

| Name   | Type  | Description                                                        | Default    |
| ------ | ----- | ------------------------------------------------------------------ | ---------- |
| `date` | `str` | The date to set the current period to, in the format 'YYYY-MM-DD'. | *required* |

Returns:

| Type            | Description                              |
| --------------- | ---------------------------------------- |
| `CurrentPeriod` | The updated current period of the model. |

## set_current_fiscal_year

```
set_current_fiscal_year(year: str) -> FiscalYear
```

Sets the current fiscal year of the model.

Parameters:

| Name   | Type  | Description                                                              | Default    |
| ------ | ----- | ------------------------------------------------------------------------ | ---------- |
| `year` | `str` | The fiscal year to set, in the format specified in the model, e.g. FY24. | *required* |

Returns:

| Type         | Description                           |
| ------------ | ------------------------------------- |
| `FiscalYear` | The updated fiscal year of the model. |

## get_model_calendar

```
get_model_calendar() -> ModelCalendar
```

Get the calendar settings of the model.

Returns:

| Type            | Description                         |
| --------------- | ----------------------------------- |
| `ModelCalendar` | The calendar settings of the model. |

## get_dimension_items

```
get_dimension_items(dimension_id: int) -> list[DimensionWithCode]
```

Get all items in a dimension. This will fail if the dimensions holds more than 1_000_000 items. Valid Dimensions are:

- Lists (101xxxxxxxxx)
- List Subsets (109xxxxxxxxx)
- Line Item Subsets (114xxxxxxxxx)
- Users (101999999999) For lists and users, you should prefer using the `get_list_items` and `get_users` methods, respectively, instead.

Parameters:

| Name           | Type  | Description                                | Default    |
| -------------- | ----- | ------------------------------------------ | ---------- |
| `dimension_id` | `int` | The ID of the dimension to list items for. | *required* |

Returns:

| Type                      | Description                |
| ------------------------- | -------------------------- |
| `list[DimensionWithCode]` | A list of Dimension items. |

## lookup_dimension_items

```
lookup_dimension_items(
    dimension_id: int,
    codes: list[str] | None = None,
    names: list[str] | None = None,
) -> list[DimensionWithCode]
```

Looks up items in a dimension by their codes or names. If both are provided, both will be searched for. You must provide at least one of `codes` or `names`. Valid Dimensions to lookup are:

- Lists (101xxxxxxxxx)
- Time (20000000003)
- Version (20000000020)
- Users (101999999999)

Parameters:

| Name           | Type        | Description                                  | Default                                     |
| -------------- | ----------- | -------------------------------------------- | ------------------------------------------- |
| `dimension_id` | `int`       | The ID of the dimension to lookup items for. | *required*                                  |
| `codes`        | \`list[str] | None\`                                       | A list of codes to lookup in the dimension. |
| `names`        | \`list[str] | None\`                                       | A list of names to lookup in the dimension. |

Returns:

| Type                      | Description                                                       |
| ------------------------- | ----------------------------------------------------------------- |
| `list[DimensionWithCode]` | A list of Dimension items that match the provided codes or names. |

## get_view_dimension_items

```
get_view_dimension_items(view_id: int, dimension_id: int) -> list[Dimension]
```

Get the members of a dimension that are part of the given View. This call returns data as filtered by the page builder when they configure the view. This call respects hidden items, filtering selections, and Selective Access. If the view contains hidden or filtered items, these do not display in the response. This will fail if the dimensions holds more than 1_000_000 items. The response returns Items within a flat list (no hierarchy) and order is not guaranteed.

Parameters:

| Name           | Type  | Description                               | Default    |
| -------------- | ----- | ----------------------------------------- | ---------- |
| `view_id`      | `int` | The ID of the View.                       | *required* |
| `dimension_id` | `int` | The ID of the Dimension to get items for. | *required* |

Returns:

| Type              | Description                            |
| ----------------- | -------------------------------------- |
| `list[Dimension]` | A list of Dimensions used in the View. |

## get_line_item_dimensions

```
get_line_item_dimensions(line_item_id: int) -> list[Dimension]
```

Get the dimensions of a Line Item. This will return all dimensions that are used in the Line Item.

Parameters:

| Name           | Type  | Description              | Default    |
| -------------- | ----- | ------------------------ | ---------- |
| `line_item_id` | `int` | The ID of the Line Item. | *required* |

Returns:

| Type              | Description                                 |
| ----------------- | ------------------------------------------- |
| `list[Dimension]` | A list of Dimensions used in the Line Item. |
