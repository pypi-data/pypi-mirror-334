import functools
import inspect
import os
import typing

from vw import config

_TEST_FILE_NAMES = [
    # pytest
    os.path.join("pytest", "__main__.py"),
    os.path.join("pytest.exe", "__main__.py"),
    os.path.join("_pytest", "main.py"),
    # unittest
    os.path.join("unittest", "__main__.py"),
    os.path.join("unittest", "main.py"),
    # doctest
    os.path.join("lib", "doctest.py"),
]


def _is_test_framework_file(filename: str) -> bool:
    """Determine if a file is a test framework file.

    Args:
        filename (str): The name of the file to check.

    Returns:
        bool: True if the file is a test framework file, False otherwise.
    """
    return any([filename.endswith(file) for file in _TEST_FILE_NAMES])


@functools.lru_cache(maxsize=1)
def stack_trace() -> typing.List[str]:
    """Get the current stack trace.

    Based on https://docs.python.org/3/library/inspect.html, make sure to delete the
    stack object to avoid a reference cycle.

    Returns:
        List[str]: The current stack trace as a list of filenames.
    """
    stack = inspect.stack()
    result = list()
    for frame in stack:
        result.append(frame.filename)
        del frame  # Avoid a reference cycle
    del stack
    return result


@functools.lru_cache(maxsize=1)
def is_test_env():
    """Use the inspect module to determine if the current environment is a test environment.

    Note: The calling module expected to not change, so it is assumed that
    an entire Python run will have the same answer.

    Environment variables (first set wins):
        VW_IGNORE -> if configured as true, this always returns false
        VW_ALWAYS -> if set, always returns this value (can be set to true or false)

    Returns:
        bool: True if the current environment is a test environment, False otherwise.

    >>> is_test_env() # Doctest should be true as well
    True
    """
    if config.VW_IGNORE:
        return False
    if config.VW_ALWAYS is not None:
        return config.VW_ALWAYS

    result = any(_is_test_framework_file(filename) for filename in reversed(stack_trace()))
    return result


if __name__ == "__main__":
    print(is_test_env())
