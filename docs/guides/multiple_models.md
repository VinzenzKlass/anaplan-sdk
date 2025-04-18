If you find yourself working with several Models at the same time, you will want to reuse a Client Instance instead of
creating an entirely new one. This will be more efficient by avoiding duplicate authentication and sharing underlying
resources that can safely be shared. For this Purpose, you can use the `from_existing()` Class method:

/// tab | Synchronous

```python
anaplan = anaplan_sdk.Client(
    workspace_id="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    model_id="11111111111111111111111111111111",
    certificate="~/certs/anaplan.pem",
    private_key="~/keys/anaplan.pem",
)
other = anaplan_sdk.Client.from_existing(
    anaplan, "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB", "22222222222222222222222222222222"
)
```

///

/// tab | Asynchronous

```python
anaplan = anaplan_sdk.AsyncClient(
    workspace_id="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    model_id="11111111111111111111111111111111",
    certificate="~/certs/anaplan.pem",
    private_key="~/keys/anaplan.pem",
)
other = anaplan_sdk.AsyncClient.from_existing(
    anaplan, "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB", "22222222222222222222222222222222"
)
```

///
