!!! tip "Client Settings"
      Anaplan SDK comes with a set of default options that are efficient for most use cases and general purpose. Mainly, it
      will compress all data before uploading and leverage Concurrency to speed up- and downloads. with a chunk size of 25MB.
      However, you can tune the client to better suit your needs. For more information,
      see [Client Parameters](client.md#anaplan_sdk.Client.__init__).

## Intro

When using this SDK you would never know it, but the workflow of performing an import of data into or export from
Anaplan is actually quite involved. To give you the full context and allow you to make informed choices, let's take a
look at the individual steps, how to perform them individually and how one can put these together to use the Bulk API to
the greatest efficiency.

Assuming you already know all the relevant Id's, the steps are:

/// tab | Import

1. Chunk your content. There is no enforced hard limit on chunk sizes, but there is a strong Recommendation to not
   exceed 50 MB and in practice you would be seeking to keep them smaller still. This SDK's default chunk size is 25 MB.
2. Set the chunk count, if you don't know this number ahead of time, set it to -1.
3. Upload all chunks
4. Mark the upload as complete. Only necessary if you set the count to -1 in step 2.
5. Trigger the import action. This will return a Task Id for the task you just spawned.
6. Poll the task status until the tasks completes.
7. Validate the task outcome.

///

/// tab | Export

1. Run the export.
2. Poll the task status until the tasks completes.
3. Get the file info and retrieve the chunk count.
4. Download all chunks.
5. Merge the chunks.

///

With this SDK, all of the above is condensed to:

/// tab | Synchronous

```python
anaplan = anaplan_sdk.Client(
    workspace_id="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    model_id="11111111111111111111111111111111",
    certificate="~/certs/anaplan.pem",
    private_key="~/keys/anaplan.pem",
)
anaplan.upload_and_import(113000000000, b"Hello World!", 118000000000)
export_content = anaplan.export_and_download(116000000000)
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
_, export_content = await gather(
    anaplan.upload_and_import(113000000000, b"Hello World!", 118000000000),
    anaplan.export_and_download(116000000000),
)
```

Here we can safely run the import and export concurrently, as they have no overlap in the files the reference. If they
did, this would be a terrible idea. See [this Chapter](bulk_vs_transactional.md/#the-bad) for details on this.

///

This standard case will typically cover most of your needs. Let's now look at some more involved examples, where you
may need some more control over the underlying files and actions to achieve a more efficient exchange.

## Applications

### One source with multiple Actions

One of the most common patterns you'll find working with Anaplan is the *upload content -> import into list -> import
into module*. As a hand-wavy TL;DR, you can think of Lists as collections of Metadata and Modules as Tables holding the
actual data. Importing into a list, you must provide a unique identifier, which will be stored in the list alongside
some additional information about this record you can add, and the module will then hold all the records for each id.
Since uploading the content the module and the list share twice would be redundant and inefficient, we want to group
those.

The easiest way to do this is to have your model builder create two actions that reference the same file, one importing
into the list and the other one importing into the module and then put them into a process. This would again just look
like this:

/// tab | Synchronous

```python
anaplan.upload_and_import(113000000000, b"Hello World!", 118000000000)
```

///
/// tab | Asynchronous

```python
await anaplan.upload_and_import(113000000000, b"Hello World!", 118000000000)
```

///

This is logically equivalent to:
/// tab | Synchronous

```python
anaplan.upload_file(113000000000, b"Hello World!")
anaplan.run_action(112000000000)  # Import into the List
anaplan.run_action(112000000001)  # Import into the Module
```

///
/// tab | Asynchronous

```python
await anaplan.upload_file(113000000000, b"Hello World!")
await anaplan.run_action(112000000000)  # Import into the List
await anaplan.run_action(112000000001)  # Import into the Module
```

///

This is by some margin the most efficient way to upload larger sets of data.

### Multiple sources and one Action

Conversely, some imports in Anaplan may need to happen in an atomic manner. For this too, we can apply a very similar
pattern:

/// tab | Synchronous

```python
anaplan.upload_file(113000000000, b"Hello World!")
anaplan.upload_file(113000000001, b"Hello World!")
anaplan.run_action(118000000000)
```

///
/// tab | Asynchronous

```python
await asyncio.gather(
    anaplan.upload_file(113000000000, b"Hello World!"),
    anaplan.upload_file(113000000001, b"Hello World!"),
)  # Concurrency is safe here, since the files are not overlapping
await anaplan.run_action(118000000000)

```

///

### Streaming Files (Larger than RAM)

If you have a file that is larger than your available RAM, or you are consuming chunks from i.e. a queue until it is
exhausted and thus cannot know the number of expected chunks ahead of time, you can use the `upload_file_stream` method.
You can pass an Iterator - in this case a Generator - that yields the chunks to this method, and it will handle the
rest. The `upload_file_stream` method on the [AsyncClient](async_client.md#anaplan_sdk.AsyncClient.upload_file_stream)
accepts both `AsyncIterator[bytes | str]` and `Iterator[str | bytes]`.

This will work nicely with i.e. [`scan_parquet()`](https://docs.pola.rs/user-guide/io/parquet/#scan)
in [Polars](https://docs.pola.rs/). Consider the following example:

/// tab | Synchronous

```python
import polars as pl


def read_file_in_chunks(chunk_size: int = 150_000):
    df = pl.scan_parquet("massive_data.parquet")
    row_count = df.select(pl.len()).collect().item()
    for i in range(0, row_count, chunk_size):
        yield df.slice(i, chunk_size).collect().write_csv()


anaplan.upload_file_stream(113000000000, read_file_in_chunks())
```

///
/// tab | Asynchronous

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

///

This will allow you to upload files of arbitrary size without running into memory issues, as long as you keep the chunk
small enough to fit into memory. It will work equally well with any other source that can be read in chunks and
especially well with sources that can be read lazily or return the results sets in chunks by default.


You can in the same way use the `download_file_stream` method to download files in chunks.

/// tab | Synchronous

```python
for chunk in anaplan.get_file_stream(113000000040):
   ...  # do something with the chunk
```

///
/// tab | Asynchronous

```python
async for chunk in anaplan.get_file_stream(113000000040):
    ...  # do something with the chunk
```

///
