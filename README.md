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
the [ALM APsI](https://help.anaplan.com/application-lifecycle-management-api-2565cfa6-e0c2-4e24-884e-d0df957184d6),
the [Audit APIs](https://auditservice.docs.apiary.io/#),
providing both synchronous and asynchronous Clients.

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
