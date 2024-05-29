This Quickstart Guide assumes you already have both the `Workspace Id` and `Model Id` of the Model you want to work
with. If you don't: You can find both of these either in the URL displayed on the browser or by instantiating a client
with Authentication information only and then call the `list_workspaces` and `list_models` endpoint. Alternatively, you
can use an HTTP Client like Postman, Insomnia, or Paw.

It further assumes you have a valid user with credentials and required permissions.

This Project provides both synchronous and asynchronous clients. The rest of this Quickstart will provide code samples
for the synchronous client. For usage of the asynchronous client you can replace the `Client` with `AsyncClient` and use
async await syntax.

## Instantiate a Client

Clients are instantiated with the workspace, model and authentication information. There are two primary means of
Authentication.

### Basic Authentication

Basic Authentication is unsuitable for Production. Anaplan password policies force password changes every 30, 60 or 90
days, depending on tenant settings, making this approach annoying to maintain and error-prone and is thus not
recommended for production.

```python
import anaplan_sdk

anaplan_client = anaplan_sdk.Client(
    workspace_id="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    model_id="11111111111111111111111111111111",
    user_email="admin@company.com",
    password="my_super_secret_password",
)
```

### Certificate Authentication

```python
import anaplan_sdk

anaplan_client = anaplan_sdk.Client(
    workspace_id="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    model_id="11111111111111111111111111111111",
    certificate=r"C:\users\vinz\certs\anaplan.pem",
    private_key=r"C:\users\vinz\keys\anaplan.pem",
    private_key_password="my_super_secret_password",
)
```

## Making first requests

Once Instantiated, you can invoke any method on your client instance. Say you want to find the id of an export action
based on the name provided by one of your Anaplan Model Builders, run the export, find the file that was populated, and
retrieve the content thereof. If this workflow feels unintuitive, you may want to head over to
the [Anaplan Explained](anaplan_explained.md) Section.

Here is what these steps would look like:

```python
export_id = next(
    filter(
        lambda x: "The thing I am looking for" in x.name,
        anaplan_client.list_exports(),
    )
).id
anaplan_client.run_action(export_id)
content = anaplan_client.get_file(export_id)
```

The `content` variable will now hold the content of what was produced by the invoked export action.

The same works similarly for imports:

```python
import_config = next(
    filter(
        lambda x: "The thing I am looking for" in x.name,
        anaplan_client.list_imports(),
    )
)
anaplan_client.upload_file(import_config.source_id, "Some excellent new data!")
anaplan_client.run_action(import_config.id)
```

Relying on the naming of actions to identify them can be very risky and is highly error-prone. It is generally a good
idea to align with your model builders, agree on the logic for your dataflows and then statically reference them by
their ids. If you need some flexibility, you can always wrap the action in processes and call these, so that the model
builder can make minor changes independently.
