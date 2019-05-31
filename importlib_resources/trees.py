from __future__ import absolute_import

import abc
import six
import zipp

try:
    import pathlib
except ImportError:
    import pathlib2 as pathlib


__metaclass__ = type


@six.add_metaclass(abc.ABCMeta)
class Traversable:
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
    package_directory = pathlib.Path(package.__spec__.origin).parent
    try:
        archive_path = package.__spec__.loader.archive
        rel_path = package_directory.relative_to(archive_path)
        return zipp.Path(archive_path, str(rel_path) + '/')
    except Exception:
        pass
    return package_directory
