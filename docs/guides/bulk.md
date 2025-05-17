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

Clients are instantiated with the workspace, model and authentication information. There are two primary means of
Authentication.

#### Basic Authentication

Basic Authentication is unsuitable for Production. Anaplan password policies force password changes every 30, 60 or 90
days, depending on tenant settings, making this approach annoying to maintain and error-prone and is thus not
recommended for production.

=== "Synchronous"
    ```python
    import anaplan_sdk
    
    anaplan = anaplan_sdk.Client(
        workspace_id="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
        model_id="11111111111111111111111111111111",
        user_email="admin@company.com",
        password="my_super_secret_password",
    )
    ```

=== "Asynchronous"
    ```python
    import anaplan_sdk
    
    anaplan = anaplan_sdk.AsyncClient(
        workspace_id="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
        model_id="11111111111111111111111111111111",
        user_email="admin@company.com",
        password="my_super_secret_password",
    )
    ```

#### Certificate Authentication

=== "Synchronous"
    ```python
    import anaplan_sdk
    
    anaplan = anaplan_sdk.Client(
        workspace_id="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
        model_id="11111111111111111111111111111111",
        certificate="~/certs/anaplan.pem",
        private_key="~/keys/anaplan.pem",
        private_key_password="my_super_secret_password",
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
        private_key_password="my_super_secret_password",
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
    workspaces, models = (
        anaplan.list_workspaces(), anaplan.list_models()
    ) # Globals, this will work on an instance with auth info only
    
    imports, exports, actions, processes = (
        anaplan.list_imports(),
        anaplan.list_exports(),
        anaplan.list_actions(),
        anaplan.list_processes(),
    ) # These require an instance with workspace and model info
    ```
=== "Asynchronous"
    ```python
    workspaces, models = await gather(
        anaplan.list_workspaces(), anaplan.list_models()
    ) # Globals, this will work on an instance with auth info only
    
    imports, exports, actions, processes = await gather(
        anaplan.list_imports(),
        anaplan.list_exports(),
        anaplan.list_actions(),
        anaplan.list_processes(),
    ) # These require an instance with workspace and model info
    ```

### Importing data

=== "Synchronous"
    ```python
    anaplan.upload_and_import(113000000000, b"Hello Anaplan", 112000000000)
    
    # Or if you need more control, 
    # i.e. to upload multiple files or run things in between:
    anaplan.upload_file(113000000000, b"Hello Anaplan")
    ...
    anaplan.run_action(112000000000)
    ```
=== "Asynchronous"
    ```python
    await anaplan.upload_and_import(113000000000, b"Hello Anaplan", 112000000000)
    
    # Or if you need more control, 
    # i.e. to upload multiple files or run things in between:
    await anaplan.upload_file(113000000000, b"Hello Anaplan")
    ...
    await anaplan.run_action(112000000000)
    ```

### Exporting data

=== "Synchronous"
    ```python
    content = anaplan.export_and_download(116000000000)
    
    # Again, you can do this in multiple steps:
    anaplan.run_action(116000000000)
    ...
    content = anaplan.get_file(116000000000)
    ```
=== "Asynchronous"
    ```python
    content = await anaplan.export_and_download(116000000000)
    
    # Again, you can do this in multiple steps:
    await anaplan.run_action(116000000000)
    ...
    content = await anaplan.get_file(116000000000)
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

Conversely, some imports in Anaplan may need to happen in an atomic manner. For this too, we can apply a very similar
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

### Streaming Files (Larger than RAM)

If you have a file that is larger than your available RAM, or you are consuming chunks from i.e. a queue until it is
exhausted and thus cannot know the number of expected chunks ahead of time, you can use the `upload_file_stream` method.
You can pass an Iterator - in this case a Generator - that yields the chunks to this method, and it will handle the
rest. The `upload_file_stream` method on the [AsyncClient](../api/async/async_client.md#anaplan_sdk.AsyncClient.upload_file_stream)
accepts both `AsyncIterator[bytes | str]` and `Iterator[str | bytes]`.

This will work nicely with i.e. [`scan_parquet()`](https://docs.pola.rs/user-guide/io/parquet/#scan)
in [Polars](https://docs.pola.rs/). Consider the following example:

=== "Synchronous"
    ```python
    import polars as pl
    
    
    def read_file_in_chunks(chunk_size: int = 150_000):
        df = pl.scan_parquet("massive_data.parquet")
        row_count = df.select(pl.len()).collect().item()
        for i in range(0, row_count, chunk_size):
            yield df.slice(i, chunk_size).collect().write_csv()
    
    
    anaplan.upload_file_stream(113000000000, read_file_in_chunks())
    ```
=== "Asynchronous"
    ```python
    import polars as pl
    
    
    async def read_file_in_chunks(chunk_size: int = 150_000):
        df = pl.scan_parquet("massive_data.parquet")
        row_count = df.select(pl.len()).collect().item()
        for i in range(0, row_count, chunk_size):
            # WARNING: `collect_async()` is experimental
            yield (await df.slice(i, chunk_size).collect_async()).write_csv()
    
    
    await anaplan.upload_file_stream(113000000000, read_file_in_chunks())
    ```

This will allow you to upload files of arbitrary size without running into memory issues, as long as you keep the chunk
small enough to fit into memory. It will work equally well with any other source that can be read in chunks and
especially well with sources that can be read lazily or return the results sets in chunks by default.

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
