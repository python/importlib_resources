from __future__ import absolute_import

# flake8: noqa

import functools
import warnings
import contextlib

try:
    from pathlib import Path, PurePath
except ImportError:
    from pathlib2 import Path, PurePath                         # type: ignore


try:
    from functools import singledispatch
except ImportError:
    from singledispatch import singledispatch                   # type: ignore


try:
    from abc import ABC                                         # type: ignore
except ImportError:
    from abc import ABCMeta

    class ABC(object):                                          # type: ignore
        __metaclass__ = ABCMeta


try:
    FileNotFoundError = FileNotFoundError                       # type: ignore
except NameError:
    FileNotFoundError = OSError                                 # type: ignore


try:
    IsADirectoryError = IsADirectoryError                       # type: ignore
except NameError:
    IsADirectoryError = OSError                                 # type: ignore


try:
    from importlib import metadata
except ImportError:
    import importlib_metadata as metadata  # type: ignore


try:
    from zipfile import Path as ZipPath  # type: ignore
except ImportError:
    from zipp import Path as ZipPath


class PackageSpec(object):
	def __init__(self, **kwargs):
		vars(self).update(kwargs)


def package_spec(package):
	return getattr(package, '__spec__', None) or \
		PackageSpec(
			origin=package.__file__,
			loader=getattr(package, '__loader__', None),
		)


def allow_dirs(orig):
    """
    In #85, this project learned of an unexpected feature that
    would expose directories as resources. This function provides
    temporary compatibility for that expectation.
    """
    @functools.wraps(orig)
    @contextlib.contextmanager
    def wrapper(package, resource):
        try:
            with orig(package, resource) as res:
                yield res
        except IsADirectoryError:
            warnings.warn(
                "Retrieving directories with path() is not supported. "
                "Use files instead.",
                DeprecationWarning,
                )
            from importlib_resources import files
            yield files(package).joinpath(resource)

    return wrapper
