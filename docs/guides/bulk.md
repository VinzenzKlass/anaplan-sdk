When using this SDK you would never know it, but the workflow of performing an import of data into or export from
Anaplan is actually quite involved. To give you the full context and allow you to make informed choices, let's take a
look at the individual steps, how to perform them individually and how one can put these together to use the Bulk API to
the greatest efficiency.

??? tip "Client Tuning"
    Anaplan SDK comes with a set of default options that are efficient for most use cases and general purpose. Mainly, it
    will compress all data before uploading and leverage Concurrency to accelerate up- and downloads, with a chunk size of 25MB.
    However, you can configure the client to better fit your needs. For more information,
    see [Client Parameters](../api/sync/sync_client.md#anaplan_sdk.Client.__init__).

## Basic Usage

### Instantiate a Client

Clients can be instantiated with just authentication information. This will give you access to all the 
non-model-specific APIs. For the Bulk API, you also need to provide the `workspace_id` and `model_id`. Here, we're 
using Certificate Authentication. You can read about other Authentication methods in the respective 
[Guide](authentication.md).

=== "Synchronous"
    ```python
    import anaplan_sdk

    anaplan = anaplan_sdk.Client(
        workspace_id="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
        model_id="11111111111111111111111111111111",
        certificate="~/certs/anaplan.pem",
        private_key="~/keys/anaplan.pem",
    )
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
    ```
### Listing Resources

You can list all the global resources available in the given users **default tenant**. You cannot list workspaces or 
models that reside in a different tenant. You can still instantiate a client for a different workspace and model, but 
you will need grab these IDs from the Anaplan UI or have them provided to you.

You can list model specific resources like imports, exports, actions and processes on any model, but you will need to
provide the workspace and model IDs.


=== "Synchronous"
    ```python
    # Globals, this will work on an instance with auth info only
    workspaces = anaplan.get_workspaces()
    models = anaplan.get_models()
    models_in_current_ws = anaplan.get_models(True) # This requires a workspace_id
    models_in_other_ws = anaplan.get_models("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
    
    # These require an instance with workspace and model info
    imports = anaplan.get_imports()
    exports = anaplan.get_exports()
    actions = anaplan.get_actions()
    processes = anaplan.get_processes()
    ```
=== "Asynchronous"
    ```python
    workspaces, models, models_in_current_ws, models_in_other_ws = await gather(
        anaplan.get_workspaces(), 
        anaplan.get_models(),
        anaplan.get_models(True), # This requires a workspace_id in
        anaplan.get_models("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
    ) # Globals, this will work on an instance with auth info only
    
    imports, exports, actions, processes = await gather(
        anaplan.get_imports(),
        anaplan.get_exports(),
        anaplan.get_actions(),
        anaplan.get_processes(),
    ) # These require an instance with workspace and model info
    ```

### Importing data

=== "Synchronous"
    ```python
    anaplan.upload_and_import(113000000000, b"Hello Anaplan", 112000000000)
    ```
    Or, if you need more control i.e. to upload multiple files or run things in between:
    ```python
    anaplan.upload_file(113000000000, b"Hello Anaplan")
    ...
    anaplan.run_action(112000000000)
    ```
=== "Asynchronous"
    ```python
    await anaplan.upload_and_import(113000000000, b"Hello Anaplan", 112000000000)
    ```
    Or, if you need more control i.e. to upload multiple files or run things in between:
    ```python
    await anaplan.upload_file(113000000000, b"Hello Anaplan")
    ...
    await anaplan.run_action(112000000000)
    ```

### Exporting data

=== "Synchronous"
    ```python
    content = anaplan.export_and_download(116000000000)
    ```
    Again, you can do this in multiple steps:
    ```python
    anaplan.run_action(116000000000)
    ...
    content = anaplan.get_file(116000000000)
    ```
=== "Asynchronous"
    ```python
    content = await anaplan.export_and_download(116000000000)
    ```
    Again, you can do this in multiple steps:
    ```python
    await anaplan.run_action(116000000000)
    ...
    content = await anaplan.get_file(116000000000)
    ```

### Optimizer Logs

You can download the Optimizer Logs from Anaplan. This will give you the Solution Logs produced by Gurobi, which can be
very useful for debugging and understanding the performance of your Optimizer models.

=== "Synchronous"
    ```python
    log = anaplan.get_optimizer_log(
        117000000000, "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    )
    ```
=== "Asynchronous"
    ```python
    log = await anaplan.get_optimizer_log(
        117000000000, "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    )
    ```

## Applications

### One source with multiple Actions

One of the most common patterns you'll find working with Anaplan is:

1. Upload content
2. Import into a list
3. Import into a module

The recommended way to do this is to have your model builder create two actions that reference the same file, one
importing into the list and the other one importing into the module and then wrap them into a process. This would again
just look like this:

??? danger "Processes are not atomic"
    Please note that Anaplan Processes are not like Transactions in Databases, i.e. they are not atomic, and they will
    not roll back if one of the actions fails. This means that if you run a process that contains multiple actions, and
    one of them fails, all changes of all other actions that ran before the failure are permanently applied.

=== "Synchronous"
    ```python
    anaplan.upload_and_import(
        file_id=113000000000, content=b"Hello World!", action_id=118000000000
    )
    ```
=== "Asynchronous"
    ```python
    await anaplan.upload_and_import(
        file_id=113000000000, content=b"Hello World!", action_id=118000000000
    )
    ```

This is logically equivalent to:

=== "Synchronous"
    ```python
    anaplan.upload_file(113000000000, b"Hello World!")
    anaplan.run_action(112000000000)  # Import into the List
    anaplan.run_action(112000000001)  # Import into the Module
    ```
=== "Asynchronous"
    ```python
    await anaplan.upload_file(113000000000, b"Hello World!")
    await anaplan.run_action(112000000000)  # Import into the List
    await anaplan.run_action(112000000001)  # Import into the Module
    ```

This is by some margin the most efficient way to upload larger sets of data.

### Multiple sources and one Action

Conversely, some imports in Anaplan may need to read from several files. For this too, we can apply a very similar
pattern:

=== "Synchronous"
    ```python
    anaplan.upload_file(113000000000, b"Hello World!")
    anaplan.upload_file(113000000001, b"Hello World!")
    anaplan.run_action(118000000000)
    ```
=== "Asynchronous"
    ```python
    await asyncio.gather(
        anaplan.upload_file(113000000000, b"Hello World!"),
        anaplan.upload_file(113000000001, b"Hello World!"),
    )  # Concurrency is safe here, since the files are not overlapping
    await anaplan.run_action(118000000000)
    ```

---

### Streaming Files (Larger than RAM)

If you have a file that is larger than your available RAM, or you are consuming chunks from a queue, you can use the 
`upload_file_stream` method. You can pass a Generator that yields the chunks to this method, and it will handle the
rest. The `upload_file_stream` method on the [AsyncClient](../api/async/async_client.md#anaplan_sdk.AsyncClient.upload_file_stream)
accepts both `AsyncIterator[bytes | str]` and `Iterator[str | bytes]`.

Let's say you want to analyze the popular NYC Taxi dataset of ~170 million rows in Anaplan, you could use the following 
code to stream the data to Anaplan. 

=== "Synchronous"
    ```python
    import polars as pl
    
    
    def stream_file(chunk_size: int = 50_000):
        url = "s3://datasets-documentation/nyc-taxi/trips*.parquet"
        options = {"aws_region": "eu-west-3", "skip_signature": "true"}
        df = pl.scan_parquet(url, storage_options=options)
        for i in range(0, df.select(pl.len()).collect().item(), chunk_size):
            chunk = df.slice(i, chunk_size).collect(engine="streaming")
            yield chunk.write_csv(include_header=i == 0)
    
    
    anaplan.upload_file_stream(113000000000, stream_file(), batch_size=3)
    ```
=== "Asynchronous"
    ```python
    import polars as pl


    async def stream_file(chunk_size: int = 50_000):
        url = "s3://datasets-documentation/nyc-taxi/trips*.parquet"
        options = {"aws_region": "eu-west-3", "skip_signature": "true"}
        df = pl.scan_parquet(url, storage_options=options)
        for i in range(0, df.select(pl.len()).collect().item(), chunk_size):
            # WARNING: `collect_async()` is experimental
            chunk = await df.slice(i, chunk_size).collect_async(engine="streaming")
            yield chunk.write_csv(include_header=i == 0)
    

    await anaplan.upload_file_stream(113000000000, stream_file(), batch_size=3)
    ```

This will allow you to upload files of arbitrary size without running into memory issues, as long as you keep the chunks
and `batch_size` (= the number of chunks that are read and uploaded concurrently) small enough to fit into memory. It 
will work equally well with any other source that can be read in chunks and especially well with sources that can be read lazily or return the results sets in chunks by default.

You can in the same way use the `get_file_stream` method to download files in chunks.

=== "Synchronous"
    ```python
    for chunk in anaplan.get_file_stream(113000000040):
        ...  # do something with the chunk
    ```
=== "Asynchronous"
    ```python
    async for chunk in anaplan.get_file_stream(113000000040):
        ...  # do something with the chunk
    ```
