# `importlib.resources`
This repository is to house the design and implementation of a planned
`importlib.resources` module for Python's stdlib -- aiming for
Python 3.7 -- along with a backport to target Python 3.4 - 3.6.

The key goal of this module is to replace
[`pkg_resources`](https://setuptools.readthedocs.io/en/latest/pkg_resources.html)
with a solution in Python's stdlib that relies on well-defined APIs.
This should not only make reading resources included in packages easier,
but have the semantics be stable and consistent.

## Goals
- Provide a reasonable replacement for `pkg_resources.resource_stream()`
- Provide a reasonable replacement for `pkg_resources.resource_string()`
- Provide a reasonable replacement for `pkg_resources.resource_filename()`
- Define an ABC for loaders to implement for reading resources
- Implement this in the stdlib for Python 3.7
- Implement a package for PyPI which will work on Python >=3.4

## Non-goals
- Replace all of `pkg_resources`
- For what is replaced in `pkg_resources`, provide an **exact**
  replacement

# Design

## Low-level
For [`importlib.abc`](https://docs.python.org/3/library/importlib.html#module-importlib.abc):
```python
import abc
from typing.io import BinaryIO


class ResourceReader(abc.ABC):

    def open_resource(self, path: str) -> BinaryIO:
        """Return a file-like object opened for binary reading.

        The 'path' argument is expected to represent only a file name.
        If the resource cannot be found, FileNotFoundError is raised.
        """
        raise FileNotFoundError

    def resource_path(self, path: str) -> str:
        """Return the file system path to the specified resource.


        The 'path' argument is expected to represent only a file name.
        If the resource does not exist on the file system, raise
        FileNotFoundError.
        """
        raise FileNotFoundError
```

## High-level
For `importlib.resources`:
```python
import pathlib
import types
from typing import ContextManager, Union
from typing.io import BinaryIO


Package = Union[str, types.ModuleType]
FileName = Union[str, os.PathLike]


def open(package: Package, file_name: FileName) -> BinaryIO:
    """Return a file-like object opened for binary-reading of the resource."""
    ...


def read(package: Package, file_name: FileName, encoding: str = "utf-8",
         errors: str = "strict") -> str:
    """Return the decoded string of the resource.

    The decoding-related arguments have the same semantics as those of
    bytes.decode().
    """
    ...


@contextlib.contextmanager
def path(package: Package, file_name: FileName) -> ContextManager[pathlib.Path]:
    """A context manager providing a file path object to the resource.

    If the resource does not already exist on its own on the file system,
    a temporary file will be created. If the file was created, the file
    will be deleted upon exiting the context manager (no exception is
    raised if the file was deleted prior to the context manager
    exiting).
    """
    ...
```

If *package* is an actual package, it is used directly. Otherwise the
argument is used in calling `importlib.import_module()`. The found
package is expected to be an actual package, otherwise `TypeError` is
raised.

For the *file_name* argument, it is expected to be only a file name
with no other path parts. If any parts beyond a file name are found, a
`ValueError` will be raised. The expectation is that all data files
will exist within a directory that can be imported by Python as a
package.

All functions raise `FileNotFoundError` if the resource does not exist
or cannot be found.


# Open Issues
Please see the
[issue tracker](https://github.com/brettcannon/importlib_resources/issues).
