"""Decorators that don't evaluate until they are first invoked."""

import functools

from vw import _utils


def no_op(func):
    """Decorator to make a function no-op if the current environment is a test environment.

    Args:
        func (function): The function to decorate.

    Returns:
        function: The decorated function.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if _utils.is_test_env():
            return
        return func(*args, **kwargs)

    return wrapper


def tests_only(func):
    """Decorator to make a function only run if the current environment is a test environment.

    Args:
        func (function): The function to decorate.

    Returns:
        function: The decorated function.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not _utils.is_test_env():
            return
        return func(*args, **kwargs)

    return wrapper
