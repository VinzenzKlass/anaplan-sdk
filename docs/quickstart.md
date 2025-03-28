This Quickstart Guide assumes you already have both the `Workspace Id` and `Model Id` of the Model you want to work
with. If you don't: You can find both of these either in the URL displayed on the browser or by instantiating a client
with Authentication information only and then call the `list_workspaces` and `list_models` endpoint. Alternatively, you
can use an HTTP Client like Postman, Insomnia, or Paw.

It further assumes you have a valid user with credentials and required permissions.

## Initializing the Client

To get started, you can use basic authentication with your email and password. Refer to
the [Bulk API Guide](guides/bulk.md#instantiate-a-client) to understand why this is not a good idea for production use.

/// tab | Synchronous

```python
import anaplan_sdk

anaplan = anaplan_sdk.Client(
    workspace_id="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    model_id="11111111111111111111111111111111",
    user_email="admin@company.com",
    password="my_super_secret_password",
)
```

///

/// tab | Asynchronous

```python
import anaplan_sdk

anaplan = anaplan_sdk.AsyncClient(
    workspace_id="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    model_id="11111111111111111111111111111111",
    user_email="admin@company.com",
    password="my_super_secret_password",
)
```

///

## Getting Started

### Importing data

/// tab | Synchronous

```python
anaplan.upload_file(113000000000, b"Hello Anaplan")
anaplan.run_action(112000000000)

# Or in short:
anaplan.upload_and_import(113000000000, b"Hello Anaplan", 112000000000)
```

///
/// tab | Asynchronous

```python
await anaplan.upload_file(113000000000, b"Hello Anaplan")
await anaplan.run_action(112000000000)

# Or in short:
await anaplan.upload_and_import(113000000000, b"Hello Anaplan", 112000000000)

```

///

### Exporting data

/// tab | Synchronous

```python
anaplan.run_action(116000000000)
content = anaplan.get_file(116000000000)

# Or in short:
content = anaplan.export_and_download(116000000000)
```

///
/// tab | Asynchronous

```python
await anaplan.run_action(116000000000)
content = await anaplan.get_file(116000000000)

# Or in short:
content = await anaplan.export_and_download(116000000000)
```

///

## Next Steps

To gain a better understanding of how Anaplan handles data, head over to the [Anaplan Explained](anaplan_explained.md)
section.

For a more detailed guide on how to use both the [Bulk APIs](guides/bulk.md) and [Transactional APIs](guides/transactional.md), refer
to the Guides.
