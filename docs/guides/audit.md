You can use the Audit API to get fine-grained information about the changes made to any model, usage, user sign-ins,
most frequently visited pages and much more. The Audit API exposes most the logs collected by Anaplan.

For details refer to
[the Documentation](https://auditservice.docs.apiary.io/#).

## Usage

The method for the Audit API reside in a different namespace for better API navigability and
comprehensiveness, but are accessible through the same client for convenience. For e.g., you can call
the `.get_events()` method like so:

/// tab | Synchronous

```python
import anaplan_sdk

anaplan = anaplan_sdk.Client(
    workspace_id="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    model_id="11111111111111111111111111111111",
    certificate="~/certs/anaplan.pem",
    private_key="~/keys/anaplan.pem",
)
events = anaplan.audit.get_events()
```

///
/// tab | Asynchronous

```python
import anaplan_sdk

anaplan = anaplan_sdk.AsyncClient(
    workspace_id="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    model_id="11111111111111111111111111111111",
    certificate="~/certs/anaplan.pem",
    private_key="~/keys/anaplan.pem",
)
events = await anaplan.audit.get_events()
```

///
