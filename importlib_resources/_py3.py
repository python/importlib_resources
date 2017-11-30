import os
import sys
import tempfile

from . import abc as resources_abc
from ._util import _wrap_file
from builtins import open as builtins_open
from contextlib import contextmanager
from importlib import import_module
from importlib.abc import ResourceLoader
from io import BytesIO, TextIOWrapper
from pathlib import Path
from types import ModuleType
from typing import Iterator, Union
from typing import cast
from typing.io import IO


Package = Union[ModuleType, str]
if sys.version_info >= (3, 6):
    FileName = Union[str, os.PathLike]              # pragma: ge35
else:
    FileName = str                                  # pragma: le35


def _get_package(package) -> ModuleType:
    if hasattr(package, '__spec__'):
        if package.__spec__.submodule_search_locations is None:
            raise TypeError("{!r} is not a package".format(
                package.__spec__.name))
        else:
            return package
    else:
        module = import_module(package)
        if module.__spec__.submodule_search_locations is None:
            raise TypeError("{!r} is not a package".format(package))
        else:
            return module


def _normalize_path(path) -> str:
    str_path = str(path)
    parent, file_name = os.path.split(str_path)
    if parent:
        raise ValueError("{!r} must be only a file name".format(path))
    else:
        return file_name


def open(package: Package,
         file_name: FileName,
         encoding: str = None,
         errors: str = None) -> IO:
    """Return a file-like object opened for reading of the resource."""
    file_name = _normalize_path(file_name)
    package = _get_package(package)
    if hasattr(package.__spec__.loader, 'open_resource'):
        reader = cast(resources_abc.ResourceReader, package.__spec__.loader)
        return _wrap_file(reader.open_resource(file_name), encoding, errors)
    else:
        # Using pathlib doesn't work well here due to the lack of 'strict'
        # argument for pathlib.Path.resolve() prior to Python 3.6.
        absolute_package_path = os.path.abspath(package.__spec__.origin)
        package_path = os.path.dirname(absolute_package_path)
        full_path = os.path.join(package_path, file_name)
        if encoding is None:
            args = dict(mode='rb')
        else:
            args = dict(mode='r', encoding=encoding, errors=errors)
        try:
            return builtins_open(full_path, **args)   # type: ignore
        except IOError:
            # Just assume the loader is a resource loader; all the relevant
            # importlib.machinery loaders are and an AttributeError for
            # get_data() will make it clear what is needed from the loader.
            loader = cast(ResourceLoader, package.__spec__.loader)
            try:
                data = loader.get_data(full_path)
            except IOError:
                package_name = package.__spec__.name
                message = '{!r} resource not found in {!r}'.format(
                    file_name, package_name)
                raise FileNotFoundError(message)
            else:
                return _wrap_file(BytesIO(data), encoding, errors)


def read(package: Package,
         file_name: FileName,
         encoding: str = 'utf-8',
         errors: str = 'strict') -> Union[str, bytes]:
    """Return the decoded string of the resource.

    The decoding-related arguments have the same semantics as those of
    bytes.decode().
    """
    file_name = _normalize_path(file_name)
    package = _get_package(package)
    # Note this is **not** builtins.open()!
    with open(package, file_name) as binary_file:
        if encoding is None:
            return binary_file.read()
        # Decoding from io.TextIOWrapper() instead of str.decode() in hopes
        # that the former will be smarter about memory usage.
        text_file = TextIOWrapper(
            binary_file, encoding=encoding, errors=errors)
        return text_file.read()


@contextmanager
def path(package: Package, file_name: FileName) -> Iterator[Path]:
    """A context manager providing a file path object to the resource.

    If the resource does not already exist on its own on the file system,
    a temporary file will be created. If the file was created, the file
    will be deleted upon exiting the context manager (no exception is
    raised if the file was deleted prior to the context manager
    exiting).
    """
    file_name = _normalize_path(file_name)
    package = _get_package(package)
    if hasattr(package.__spec__.loader, 'resource_path'):
        reader = cast(resources_abc.ResourceReader, package.__spec__.loader)
        try:
            yield Path(reader.resource_path(file_name))
            return
        except FileNotFoundError:
            pass
    # Fall-through for both the lack of resource_path() *and* if
    # resource_path() raises FileNotFoundError.
    package_directory = Path(package.__spec__.origin).parent
    file_path = package_directory / file_name
    if file_path.exists():
        yield file_path
    else:
        with open(package, file_name) as file:
            data = file.read()
        # Not using tempfile.NamedTemporaryFile as it leads to deeper 'try'
        # blocks due to the need to close the temporary file to work on
        # Windows properly.
        fd, raw_path = tempfile.mkstemp()
        try:
            os.write(fd, data)
            os.close(fd)
            yield Path(raw_path)
        finally:
            try:
                os.remove(raw_path)
            except FileNotFoundError:
                pass
