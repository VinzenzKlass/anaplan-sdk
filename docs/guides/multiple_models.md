If you find yourself working with several Models at the same time, you will want to reuse a Client Instance instead of
creating an entirely new one. This will be more efficient by avoiding duplicate authentication and sharing underlying
resources that can safely be shared. For this Purpose, you can use the `from_existing()` Class method. You can 
optionally pass a new Workspace ID and Model ID to this method. If you omit the Workspace ID, the existing one will be used. If you omit both, the new client will be an identical copy of the existing one.

=== "Synchronous"
    ```python
    anaplan = anaplan_sdk.Client(
        workspace_id="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
        model_id="11111111111111111111111111111111",
        certificate="~/certs/anaplan.pem",
        private_key="~/keys/anaplan.pem",
    )
    other = anaplan_sdk.Client.from_existing(
        anaplan,
        workspace_id="BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
        model_id="22222222222222222222222222222222",
    )
    ```
=== "Asynchronous"
    ```python
    anaplan = anaplan_sdk.AsyncClient(
        workspace_id="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
        model_id="11111111111111111111111111111111",
        certificate="~/certs/anaplan.pem",
        private_key="~/keys/anaplan.pem",
    )
    other = anaplan_sdk.AsyncClient.from_existing(
        anaplan,
        workspace_id="BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
        model_id="22222222222222222222222222222222",
    )
    ```
