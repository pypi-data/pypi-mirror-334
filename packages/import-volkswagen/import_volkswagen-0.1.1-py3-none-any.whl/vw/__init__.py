"""Decorators no-op or be active depending on whether or not it is in a testing environment."""

import functools

from vw import _utils, config, lazy


@functools.wraps(_utils.is_test_env)
def is_test_env():
    """Return if it is a test environment."""
    return _utils.is_test_env()


def clear_env_cache():
    """Clear the cache value of whether it is a test environment or not."""
    _utils.is_test_env.cache_clear()
    _utils.stack_trace.cache_clear()


def no_op(func):
    """Decorator to make a function a no-op if the current environment is a test environment.

    Args:
        func (function): The function to decorate.

    Returns:
        function: The decorated function.
    """
    if is_test_env():

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # print("no_op wrapper called -> no op")
            return None

    else:

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # print("no_op wrapper called -> doing it")
            return func(*args, **kwargs)

    return wrapper


def tests_only(func):
    """Decorator to make a function a no-op if the current environment is a test environment.

    Args:
        func (function): The function to decorate.

    Returns:
        function: The decorated function.
    """
    if is_test_env():

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

    else:

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return None

    return wrapper


__all__ = [
    config.__name__,
    clear_env_cache.__name__,
    no_op.__name__,
    tests_only.__name__,
    lazy.__name__,
    is_test_env.__name__,
]
