The purpose of the Application Lifecycle Management (ALM) API is to make model change management more scalable,
automatable, and integrate with other systems.

For details on required subscriptions and what you might want to use the ALM API for, refer to
[the Documentation](https://help.anaplan.com/application-lifecycle-management-0406d4dd-3e8d-40c0-be2f-1c34c1caeebf).

## Accessing the Namespace

All the methods for the ALM APIs reside in a different namespace for better API navigability and
comprehensiveness, but are accessible through the same client for convenience. For e.g., you can call
the `.get_revisions()` method like so:

=== "Synchronous"
      ```python
      import anaplan_sdk
      
      anaplan = anaplan_sdk.Client(
          workspace_id="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
          model_id="11111111111111111111111111111111",
          certificate="~/certs/anaplan.pem",
          private_key="~/keys/anaplan.pem",
      )
      revisions = anaplan.alm.get_revisions()
      ```
=== "Asynchronous"
      ```python
      import anaplan_sdk
      
      anaplan = anaplan_sdk.AsyncClient(
          workspace_id="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
          model_id="11111111111111111111111111111111",
          certificate="~/certs/anaplan.pem",
          private_key="~/keys/anaplan.pem",
      )
      revisions = await anaplan.alm.get_revisions()
      ```
???+ note
      While you can instantiate a [Client](../api/sync/sync_client.md) without the workspace or model parameters, trying to access
      the [ALM Client](../api/sync/sync_alm_client.md) on an instance without the `model_id` will raise a `ValueError`.

For brevity, if you need to access only the ALM API or need to do so repeatedly, you can assign the
ALM Client to its own variable.

=== "Synchronous"
      ```python
      alm = anaplan.alm
      revisions = alm.get_revisions()
      syncs = alm.get_sync_tasks()
      ```
=== "Asynchronous"
      ```python
      alm = anaplan.alm
      revisions, syncs = await asyncio.gather(
          alm.get_revisions(), alm.get_sync_tasks()
      )
      ```


## Model Status Management

You can change a Models online state.

=== "Synchronous"
    ```python
    anaplan.alm.change_model_status("offline")
    anaplan.alm.change_model_status("online")
    ```
=== "Asynchronous"
    ```python
    await anaplan.alm.change_model_status("offline")
    await anaplan.alm.change_model_status("online")
    ```


## Revision Management

Revisions are snapshots of your model at a specific point in time. You can create new revisions to mark important milestones in your model development.

=== "Synchronous"
    ```python
    revisions = anaplan.alm.get_revisions()
    latest = anaplan.alm.get_latest_revision()
    new_revision = anaplan.alm.create_revision(
        name="Production Release v2.1",
        description="Updated forecast logic and new product hierarchy"
    )
    ```
=== "Asynchronous"
    ```python
    revisions = await anaplan.alm.get_revisions()
    latest = await anaplan.alm.get_latest_revision()
    new_revision = await anaplan.alm.create_revision(
        name="Production Release v2.1",
        description="Updated forecast logic and new product hierarchy"
    )
    ```

Before synchronizing models, you need to identify which revisions from your source model can be synchronized to your target model. You can list all revisions that are compatible for synchronization for any model.

=== "Synchronous"
    ```python
    source_model_id = "22222222222222222222222222222222"
    syncable_revisions = anaplan.alm.get_syncable_revisions(source_model_id)
    ```
=== "Asynchronous"
    ```python
    source_model_id = "22222222222222222222222222222222"
    syncable_revisions = await anaplan.alm.get_syncable_revisions(source_model_id)
    ```

## Model Synchronization

Model synchronization allows you to propagate changes from one model to another. This is particularly useful for promoting changes from development to test or production environments.

=== "Synchronous"
    ```python
    sync_task = anaplan.alm.sync_models(
        source_revision_id="rev_123",
        source_model_id="22222222222222222222222222222222",
        target_revision_id="rev_456"
    )
    ```
=== "Asynchronous"
    ```python
    sync_task = await anaplan.alm.sync_models(
        source_revision_id="rev_123",
        source_model_id="22222222222222222222222222222222",
        target_revision_id="rev_456"
    )
    ```
By default, the `sync_models` method will wait until the synchronization is complete and return the results. You can also specify `wait_for_completion=False` to start the sync and return immediately. For long-running synchronization tasks, you might want to start the sync and check on it later rather than blocking your application.


You can list and monitor all sync tasks for your model to track ongoing or recent synchronization activities.

=== "Synchronous"
    ```python
    sync_tasks = anaplan.alm.get_sync_tasks()
    
    # See if there is any task that is still running
    running_task = next((t for t in sync_tasks if t.task_state != "COMPLETE"), None)
    ```
=== "Asynchronous"
    ```python
    sync_tasks = await anaplan.alm.get_sync_tasks()
    
    # See if there is any task that is still running
    running_task = next((t for t in sync_tasks if t.task_state != "COMPLETE"), None)
    ```

## Comparison Reports

Comparison reports provide detailed information about the differences between two model revisions.

=== "Synchronous"
    ```python
    report_task = anaplan.alm.create_comparison_report(
        source_revision_id="rev_123",
        source_model_id="22222222222222222222222222222222",
        target_revision_id="rev_456"
    )
    report_content = anaplan.alm.get_comparison_report(report_task)
    ```
=== "Asynchronous"
    ```python
    report_task = await anaplan.alm.create_comparison_report(
        source_revision_id="rev_123",
        source_model_id="22222222222222222222222222222222",
        target_revision_id="rev_456"
    )
    report_content = await anaplan.alm.get_comparison_report(report_task)
    ```
By default, the `create_comparison_report` method will wait until the report is complete. You can also specify `wait_for_completion=False` to start the report generation and return immediately. You can then check the status of the report and retrieve the content once it's ready.

=== "Synchronous"
    ```python
    report_task = anaplan.alm.create_comparison_report(
        source_revision_id="rev_123",
        source_model_id="22222222222222222222222222222222",
        target_revision_id="rev_456",
        wait_for_completion=False
    )
    # Check the status of the report later
    report_status = anaplan.alm.get_comparison_report_task(report_task.id)
    if report_status.task_state == "COMPLETE":
        report_content = anaplan.alm.get_comparison_report(report_task)
    ```
=== "Asynchronous"
    ```python
    report_task = await anaplan.alm.create_comparison_report(
        source_revision_id="rev_123",
        source_model_id="22222222222222222222222222222222",
        target_revision_id="rev_456",
        wait_for_completion=False
    )
    # Check the status of the report later
    report_status = await anaplan.alm.get_comparison_report_task(report_task.id)
    if report_status.task_state == "COMPLETE":
        report_content = await anaplan.alm.get_comparison_report(report_task)
    ``` 

---

For a brief overview of changes, you can generate comparison summaries that provide structured data about the differences. The summary will be an instance of [`SummaryReport`](../api/models/alm.md#anaplan_sdk.models._alm.SummaryReport).

=== "Synchronous"
    ```python
    summary = anaplan.alm.create_comparison_summary(
        source_revision_id="rev_123",
        source_model_id="22222222222222222222222222222222",
        target_revision_id="rev_456"
    )
    ```
=== "Asynchronous"
    ```python
    summary = await anaplan.alm.create_comparison_summary(
        source_revision_id="rev_123",
        source_model_id="22222222222222222222222222222222",
        target_revision_id="rev_456"
    )
    ```
By default, the `create_comparison_summary` method will wait until the summary is complete. You can also specify `wait_for_completion=False` to start the summary generation and return immediately. You can then check the status of the summary and retrieve the content once it's ready.

=== "Synchronous"
    ```python
    summary_task = anaplan.alm.create_comparison_summary(
        source_revision_id="rev_123",
        source_model_id="22222222222222222222222222222222",
        target_revision_id="rev_456",
        wait_for_completion=False,
    )
    # Check the status of the summary later
    summary_task = anaplan.alm.get_comparison_summary_task(summary_task.id)
    if summary_task.task_state == "COMPLETE":
        summary_content = anaplan.alm.get_comparison_summary(summary_task)
    ```
=== "Asynchronous"
    ```python
    summary_task = await anaplan.alm.create_comparison_summary(
        source_revision_id="rev_123",
        source_model_id="22222222222222222222222222222222",
        target_revision_id="rev_456",
        wait_for_completion=False,
    )
    # Check the status of the summary later
    summary_task = await anaplan.alm.get_comparison_summary_task(summary_task.id)
    if summary_task.task_state == "COMPLETE":
        summary_content = await anaplan.alm.get_comparison_summary(summary_task)
    ```

## Applications

### Deployment Pipeline

Here's an example of a complete deployment pipeline that creates a revision, syncs to production, and returns the comparison report. In production, you would want to handle errors and do something meaningful with the report, like saving it to a bucket as a change log.

=== "Synchronous"
    ```python
    def deploy_to_production(source_model_id: str, target_model_id: str) -> bytes:
        source_client = anaplan_sdk.Client(
            model_id=source_model_id,
            certificate="~/certs/anaplan.pem",
            private_key="~/keys/anaplan.pem",
        )
        target_client = anaplan_sdk.Client.from_existing(
            source_client, model_id=target_model_id
        )
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        source_revision = source_client.alm.create_revision(
            name=f"Production Deploy {now}",
            description="Automated production deployment",
        )
        target_revision = target_client.alm.get_latest_revision()
        report_task = target_client.alm.create_comparison_report(
            source_revision.id, source_model_id, target_revision.id
        )
        report = target_client.alm.get_comparison_report(report_task)
        target_client.alm.sync_models(
            source_revision.id, source_model_id, target_revision.id
        )
        return report
    ```
=== "Asynchronous"
    ```python
    async def deploy_to_production(
        source_model_id: str, target_model_id: str
    ) -> bytes:
        source_client = anaplan_sdk.AsyncClient(
            model_id=source_model_id,
            certificate="~/certs/anaplan.pem",
            private_key="~/keys/anaplan.pem",
        )
        target_client = anaplan_sdk.AsyncClient.from_existing(
            source_client, model_id=target_model_id
        )
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        source_revision, target_revision = await gather(
            source_client.alm.create_revision(
                name=f"Production Deploy {now}",
                description="Automated production deployment",
            ),
            target_client.alm.get_latest_revision(),
        )
        report_task = await target_client.alm.create_comparison_report(
            source_revision.id, source_model_id, target_revision.id
        )
        report, _ = await gather(
            target_client.alm.get_comparison_report(report_task),
            target_client.alm.sync_models(
                source_revision.id, source_model_id, target_revision.id
            ),
        )
        return report
    ```
