<p align="center" style="margin: 0 0 10px">
  <img width="200" height="200" src="https://vinzenzklass.github.io/anaplan-sdk/img/anaplan-sdk.png" alt='Python' style="border-radius: 15px">
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

Anaplan SDK is an independent, unofficial project providing pythonic access to
the [Anaplan Integration API v2](https://anaplan.docs.apiary.io/). This Project aims to provide high-level abstractions
over the API, so you can deal with python objects and simple functions rather than implementation details like HTTP
Requests, Authentication, JSON Parsing, Compression, Chunking and so on.

This Projects supports both
the [Bulk APIs](https://help.anaplan.com/use-the-bulk-apis-93218e5e-00e5-406e-8361-09ab861889a7) and
the [Transactional APIs](https://help.anaplan.com/use-the-transactional-apis-cc1c1e91-39fc-4272-a4b5-16bc91e9c313) and
provides synchronous and asynchronous Clients for both.

Visit [Anaplan SDK](https://vinzenzklass.github.io/anaplan-sdk/) for documentation.

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
    print(f"f{workspace.name}: {workspace.id}")

for model in anaplan.list_models():
    print(f"f{model.name}: {model.id}")
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
    print(f"f{workspace.name}: {workspace.id}")
for model in models:
    print(f"f{model.name}: {model.id}")
```

For more information, API reference and detailed guides,
visit [Anaplan SDK](https://vinzenzklass.github.io/anaplan-sdk/).
