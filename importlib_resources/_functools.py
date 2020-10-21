from __future__ import absolute_import

import functools
import contextlib


def defer(func):
    """
    Decorate a function that returns a context manager to
    cause its execution to be deferred until the context
    is entered.
    """
    @functools.wraps(func)
    @contextlib.contextmanager
    def wrapper(*args, **kwargs):
        with func(*args, **kwargs) as res:
            yield res
    return wrapper
