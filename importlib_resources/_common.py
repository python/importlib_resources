import os
import pathlib
import tempfile
import functools
import contextlib
import types
import importlib

from typing import Union, Optional
from .abc import ResourceReader, Traversable

from ._compat import wrap_spec

Package = Union[types.ModuleType, str]


def files(package):
    # type: (Package) -> Traversable
    """
    Get a Traversable resource from a package
    """
    return from_package(get_package(package))


def get_resource_reader(package):
    # type: (types.ModuleType) -> Optional[ResourceReader]
    """
    Return the package's loader if it's a ResourceReader.
    """
    # We can't use
    # a issubclass() check here because apparently abc.'s __subclasscheck__()
    # hook wants to create a weak reference to the object, but
    # zipimport.zipimporter does not support weak references, resulting in a
    # TypeError.  That seems terrible.
    spec = package.__spec__
    reader = getattr(spec.loader, 'get_resource_reader', None)  # type: ignore
    if reader is None:
        return None
    return reader(spec.name)  # type: ignore


def resolve(cand):
    # type: (Package) -> types.ModuleType
    return cand if isinstance(cand, types.ModuleType) else importlib.import_module(cand)


def get_package(package):
    # type: (Package) -> types.ModuleType
    """Take a package name or module object and return the module.

    Raise an exception if the resolved module is not a package.
    """
    resolved = resolve(package)
    if wrap_spec(resolved).submodule_search_locations is None:
        raise TypeError(f'{package!r} is not a package')
    return resolved


def from_package(package):
    """
    Return a Traversable object for the given package.

    """
    spec = wrap_spec(package)
    reader = spec.loader.get_resource_reader(spec.name)
    return reader.files()


@contextlib.contextmanager
def _tempfile(
    reader,
    suffix='',
    # gh-93353: Keep a reference to call os.remove() in late Python
    # finalization.
    *,
    _os_remove=os.remove,
):
    # Not using tempfile.NamedTemporaryFile as it leads to deeper 'try'
    # blocks due to the need to close the temporary file to work on Windows
    # properly.
    fd, raw_path = tempfile.mkstemp(suffix=suffix)
    try:
        try:
            os.write(fd, reader())
        finally:
            os.close(fd)
        del reader
        yield pathlib.Path(raw_path)
    finally:
        try:
            _os_remove(raw_path)
        except FileNotFoundError:
            pass


@functools.singledispatch
def as_file(path):
    """
    Given a Traversable object, return that object as a
    path on the local file system in a context manager.
    """
    return _tempfile(path.read_bytes, suffix=path.name)


@as_file.register(pathlib.Path)
@contextlib.contextmanager
def _(path):
    """
    Degenerate behavior for pathlib.Path objects.
    """
    yield path


@contextlib.contextmanager
def _temp_path(dir: tempfile.TemporaryDirectory):
    """
    Wrap tempfile.TemporyDirectory to return a pathlib object.
    """
    with dir as result:
        yield pathlib.Path(result)


@contextlib.contextmanager
def _as_tree(path):
    """
    Given a traversable dir, recursively replicate the whole tree
    to the file system in a context manager.
    """
    assert path.is_dir()
    with _temp_path(tempfile.TemporaryDirectory(suffix=path.name)) as temp_dir:
        _write_contents(temp_dir, path)
        yield temp_dir


def _write_contents(target, source):
    for item in source.iterdir():
        child = target.joinpath(item.name)
        if item.is_dir():
            child.mkdir()
            _write_contents(child, item)
        else:
            child.open('wb').write(item.read_bytes())
