If you need visibility of the internal behaviour of `anaplan_sdk`, you can use the built-in logging module. `anaplan_sdk` will log network errors, retries, as well as information about internal functionalities.

Consider this example:

```
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

```
logging.getLogger("anaplan_sdk").setLevel(logging.CRITICAL)
```

You can do the same using dictionary configuration for logging just as well.

If you need Information about the actual HTTP Requests sent, you can set the log level for the underlying [httpx](https://www.python-httpx.org/) library:

```
logging.getLogger("httpx").setLevel(logging.INFO)
```

To get a more detailed view on the internal workings of `anaplan_sdk`, you can set the log level to `DEBUG`:

```
logging.getLogger("anaplan_sdk").setLevel(logging.DEBUG)
```
