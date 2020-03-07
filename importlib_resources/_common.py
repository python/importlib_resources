from __future__ import absolute_import

import os
import types
import tempfile
import importlib
import contextlib

from ._compat import (
    Path, package_spec, FileNotFoundError, ZipPath,
    singledispatch, suppress, string_types, is_package,
    )

try:
    from typing import Any
except Exception:  # pragma: nocover
    pass


def from_package(package):
    """
    Return a Traversable object for the given package.

    """
    spec = package_spec(package)
    return from_traversable_resources(spec) or fallback_resources(spec)


def from_traversable_resources(spec):
    """
    If the spec.loader implements TraversableResources,
    directly or implicitly, it will have a ``files()`` method.
    """
    with suppress(AttributeError):
        return spec.loader.files()


def fallback_resources(spec):
    package_directory = Path(spec.origin).parent
    try:
        archive_path = spec.loader.archive
        rel_path = package_directory.relative_to(archive_path)
        return ZipPath(archive_path, str(rel_path) + '/')
    except Exception:
        pass
    return package_directory


@contextlib.contextmanager
def _tempfile(reader):
    # Not using tempfile.NamedTemporaryFile as it leads to deeper 'try'
    # blocks due to the need to close the temporary file to work on Windows
    # properly.
    fd, raw_path = tempfile.mkstemp()
    try:
        os.write(fd, reader())
        os.close(fd)
        yield Path(raw_path)
    finally:
        try:
            os.remove(raw_path)
        except FileNotFoundError:
            pass


@singledispatch
@contextlib.contextmanager
def as_file(path):
    """
    Given a Traversable object, return that object as a
    path on the local file system in a context manager.
    """
    with _tempfile(path.read_bytes) as local:
        yield local


@as_file.register(Path)
@contextlib.contextmanager
def _(path):
    """
    Degenerate behavior for pathlib.Path objects.
    """
    yield path


def _normalize_path(path):
    # type: (Any) -> str
    """Normalize a path by ensuring it is a string.

    If the resulting string contains path separators, an exception is raised.
    """
    str_path = str(path)
    parent, file_name = os.path.split(str_path)
    if parent:
        raise ValueError("{!r} must be only a file name".format(path))
    return file_name


def _resolve(name):
    # (Any) -> ModuleType
    """If name is a string, resolve to a module."""
    return (
        importlib.import_module(name)
        if isinstance(name, string_types) else
        name
        )


def _get_package(package):
    # type: (Any) -> types.ModuleType
    """Take a package name or module object and return the module.

    If a name, the module is imported.  If the resolved module
    object is not a package, raise an exception.
    """
    module = _resolve(package)
    if not is_package(module):
        raise TypeError("{!r} is not a package".format(package))
    return module
