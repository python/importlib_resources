import abc
import zipp
import pathlib
import contextlib


class Traversable(metaclass=abc.ABCMeta):
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
    with contextlib.suppress(Exception):
        archive_path = package.__spec__.loader.archive
        rel_path = package_directory.relative_to(archive_path)
        return zipp.Path(archive_path, str(rel_path) + '/')
    return package_directory
