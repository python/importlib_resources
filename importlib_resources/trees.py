from __future__ import absolute_import

import os
import abc
import zipp
import tempfile
import contextlib

from ._compat import ABC, Path, package_spec, FileNotFoundError


class Traversable(ABC):
    @abc.abstractmethod
    def iterdir(self):
        """
        Yield Traversable objects in self
        """

    @abc.abstractmethod
    def read_bytes(self):
        """
        Read contents of self as bytes
        """

    @abc.abstractmethod
    def read_text(self, encoding=None):
        """
        Read contents of self as bytes
        """

    @abc.abstractmethod
    def is_dir(self):
        """
        Return True if self is a dir
        """

    @abc.abstractmethod
    def is_file(self):
        """
        Return True if self is a file
        """


def from_package(package):
    """Return a Traversable object for the given package"""
    spec = package_spec(package)
    package_directory = Path(spec.origin).parent
    try:
        archive_path = spec.loader.archive
        rel_path = package_directory.relative_to(archive_path)
        return zipp.Path(archive_path, str(rel_path) + '/')
    except Exception:
        pass
    return package_directory


@contextlib.contextmanager
def _zip_path_as_file(path):
    # Not using tempfile.NamedTemporaryFile as it leads to deeper 'try'
    # blocks due to the need to close the temporary file to work on Windows
    # properly.
    fd, raw_path = tempfile.mkstemp()
    try:
        os.write(fd, path.read_bytes())
        os.close(fd)
        yield Path(raw_path)
    finally:
        try:
            os.remove(raw_path)
        except FileNotFoundError:
            pass


@contextlib.contextmanager
def _local_path_as_file(path):
    """
    Degenerate wrapper for pathlib.Path objects
    """
    yield path


@contextlib.contextmanager
def as_file(path):
    """
    Given a path-like object, return that object as a
    path on the local file system in a context manager.
    """
    if not path.is_file():
        raise FileNotFoundError(path)
    # todo: consider using functools.singledispatch
    wrapper = (
        _zip_path_as_file
        if isinstance(path, zipp.Path)
        else _local_path_as_file
        )
    with wrapper(path) as local:
        yield local
