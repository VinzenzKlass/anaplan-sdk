<p align="center" style="margin: 0 0 10px">
  <img width="200" height="200" src="https://vinzenzklass.github.io/anaplan-sdk/img/anaplan-sdk.png" alt='Python' style="border-radius: 15px">
</p>

<h1 align="center" style="font-size: 3rem; font-weight: 400; margin: -15px 0">
Anaplan SDK
</h1>

---

Anaplan SDK is an independent, unofficial project providing pythonic access to
the [Anaplan Integration API v2](https://anaplan.docs.apiary.io/). This Project aims to provide high-level abstractions
over the API, so you can deal with python objects and simple functions rather than implementation details like HTTP
Requests, Authentication, JSON Parsing, Compression, Chunking and so on.

Visit [Anaplan SDK](https://vinzenzklass.github.io/anaplan-sdk/) for documentation.

---

### Install Anaplan SDK using pip

```shell
pip install anaplan-sdk
```

### Instantiate a client

```python
import anaplan_sdk

anaplan_client = anaplan_sdk.Client(
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
anaplan_client = anaplan_sdk.Client(
    user_email="admin@company.com",
    password="my_super_secret_password",
)

for workspace in anaplan_client.list_workspaces():
    print(f"f{workspace.name}: {workspace.id}")

for model in anaplan_client.list_models():
    print(f"f{model.name}: {model.id}")
```

### Async Support

This SDK also provides and `AsyncClient` with full async support

```python
anaplan_client = anaplan_sdk.AsyncClient(
    workspace_id=os.getenv("ANAPLAN_SDK_TEST_WORKSPACE_ID"),
    model_id=os.getenv("ANAPLAN_SDK_TEST_MODEL_ID"),
    certificate=os.getenv("ANAPLAN_SDK_TEST_CERT"),
    private_key=os.getenv("ANAPLAN_SDK_TEST_PK"),
)
workspaces, models = await asyncio.gather(
    anaplan_client.list_workspaces(), anaplan_client.list_models()
)
for workspace in workspaces:
    print(f"f{workspace.name}: {workspace.id}")
for model in models:
    print(f"f{model.name}: {model.id}")
```

For more information, API reference and detailed guides:
Visit [Anaplan SDK](https://vinzenzklass.github.io/anaplan-sdk/).
