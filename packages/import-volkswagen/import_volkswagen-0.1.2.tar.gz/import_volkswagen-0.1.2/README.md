# VW

This module provides decorators that turn on or off the decorated method depending on 
whether it is running in a testing environment or not.

**NOTE**: The name `vw` was chosen for convenience and is not intended as commentary on any political topic real or imagined.

# Why?

Have you ever found yourself wanting an easy way to turn off the logging when running in tests?

What about database access?

[Mocking](https://docs.python.org/3/library/unittest.mock.html) works well for your own code, but what about when a user imports your library?

This is what this tool is meant to solve.

# Controlling

By using [python-decouple](https://pypi.org/project/python-decouple/), the following variables can be set in a `settings.ini` file, or a `.env` file, or as variables in the environment.

- `VW_IGNORE` -> causes VW to ignore if it is in a test environment (`no_op` still acts, and `tests_only` will not)
- `VW_ALWAYS` -> (NOTE: `VW_IGNORE` takes precedence over this var) causes VW to behave like it is always in a test environment (`no_op` is always a no-op)

# Examples

1. Using an in-memory db for tests:

    ```python
    import sqlite3

    import vw

    _con = sqlite3.connect(":memory:" if vw.is_test_env() else "database.sqlite3")
    ```

1. Logging to a local file for tests

    ```python
    import logging

    import vw

    _root_logger = logging.getLogger(None)
    _root_logger.addHandler(logging.FileHandler("test.log" if vw.is_test_env() else "//path/to/server/log.txt"))
    ```

1. Avoid doing things in unit/component/integration tests that should only be done in production

    ```python
    import requests
    import vw

    @vw.no_op
    def send_tornado_warning():
        requests.post(...)
    ```
