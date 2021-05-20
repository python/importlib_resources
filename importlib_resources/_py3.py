import os
import io

from . import _common
from contextlib import suppress
from pathlib import Path
from types import ModuleType
from typing import ContextManager, Union
from collections.abc import Sequence
from functools import singledispatch

Package = Union[str, ModuleType]
Resource = Union[str, os.PathLike]


def path(
    package: Package,
    resource: Resource,
) -> 'ContextManager[Path]':
    """A context manager providing a file path object to the resource.

    If the resource does not already exist on its own on the file system,
    a temporary file will be created. If the file was created, the file
    will be deleted upon exiting the context manager (no exception is
    raised if the file was deleted prior to the context manager
    exiting).
    """
    reader = _common.get_resource_reader(_common.get_package(package))
    return (
        _path_from_reader(reader, _common.normalize_path(resource))
        if reader
        else _common.as_file(
            _common.files(package).joinpath(_common.normalize_path(resource))
        )
    )


def _path_from_reader(reader, resource):
    return _path_from_resource_path(reader, resource) or _path_from_open_resource(
        reader, resource
    )


def _path_from_resource_path(reader, resource):
    with suppress(FileNotFoundError):
        return Path(reader.resource_path(resource))


def _path_from_open_resource(reader, resource):
    saved = io.BytesIO(reader.open_resource(resource).read())
    return _common._tempfile(saved.read, suffix=resource)


def is_resource(package: Package, name: str) -> bool:
    """True if `name` is a resource inside `package`.

    Directories are *not* resources.
    """
    package = _common.get_package(package)
    _common.normalize_path(name)
    reader = _common.get_resource_reader(package)
    if reader is not None:
        return reader.is_resource(name)
    package_contents = set(_common.contents(package))
    if name not in package_contents:
        return False
    return (_common.from_package(package) / name).is_file()


@singledispatch
def _ensure_sequence(iterable):
    return list(iterable)


@_ensure_sequence.register(Sequence)
def _(iterable):
    return iterable
