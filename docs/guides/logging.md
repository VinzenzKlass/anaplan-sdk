If you need visibility of the internal behaviour of `anaplan_sdk`, you can use the built-in logging
module. `anaplan_sdk` will log network requests, retries, as well as information about internal functionalities.

Consider this example:

```python
import logging

logging.basicConfig(
    format="%(levelname)s\t%(asctime)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8",
    level=logging.INFO,
)
```

This will output information to the console. If you have redirected `stdout`, it will be redirected accordingly.

To configure the log level independently of the logging for your app, you can use the following line:

```python
logging.getLogger("anaplan_sdk").setLevel(logging.CRITICAL)
```

You can do the same using dictionary configuration for logging just as well.

If you need Information about the actual HTTP Requests sent, you can set the log level for the
underlying [httpx](https://www.python-httpx.org/) library:

```python
logging.getLogger("httpx").setLevel(logging.INFO)
```
