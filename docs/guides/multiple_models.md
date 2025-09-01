--- 
hide:
    - toc
--- 

If you find yourself working with several Models at the same time, you will want to reuse a Client Instance instead of
creating an entirely new one. This is both syntactically nicer and more efficient by avoiding duplicate authentication 
and sharing underlying resources that can safely be shared. For this Purpose, you can use the `with_model()` method. 
You can optionally pass a new Workspace ID and Model ID to this method. If you omit the Workspace ID - the second 
argument - the existing one will be used.

=== "Synchronous"
    ```python
    anaplan = Client(
        workspace_id="8a81b09d599f3c6e0159f605560c2630",
        model_id="8896D8C366BC48E5A3182B9F5CE10526",
        certificate=getenv("ANAPLAN_CERT"),
        private_key=getenv("ANAPLAN_PK"),
    )
    other = anaplan.with_model("22222222222222222222222222222222")  # Updates the Model Id
    other_ws = anaplan.with_model(
        "22222222222222222222222222222222", "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"
    )  # Updates the Model Id and the Workspace Id  
    ```
=== "Asynchronous"
    ```python
    anaplan = AsyncClient(
        workspace_id="8a81b09d599f3c6e0159f605560c2630",
        model_id="8896D8C366BC48E5A3182B9F5CE10526",
        certificate=getenv("ANAPLAN_CERT"),
        private_key=getenv("ANAPLAN_PK"),
    )
    other = anaplan.with_model("22222222222222222222222222222222")  # Updates the Model Id
    other_ws = anaplan.with_model(
        "22222222222222222222222222222222", "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"
    )  # Updates the Model Id and the Workspace Id
    ```
