!!! tip "TL;DR"
    Use the [Bulk APIs](bulk.md) for larger (>5k rows), efficient data ingress or egress, or if you're looking to automate
    some logic through for e.g. processes and other Anaplan mechanisms already in place. For everything else, have a look at
    the [Transactional APIs](transactional.md) first.

This section focuses on explaining the different APIs and implications thereof. If you're looking for specific use cases
and code snippets, consult the respective Guide.

## The Bulk API

The Bulk API is the "traditional" API of Anaplan. It closely reflects the way Anaplan handles data and related
workflows. The *upload a file, then call an import on it* - or the reverse thereof for exports - workflow is
essentially a step-wise automation of what a model builder would de when manually uploading new data to Anaplan.

This Workflow may feel unintuitive to a developer at first and is perhaps unconventional, but it does have upsides
over the Transactional API as well.

### The Good

- Data can be CSV serialized and compressed for transfer, making it comparatively efficient.
- Data can be reused across several imports, avoiding redundant work.
- Import Actions are a very powerful abstraction over the Anaplan Internal Data Formats, abstracting away a lot of
  potential work from developers:
    - Can build hierarchies out of flat data
    - Can incur mapping of columns to dimensions in Anaplan, both on name and index
    - Defaults to an Upsert-like behaviour, which can be very convenient
    - Can convert types, parse dates and incur other transformation overhead

In essence, once you get used to this workflow and gain an understanding of how Actions work and what they can do,
you can use them to great effect, and they can abstract away a lot of work from the developer.

### The Bad

There are, however, also some noteworthy Footguns, first and foremost the fact that Anaplan **does not acquire a lock
when reading from a file**, meaning that you can upload a file, start an Import that uses this file a source and then -
while the import is reading from that file - overwrite that file with other content. The best you can hope for in this
case is an import error. If the new data you overwrote the file with happens to be compatible with whatever data the
import was expecting, can produce highly erroneous results without producing an error. There are easy ways to avoid this
of course, but it is a massive Footgun nonetheless, especially because of the lack of documentation around this issue.

Further, there can be cases when an import completes successfully but includes warnings. These warnings can be hard to
understand and very tedious to resolve, especially because some of them are perfectly fine, while others are indeed
cause for concern. It can be hard for a developer who does not have experience with Anaplan to make sense of these and
decide
on a resolution strategy, at which point a long and iterative process between the developer and model builder may
ensue.

### Conclusion

The Bulk API is the main way to import and export data to and from Anaplan, and it allows doing so fairly efficiently
while providing powerful features and abstractions through Import Actions. The Problems that may manifest can be
critical and hard to resolve, but are always solvable and with some experience, one can quickly develop a good intuition
on how to best design workflows to exchange Data with Anaplan efficiently while avoiding pitfalls.

## The Transactional API

The Transactional API is a more standard, JSON oriented REST-API a developer may expect. It accepts and mostly returns
JSON, allows targeting individual cells in a module (think of it as a table if you're not familiar), provides
synchronous responses and enables invoking extended functionality on the Anaplan platform beyond shuffling data around.

Since this API works and behaves much more like an API a developer may expect, there are fewer things to explain and
point out, so we can skip to the conclusion directly:

- Great granularity of control
- Many features, can import and export data as well as retrieve a large number of information about data and structures
  residing in Anaplan
- Less efficient for large transfers
- If used for larger transfers or overused, the Transactional API will prove a very reliable way to completely clutter
  the Anaplan internal logs and make them massively painful to read and extract information from.
- Greater Developer convenience - even though this SDK largely closes this gap. This is great, but also a possible
  Footgun, as it leads to this API being used, when the five minutes of effort to shift the work to the Bulk API would
  definitely have been a good investment.

