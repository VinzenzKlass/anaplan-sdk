The CloudWorks API is a set of APIs that allow you to manage and interact with CloudWorks. It provides
functionality for creating, updating, and deleting CloudWorks Connection and Integrations as well as managing their
schedules and monitoring their status. For more details,
see [CloudWorks](https://help.anaplan.com/cloudworks-96f951fe-52fc-45a3-b6cb-16b7fe38e1aa). It also supports Flows, 
which are a sequence of integrations that are executed in a specific order.

## Listing Resources

You can list all CloudWorks Connections, Integrations and Flows using the following methods:

=== "Synchronous"
    ```python
    connections = anaplan.cw.get_connections()
    integrations = anaplan.cw.get_integrations()
    flows = anaplan.cw.flows.get_flows()
    ```
=== "Asynchronous"
    ```python
    from asyncio import gather

    connections, integrations, flows = await gather(
        anaplan.cw.get_connections(),
        anaplan.cw.get_integrations(),
        anaplan.cw.flows.get_flows(),
    )
    ```

All the examples below are shown using the synchronous API. The syntax for the asynchronous API is identical.

## Create a Connection

You can use the pydantic models from `anaplan_sdk.models.cloud_works` to construct a connection Payload with 
auto-completion, type checking and default values. This is most useful when manually constructing a connection payload,
but you can also pass a plain dictionary instead, when you are for e.g. dynamically creating the payload at runtime 
anyway.

=== "Pydantic"
    === "Azure Blob"
        ```python
        from anaplan_sdk.models.cloud_works import (
            AzureBlobConnectionInput, ConnectionInput
        )

        con_id = anaplan.cw.create_connection(
            ConnectionInput(
                type="AzureBlob",
                body=AzureBlobConnectionInput(
                    name="Azure Blob Connection",
                    storage_account_name="mystorageaccount",
                    sas_token="sp=racwdl&st=2025-09-19T09:02:45Z...",
                    container_name="my-container",
                ),
            )
        )   
        ```

    === "AWS S3"
        ```python
        from anaplan_sdk.models.cloud_works import (
            AmazonS3ConnectionInput, ConnectionInput
        )
    
        con_id = anaplan.cw.create_connection(
            ConnectionInput(
                type="AmazonS3",
                body=AmazonS3ConnectionInput(
                    name="AWS S3 Connection",
                    access_key_id="XXX",
                    secret_access_key="XXX",
                    bucket_name="my-bucket-name",
                ),
            )
        )
        ```
    === "Google BigQuery"
        ```python
        from anaplan_sdk.models.cloud_works import (
            GoogleBigQueryConnectionInput, ConnectionInput
        )
    
        con_id = anaplan.cw.create_connection(
            ConnectionInput(
                type="GoogleBigQuery",
                body=GoogleBigQueryConnectionInput(
                    name="Google BigQuery Connection",
                    dataset="my_dataset",
                    service_account_json={"type": "service_account", ...},
                ),
            )
        )
        ```

=== "Dictionary"
    === "Azure Blob"
        ```python
        con_id = anaplan.cw.create_connection(
            {
                "type": "AzureBlob",
                "body": {
                    "name": "Azure Blob Connection",
                    "storageAccountName": "mystorageaccount",
                    "containerName": "my-container",
                    "sasToken": "sp=racwdl&st=2025-09-19T09:02:45Z...",
                },
            }
        )
        ```
    === "AWS S3"
        ```python
        con_id = anaplan.cw.create_connection(
            {
                "type": "AmazonS3",
                "body": {
                    "name": "AWS S3 Connection",
                    "bucketName": "my-bucket-name",
                    "accessKeyId": "XXX",
                    "secretAccessKey": "XXX",
                },
            }
        )
        ```
    === "Google BigQuery"
        ```python
        con_id = anaplan.cw.create_connection(
            {
                "type": "GoogleBigQuery",
                "body": {
                    "name": "Google BigQuery Connection",
                    "dataset": "my_dataset",
                    "serviceAccountKey": {"type": "service_account", ...},
                },
            }
        )
        ```

If you pass a dictionary,the payload is still validated against the Pydantic Model. This way, you benefit from more concise error messages and can save on network calls. For example, if you accidentally pass  `storageAccount` instead of `storageAccountName` in the dictionary payload, you will get
> body.AzureBlobConnectionInput.storageAccountName Field required

instead of

> { "code": 400, "message": "Invalid request body" }

and without sending a request to Anaplan at all.

## Create an Integration

Similarly, you can use the `create_integration` method to create an integration.

=== "Pydantic"
    ```python
    from anaplan_sdk.models.cloud_works import (
        AnaplanTarget,
        FileSource,
        IntegrationInput,
        IntegrationJobInput,
    )

    source = FileSource(type="AzureBlob", connection_id="5e...05", file="dummy.csv")
    target = AnaplanTarget(action_id=112000000001, file_id=113000000001)
    job = IntegrationJobInput(
        type="AzureBlobToAnaplan", sources=[source], targets=[target]
    )
    integration_input = IntegrationInput(
        name="Blob to Anaplan",
        workspace_id="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
        model_id="22222222222222222222222222222222",
        jobs=[job],
    )
    integration_id = anaplan.cw.create_integration(integration_input)
    ```
=== "Dictionary"
    ```
    anaplan.cw.create_integration(
        {
            "name": "Blob to Anaplan",
            "version": "2.0",
            "workspaceId": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
            "modelId": "22222222222222222222222222222222",
            "nuxVisible": False,
            "jobs": [
                {
                    "type": "AzureBlobToAnaplan",
                    "sources": [
                        {
                            "connectionId": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
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
    )
    ```

To create a Process Integration, you can simply extend the above example to include the `process_id` in the
`IntegrationInput` instance. You can then pass as number of `IntegrationJobInput` to `jobs`.
=== "Pydantic"
    ```python
    anaplan.cw.create_integration(
        IntegrationInput(
            name="Double Blob to Anaplan",
            workspace_id="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
            model_id="22222222222222222222222222222222",
            process_id=118000000012,  # Add this line
            jobs=[job, another_job, ...],
        )
    ```

=== "Dictionary"
    ```python
    anaplan.cw.create_integration(
        {
            "name": "Double Blob to Anaplan",
            "version": "2.0",
            "workspaceId": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
            "modelId": "22222222222222222222222222222222",
            "processId": "118000000012", # Add this line
            "nuxVisible": false,
            "jobs": [
                {
                    "type": "AzureBlobToAnaplan",
                    "sources": [
                        {
                            "connectionId": "5e...05",
                            "type": "AzureBlob",
                            "file": "dummy.csv"
                        }
                    ],
                    "targets": [
                        {
                            "type": "Anaplan",
                            "actionId": "112000000001",
                            "fileId": "113000000001"
                        }
                    ]
                },
                {
                    "type": "AzureBlobToAnaplan",
                    "sources": [
                        {
                            "connectionId": "5e...05",
                            "type": "AzureBlob",
                            "file": "dummy.csv"
                        }
                    ],
                    "targets": [
                        {
                            "type": "Anaplan",
                            "actionId": "112000000001",
                            "fileId": "113000000001"
                        }
                    ]
                }
            ]
        }
    )
    ```

Be careful to ensure that all ids specified in the job inputs match what is defined in your model and matches the
process. If this is not the case, this will error, occasionally with a misleading error message, i.e.
`XYZ is not defined in your model` even though it is, Anaplan just does not know what to do with it in the location you
specified.

You can also use CloudWorks to simply schedule a process in one of your models, or create an integration with only a
process for any other reason. To do so, you can pass an `IntegrationProcessInput` instance to `create_integration`
instead, or an accordingly shaped dictionary:

=== "Pydantic"
    ```python
    from anaplan_sdk.models.cloud_works import IntegrationProcessInput

    anaplan.cw.create_integration(
        IntegrationProcessInput(
            name="My Process",
            process_id=118000000012,
            workspace_id="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
            model_id="22222222222222222222222222222222",
        )
    )
    ```
=== "Dictionary"
    ```python
    anaplan.cw.create_integration(
        {
            "name": "My Process",
            "version": "2.0",
            "workspaceId": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
            "modelId": "22222222222222222222222222222222",
            "processId": "118000000012"
        }
    )
    ```


## Create a Flow

A Flow or Integration Flow is a sequence of integrations that are executed in a specific order. You can create a Flow
using the `create_flow` method. The flow can again be created passing either a dictionary or a Pydantic model. This SDK
also comes with a set of defaults, allowing you to omit a lot of inputs compared to calling the API directly.

=== "Pydantic"
    ```python
    from anaplan_sdk.models.flows import FlowInput, FlowStepInput
    
    anaplan.cw.flows.create_flow(
        FlowInput(
            name="My Flow",
            steps=[
                FlowStepInput(referrer="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"),
                FlowStepInput(
                    referrer="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
                    depends_on=["AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"],
                ),
            ],
        )
    )
    ```
=== "Dictionary"
    ```python
    anaplan.cw.flows.create_flow(
        {
            "name": "My Flow",
            "version": "2.0",
            "type": "IntegrationFlow",
            "steps": [
                {
                    "type": "Integration",
                    "referrer": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
                    "isSkipped": False,
                    "exceptionBehavior": [
                        {
                            "type": "failure",
                            "strategy": "stop"
                        },
                        {
                            "type": "partial_success",
                            "strategy": "continue"
                        }
                    ]
                },
                {
                    "type": "Integration",
                    "referrer": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
                    "dependsOn": [
                        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
                    ],
                    "isSkipped": False,
                    "exceptionBehavior": [
                        {
                            "type": "failure",
                            "strategy": "stop"
                        },
                        {
                            "type": "partial_success",
                            "strategy": "continue"
                        }
                    ]
                }
            ]
        }
    )
    ```
