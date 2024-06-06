This Quickstart Guide assumes you already have both the `Workspace Id` and `Model Id` of the Model you want to work
with. If you don't: You can find both of these either in the URL displayed on the browser or by instantiating a client
with Authentication information only and then call the `list_workspaces` and `list_models` endpoint. Alternatively, you
can use an HTTP Client like Postman, Insomnia, or Paw.

It further assumes you have a valid user with credentials and required permissions.

## Instantiate a Client

Clients are instantiated with the workspace, model and authentication information. There are two primary means of
Authentication.

### Basic Authentication

Basic Authentication is unsuitable for Production. Anaplan password policies force password changes every 30, 60 or 90
days, depending on tenant settings, making this approach annoying to maintain and error-prone and is thus not
recommended for production.

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

### Certificate Authentication

/// tab | Synchronous

```python
import anaplan_sdk

anaplan = anaplan_sdk.Client(
    workspace_id="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    model_id="11111111111111111111111111111111",
    certificate="~/certs/anaplan.pem",
    private_key="~/keys/anaplan.pem",
    private_key_password="my_super_secret_password",
)

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
    private_key_password="my_super_secret_password",
)

```

///

## Making first requests

Say you want to find the id of an export action based on the name provided by one of your Anaplan Model Builders, run
the export, find the file that was populated, and retrieve the content thereof. If this workflow feels unintuitive, you
may want to head over to the [Anaplan Explained](anaplan_explained.md) Section.

Here is what these steps would look like:

/// tab | Synchronous

```python
export_id = next(
    filter(
        lambda x: "The thing I am looking for" in x.name,
        anaplan.list_exports(),
    )
).id
anaplan.run_action(export_id)
content = anaplan.get_file(export_id)
```

///
/// tab | Asynchronous

```python
export_id = next(
    filter(
        lambda x: "The thing I am looking for" in x.name,
        await anaplan.list_exports(),
    )
).id
await anaplan.run_action(export_id)
content = await anaplan.get_file(export_id)

```

///

The `content` variable will now hold the content of what was produced by the invoked export action.

The same works similarly for imports:

/// tab | Synchronous

```python
import_config = next(
    filter(
        lambda x: "The thing I am looking for" in x.name,
        anaplan.list_imports(),
    )
)
anaplan.upload_file(import_config.source_id, "Some excellent new data!")
anaplan.run_action(import_config.id)
```

///
/// tab | Asynchronous

```python
import_config = next(
    filter(
        lambda x: "The thing I am looking for" in x.name,
        await anaplan.list_imports(),
    )
)
await anaplan.upload_file(import_config.source_id, "Some excellent new data!")
await anaplan.run_action(import_config.id)
```

///

Relying on the naming of actions to identify them can be very risky and is highly error-prone. It is generally a good
idea to align with your model builders, agree on the logic for your dataflows and then statically reference them by
their ids. If you need some flexibility, you can always wrap the action in processes and call these, so that the model
builder can make minor changes independently.

If you already know all the Ids, you just need the last two lines of the above Snippet, making the code becomes much simpler and more robust.

For a more detailed guide on how to use both the Bulk APIs and Transactional APIs, refer to the Guides.
