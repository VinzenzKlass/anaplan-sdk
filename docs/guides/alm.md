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
      lists = anaplan.alm.get_revisions()
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
      lists = await anaplan.alm.get_revisions()
      ```

For brevity, if you need to access only the ALM API or need to do so repeatedly, you can assign the
ALM Client to its own variable.

=== "Synchronous"
      ```python
      anaplan = anaplan_sdk.Client(
          workspace_id="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
          model_id="11111111111111111111111111111111",
          certificate="~/certs/anaplan.pem",
          private_key="~/keys/anaplan.pem",
      )
      alm = anaplan.alm
      revisions = alm.get_revisions()
      syncs = alm.get_sync_tasks()
      ```
=== "Asynchronous"
      ```python
      import asyncio
      
      anaplan = anaplan_sdk.AsyncClient(
          workspace_id="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
          model_id="11111111111111111111111111111111",
          certificate="~/certs/anaplan.pem",
          private_key="~/keys/anaplan.pem",
      )
      alm = anaplan.alm
      revisions, syncs = await asyncio.gather(
          alm.get_revisions(), alm.get_sync_tasks()
      )
      ```
 
!!! note
      While you can instantiate a [Client](../api/sync/client.md) without the workspace or model parameters, trying to access
      the [Transactional Client](../api/sync/transactional_client.md) on an instance without the `model_id` will raise a `ValueError`.
