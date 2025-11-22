This Quickstart focuses on the Bulk endpoints of the Anaplan API, which are most commonly used for data import and export. If you are looking for different APIs, such as the Transactional APIs or CloudWork APIs, please refer to the respective [Guides](https://vinzenzklass.github.io/anaplan-sdk/guides/index.md).

To get started, you can use basic authentication. Refer to the [Bulk API Guide](https://vinzenzklass.github.io/anaplan-sdk/guides/bulk/#instantiate-a-client) to understand why this is not a good idea for production use.

Prerequisites

The Quickstart assumes you already have both valid credentials for your tenant, and the `workspace_id` and `model_id` of the Model you want to work with. If you don't: You can find both of these either in the URL displayed in the browser or by instantiating a client with Authentication information only and then calling the `get_workspaces` and `get_models` methods. Alternatively, you can use an HTTP Client like Postman, Insomnia, or Paw.

```
import anaplan_sdk

anaplan = anaplan_sdk.Client(
    workspace_id="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    model_id="11111111111111111111111111111111",
    user_email="admin@company.com",
    password="my_super_secret_password",
)
```

```
import anaplan_sdk

anaplan = anaplan_sdk.AsyncClient(
    workspace_id="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    model_id="11111111111111111111111111111111",
    user_email="admin@company.com",
    password="my_super_secret_password",
)
```

## Importing Data

Start by listing available assets in your model. Typically, these will have already been created, and you will be searching for a specific name provided by your Model Builder. Here, we will use one file and one process, which is common practice.

```
file = anaplan.get_files()
processes = anaplan.get_processes()
```

```
from asyncio import gather

files, processes = await gather(anaplan.get_files(), anaplan.get_processes())
```

Output

Models used in this Example: [File](https://vinzenzklass.github.io/anaplan-sdk/api/models/bulk/#anaplan_sdk.models._bulk.File), [Process](https://vinzenzklass.github.io/anaplan-sdk/api/models/bulk/#anaplan_sdk.models._bulk.Process).

```
[
    File(
        id=113000000000,
        name="Quickstart.csv",
        chunk_count=0,
        delimiter='"',
        encoding="UTF-8",
        first_data_row=2,
        format="txt",
        header_row=1,
        separator=",",
    )
]
[Process(id=118000000000, name="Quickstart")]
```

With these two, you're ready to run your first import.

```
anaplan.upload_and_import(
    file_id=113000000000, action_id=118000000000, content=b"Hello, Anaplan!"
)
```

```
await anaplan.upload_and_import(
    file_id=113000000000, action_id=118000000000, content=b"Hello, Anaplan!"
)
```

This will upload the file to Anaplan, trigger the process task, wait for the completion of the task and validate the task result. You can see the details of the task by inspecting the [TaskResult](https://vinzenzklass.github.io/anaplan-sdk/api/models/task/#anaplan_sdk.models._task.TaskResult).

## Exporting Data

Conversely, for exporting data, we start by listing the available exports.

```
exports = anaplan.get_exports()
```

```
exports = await anaplan.get_exports()
```

Output

Models used in this Example: [Export](https://vinzenzklass.github.io/anaplan-sdk/api/models/bulk/#anaplan_sdk.models._bulk.Export).

```
[
    Export(
        id=116000000000,
        name="Quickstart Export",
        type="GRID_CURRENT_PAGE",
        format="text/csv",
        encoding="UTF-8",
        layout="GRID_CURRENT_PAGE",
    )
]
```

```
content = anaplan.export_and_download(116000000000)
```

```
content = await anaplan.export_and_download(116000000000)
```

## Next Steps

To gain a better understanding of how Anaplan handles data, head over to the [Anaplan Explained](https://vinzenzklass.github.io/anaplan-sdk/concepts/index.md) section.

For a more detailed guide on how to use both the [Bulk APIs](https://vinzenzklass.github.io/anaplan-sdk/guides/bulk/index.md) and [Transactional APIs](https://vinzenzklass.github.io/anaplan-sdk/guides/transactional/index.md), refer to the Guides.
