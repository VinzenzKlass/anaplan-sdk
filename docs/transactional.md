## Intro

If you need to go beyond the standard flows of importing and exporting data to and from Anaplan, you likely will need
some functionality of the Transactional APIs. The Transactional APIs can provide a lot of Information about the Model,
the data that resides in the model, ongoing Tasks etc. You can also use them to insert data directly into Lists and
Modules or read data from Lists and Modules. Whenever the need to do so arises, always consider if the same could be
achieved using the Bulk API first.

## Accessing the Namespace

All the methods for the Transactional APIs reside in a different namespace for better API navigability and
comprehensiveness, but are accessible through the same client for convenience. For e.g., you can call
the `.list_lists()` method like so:

/// tab | Synchronous

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

///
/// tab | Asynchronous

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

///

For brevity, if you need to access only the Transactional API or need to do so repeatedly, you can assign the
Transactional Client to it's own variable.

/// tab | Synchronous

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

///
/// tab | Asynchronous

```python
anaplan = anaplan_sdk.AsyncClient(
    workspace_id="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    model_id="11111111111111111111111111111111",
    certificate="~/certs/anaplan.pem",
    private_key="~/keys/anaplan.pem",
)
trans_anaplan = anaplan.transactional
lists = await trans_anaplan.list_lists()
modules = await trans_anaplan.list_modules()
```

///

!!! note
      While you can instantiate a [Client](client.md) without the workspace or model parameters, trying to access
      the [Transactional Client](transactional_client.md) on an instance without the `model_id` will raise a `ValueError`.

## Applications

### Resetting List Index w/o data loss

Lists holding large sets of transactional data that are frequently updated, will often produce a `List index limit`
Warning. To automate this tedious task without losing any data, we can perform four simple steps:

1. Export the list data and either hold it in memory or save it.
2. Purge the list. This is necessary so the List Index can be reset. Attempting to reset the Index of a non-empty List
   will result in an error.
3. Reset the List Index.
4. Reimport the Data from Step one.

/// tab | Synchronous

```python
items = anaplan.transactional.get_list_items(101000000000)
anaplan.transactional.delete_list_items(101000000000, [{"id": e.id} for e in items])
anaplan.transactional.reset_list_index(101000000000)
result = anaplan.transactional.add_items_to_list(101000000008, [{"code": e.code} for e in items])

```

///
/// tab | Asynchronous

```python
items = await anaplan.transactional.get_list_items(101000000000)
await anaplan.transactional.delete_list_items(101000000000, [{"id": e.id} for e in items])
await anaplan.transactional.reset_list_index(101000000000)
result = await anaplan.transactional.add_items_to_list(
    101000000008, [{"code": e.code} for e in items]
)
```

///
