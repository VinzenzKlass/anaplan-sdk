You can use the Audit API to get fine-grained information about the changes made to any model, usage, user sign-ins,
most frequently visited pages and much more. The Audit API exposes most the logs collected by Anaplan.

For API details refer to
[the Documentation](https://auditservice.docs.apiary.io/#).

## Usage

!!! tip "Tenant Level API"
    Note the absence of `workspace_id` and `model_id` in the Audit API. The Audit API is a tenant level API, meaning it
    is not scoped to a specific workspace or model. You can use the Audit API to get information about all workspaces and
    models for the default tenant of the user you are providing the credentials for.

The methods for the Audit API reside in a different namespace for better API navigability and
comprehensiveness, but are accessible through the same client for convenience. For e.g., you can call
the `.get_events()` method like so:

/// tab | Synchronous

```python
import anaplan_sdk

anaplan = anaplan_sdk.Client(
    certificate="~/certs/anaplan.pem", private_key="~/keys/anaplan.pem"
)
events = anaplan.audit.get_events()
```

///
/// tab | Asynchronous

```python
import anaplan_sdk

anaplan = anaplan_sdk.AsyncClient(
    certificate="~/certs/anaplan.pem", private_key="~/keys/anaplan.pem"
)
events = await anaplan.audit.get_events()
```

///

The Audit API also exposes the `list_users()` method to get a list of all users in the workspace. You can for e.g. use
the two methods in combination to get a list of events with the username using [polars](https://docs.pola.rs):

/// tab | Synchronous

```python
import polars as pl

events, users = anaplan.audit.get_events(14), anaplan.audit.list_users()
df = pl.DataFrame(events, orient="row", infer_schema_length=1_000).join(
    pl.DataFrame(users, orient="row").select(
        pl.col("id").alias("userId"), "first_name", "last_name"
    ),
    on="userId",
    how="left",
)
```

///
/// tab | Asynchronous

```python
import polars as pl

events, users = await gather(
    anaplan.audit.get_events(14), anaplan.audit.list_users()
)
df = pl.DataFrame(events, orient="row", infer_schema_length=1_000).join(
    pl.DataFrame(users, orient="row").select(
        pl.col("id").alias("userId"), "first_name", "last_name"
    ),
    on="userId",
    how="left",
)
```

///


