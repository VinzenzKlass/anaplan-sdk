<p align="center" style="margin: 0 0 10px">
  <img width="200" height="200" src="https://vinzenzklass.github.io/anaplan-sdk/img/anaplan-sdk.webp" alt='Python' style="border-radius: 15px">
</p>

<h1 align="center" style="font-size: 3rem; font-weight: 400; margin: -15px 0">
Anaplan SDK
</h1>

<p align="center" style="margin-top: 15px">
<a href="https://pepy.tech/project/anaplan-sdk">
<img align="center" src="https://static.pepy.tech/badge/anaplan-sdk/month" alt="Downloads Badge"/>
</a>
</p>

---

Anaplan SDK is an independent, unofficial project providing pythonic access to Anaplan. Anaplan SDK provides high-level
abstractions over the various Anaplan APIs, so you can focus on you requirements rather than spend time on
implementation details like authentication, error handling, chunking, compression and data formatting.

This Projects supports
the [Bulk APIs](https://help.anaplan.com/use-the-bulk-apis-93218e5e-00e5-406e-8361-09ab861889a7),
the [Transactional APIs](https://help.anaplan.com/use-the-transactional-apis-cc1c1e91-39fc-4272-a4b5-16bc91e9c313) and
the [ALM APIs](https://help.anaplan.com/application-lifecycle-management-api-2565cfa6-e0c2-4e24-884e-d0df957184d6),
the [Audit APIs](https://auditservice.docs.apiary.io/#),
providing both synchronous and asynchronous Clients.

Visit [Anaplan SDK](https://vinzenzklass.github.io/anaplan-sdk/) for documentation.

If you find any issues or feel that this SDK is not adequately covering your use case,
please [open an issue](https://github.com/VinzenzKlass/anaplan-sdk/issues/new).

---

### Install Anaplan SDK using pip

```shell
pip install anaplan-sdk
```

### Instantiate a client

```python
import anaplan_sdk

anaplan = anaplan_sdk.Client(
    workspace_id="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    model_id="11111111111111111111111111111111",
    user_email="admin@company.com",
    password="my_super_secret_password",
)
```

### Find workspaces and models

If you don't know the workspace and model Ids, instantiate client with authentication information only and
call `.list_workspaces()` and list `.list_models()`

```python
anaplan = anaplan_sdk.Client(
    user_email="admin@company.com",
    password="my_super_secret_password",
)

for workspace in anaplan.list_workspaces():
    print(f"{workspace.name}: {workspace.id}")

for model in anaplan.list_models():
    print(f"{model.name}: {model.id}")
```

### Async Support

This SDK also provides an `AsyncClient` with full async support

```python
import asyncio

anaplan = anaplan_sdk.AsyncClient(
    workspace_id="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    model_id="11111111111111111111111111111111",
    user_email="admin@company.com",
    password="my_super_secret_password",
)
workspaces, models = await asyncio.gather(
    anaplan.list_workspaces(), anaplan.list_models()
)
for workspace in workspaces:
    print(f"{workspace.name}: {workspace.id}")
for model in models:
    print(f"{model.name}: {model.id}")
```

For more information, API reference and detailed guides,
visit [Anaplan SDK](https://vinzenzklass.github.io/anaplan-sdk/).

### Contributing

Pull Requests are welcome. For major changes, please open an issue first to discuss what you would like to change. To
submit a pull request, please follow the
standard [Fork & Pull Request workflow](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork).

Before submitting your pull request, please ensure that all the files pass linting and formatting checks. You can do
this by running the following command:

```shell
uv sync --dev

ruff check
ruff format
```

You can also enable [pre-commit](https://pre-commit.com/) hooks to automatically format and lint your code before
committing:

```shell
pre-commit install
```

If your PR goes beyond a simple bug fix or small changes, please add tests to cover your changes.

### API Endpoints
- [ ] [Create a connection](https://cloudworks.docs.apiary.io/#create_connection)
- [ ] [Get connections](https://cloudworks.docs.apiary.io/#get_connections)
- [ ] [Edit a connection](https://cloudworks.docs.apiary.io/#edit_connection)
- [ ] [Patch a connection](https://cloudworks.docs.apiary.io/#patch_connection)
- [ ] [Delete a connection](https://cloudworks.docs.apiary.io/#delete_connection)
- [ ] [Create a new integration](https://cloudworks.docs.apiary.io/#create_integration)
- [ ] [Run an integration](https://cloudworks.docs.apiary.io/#run_integration)
- [ ] [Get all integrations](https://cloudworks.docs.apiary.io/#get_integrations)
- [ ] [Get integrations by integration ID](https://cloudworks.docs.apiary.io/#get_integrations_by_integration)
- [ ] [Get integrations by Model ID](https://cloudworks.docs.apiary.io/#get_integration_by_model)
- [ ] [Edit an integration](https://cloudworks.docs.apiary.io/#edit_integration)
- [ ] [Delete an integration](https://cloudworks.docs.apiary.io/#delete_integration)
- [ ] [Create process integration](https://cloudworks.docs.apiary.io/#create_process_integration)
- [ ] [Edit a process integration](https://cloudworks.docs.apiary.io/#edit_process_integration)
- [ ] [Set the status of an integration schedule](https://cloudworks.docs.apiary.io/#set_status_schedule)
- [ ] [Create an integration schedule](https://cloudworks.docs.apiary.io/#create_integration_schedule)
- [ ] [Update the schedule of an integration](https://cloudworks.docs.apiary.io/#update_schedule)
- [ ] [Delete an integration schedule](https://cloudworks.docs.apiary.io/#delete_integration_schedule)
- [ ] [Get history of integration runs](https://cloudworks.docs.apiary.io/#get_history)
- [ ] [Get integration run errors](https://cloudworks.docs.apiary.io/#get_run_errors)
- [ ] [Get run status](https://cloudworks.docs.apiary.io/#get_run_status)
- [ ] [Get a notification configuration](https://cloudworks.docs.apiary.io/#get_notification)
- [ ] [Create notification configuration](https://cloudworks.docs.apiary.io/#create_notification)
- [ ] [Edit a notification configuration](https://cloudworks.docs.apiary.io/#edit_notification)
- [ ] [Delete a notification configuration](https://cloudworks.docs.apiary.io/#delete_notification)
- [ ] [Get an import error log](https://cloudworks.docs.apiary.io/#get_import_error_log)
- [ ] [Get a process error log](https://cloudworks.docs.apiary.io/#get_process_error_log)

### Flow Endpoints

- [ ] Create a new integration flow
- [ ] Run an integration flow
- [ ] Get all integration flows
- [ ] Get integration flows by integration ID
- [ ] Delete an integration flow
- [ ] Edit an integration flow
