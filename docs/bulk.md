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

### One source | Multiple Actions

One of the most common patterns you'll find working with Anaplan is the *upload content -> import into list -> import
into module*. As a handwavy TL;DR, you can think of Lists as collections of Metadata and Modules as Tables holding the
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

### Multiple sources | One Action

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
await anaplan.upload_file(113000000000, b"Hello World!")
await anaplan.upload_file(113000000001, b"Hello World!")
await anaplan.run_action(118000000000)

```
