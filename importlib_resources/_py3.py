import os
import sys

from . import trees
from importlib import import_module
from types import ModuleType
from typing import Iterable, Iterator, Optional, Set, Union   # noqa: F401


Package = Union[ModuleType, str]
if sys.version_info >= (3, 6):
    Resource = Union[str, os.PathLike]              # pragma: <=35
else:
    Resource = str                                  # pragma: >=36


def _resolve(name) -> ModuleType:
    """If name is a string, resolve to a module."""
    if hasattr(name, '__spec__'):
        return name
    return import_module(name)


def _get_package(package) -> ModuleType:
    """Take a package name or module object and return the module.

    If a name, the module is imported.  If the resolved module
    object is not a package, raise an exception.
    """
    module = _resolve(package)
    if module.__spec__.submodule_search_locations is None:
        raise TypeError('{!r} is not a package'.format(package))
    return module


def files(package: Package) -> trees.Traversable:
    """
    Get a Traversable resource from a package
    """
    return trees.from_package(_get_package(package))
