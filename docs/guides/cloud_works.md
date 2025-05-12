The CloudWorks API is a set of APIs that allow you to manage and interact with Anaplan CloudWorks. It provides
functionality for creating, updating, and deleting CloudWorks Connection and Integrations as well as managing their
schedules and monitoring their status. For more details,
see [CloudWorks](https://help.anaplan.com/cloudworks-96f951fe-52fc-45a3-b6cb-16b7fe38e1aa).

## Create a Connection

You can create a CloudWorks Connection using the `create_connection` method. The connection can be created passing
either a dictionary or a Pydantic model. The below two statements are equivalent:

=== "Synchronous"
    ```python
    from_pydantic = anaplan.cw.create_connection(
        ConnectionInput(
            type="AzureBlob",
            body=AzureBlobConnectionInput(
                name="My Blob",
                storage_account_name="mystorageaccount",
                sas_token="sp=rl&st=2025-05-10T19:29:44Z...",
                container_name="raw",
            ),
        )
    )
    from_dict = anaplan.cw.create_connection(
        {
            "type": "AzureBlob",
            "body": {
                "name": "My Blob",
                "storageAccountName": "mystorageaccount",
                "containerName": "raw",
                "sasToken": "sp=rl&st=2025-05-10T19:29:44Z...",
            },
        }
    )
    ```

=== "Asynchronous"
    ```python
    from_pydantic = await anaplan.cw.create_connection(
        ConnectionInput(
            type="AzureBlob",
            body=AzureBlobConnectionInput(
                name="My Blob",
                storage_account_name="mystorageaccount",
                sas_token="sp=rl&st=2025-05-10T19:29:44Z...",
                container_name="raw",
            ),
        )
    )
    from_dict = await anaplan.cw.create_connection(
        {
            "type": "AzureBlob",
            "body": {
                "name": "My Blob",
                "storageAccountName": "mystorageaccount",
                "containerName": "raw",
                "sasToken": "sp=rl&st=2025-05-10T19:29:44Z...",
            },
        }
    )
    ```

In the latter case, you still benefit from pydantic validation before the request is sent out. This way, you benefit
from more concise error messages and can save on network calls. For example, if you accidentally pass

=== "Synchronous"
    ```python
    from_dict = anaplan.cw.create_connection(
        {
            "type": "AzureBlob",
            "body": {
                "name": "My Blob 2",
                "storageAccount": "mystorageaccount",
                "containerName": "raw",
                "sasToken": "sp=rl&st=2025-05-10T19:29:44Z...",
            },
        }
    )
    ```

=== "Asynchronous"
    ```python
    from_dict = await anaplan.cw.create_connection(
        {
            "type": "AzureBlob",
            "body": {
                "name": "My Blob 2",
                "storageAccount": "mystorageaccount",
                "containerName": "raw",
                "sasToken": "sp=rl&st=2025-05-10T19:29:44Z...",
            },
        }
    )
    ```

You will get
> body.AzureBlobConnectionInput.storageAccountName Field required

Instead of
> { "code": 400, "message": "Invalid request body" }

before any network calls are made.

## Create an Integration

Similarly, you can use the pydantic models provided by the `anaplan_sdk.models.cloud_works` module to construct an Integration Payload with auto-completion, type checking and default values. The following example shows how to create an Integration that copies data from an Azure Blob Storage to Anaplan.
```python
source = FileSource(
    type="AzureBlob", connection_id="5e...05", file="dummy.csv"
)
target = AnaplanTarget(action_id=112000000001, file_id=113000000001)
job = IntegrationJobInput(
    type="AzureBlobToAnaplan", sources=[source], targets=[target]
)
integration_input = IntegrationInput(
    name="Blob to Anaplan",
    workspace_id="8a81b09d599f3c6e0159f605560c2630",
    model_id="8896D8C366BC48E5A3182B9F5CE10526",
    jobs=[job],
)
```

??? example "Dictionary Payload"
    The equivalent dictionary payload would be:

    ```
    {
        "name": "Blob to Anaplan",
        "version": "2.0",
        "workspaceId": "8a81b09d599f3c6e0159f605560c2630",
        "modelId": "8896D8C366BC48E5A3182B9F5CE10526",
        "nuxVisible": false,
        "jobs": [
            {
                "type": "AzureBlobToAnaplan",
                "sources": [
                    {
                        "connectionId": "5e634ba338444d2ea26ce384a70b5705",
                        "type": "AzureBlob",
                        "file": "dummy.csv"
                    }
                ],
                "targets": [
                    {
                        "type": "Anaplan",
                        "actionId": "112000000001",
                        "fileId": "112000000001"
                    }
                ]
            }
        ]
    }
    ```

To create a Process Integration, you can simply extend the above example to include the `process_id` in the `IntegrationInput` instance. You can then pass as number of `IntegrationJobInput` to `jobs`. 

```python
integration_input = IntegrationInput(
    name="Double Blob to Anaplan",
    workspace_id="8a81b09d599f3c6e0159f605560c2630",
    model_id="8896D8C366BC48E5A3182B9F5CE10526",
    process_id=118000000012, # Add this line
    jobs=[job, another_job, ...],
)
```

Be careful to ensure, that all ids specified in the job inputs match what is defined in your model and matches the process. If this is not the case, this will error, occasionally with a misleading error message, i.e. `XYZ is not defined in your model` even though it is, Anaplan just does not know what to do with it in the location you specified.

You can also use CloudWorks to simply schedule a process in one of your models, or create an integration with only a process for any other reason. To do so, you can pass an `IntegrationProcessInput` instance to `create_integration` instead, or an accordingly shaped dictionary:

```python
IntegrationProcessInput(
    name="My Process",
    process_id=118000000012,
    workspace_id="8a81b09d599f3c6e0159f605560c2630",
    model_id="8896D8C366BC48E5A3182B9F5CE10526",
)
```
