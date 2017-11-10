import abc

from typing.io import BinaryIO


class ResourceReader(abc.ABC):
    """Abstract base class for loaders to provide resource reading support."""

    @abc.abstractmethod
    def open_resource(self, path: str) -> BinaryIO:
        """Return an opened, file-like object for binary reading.

        The 'path' argument is expected to represent only a file name.
        If the resource cannot be found, FileNotFoundError is raised.
        """
        # This deliberately raises FileNotFoundError instead of
        # NotImplementedError so that if this method is accidentally called,
        # it'll still do the right thing.
        raise FileNotFoundError                     # pragma: nocover

    @abc.abstractmethod
    def resource_path(self, path: str) -> str:
        """Return the file system path to the specified resource.

        The 'path' argument is expected to represent only a file name.
        If the resource does not exist on the file system, raise
        FileNotFoundError.
        """
        # This deliberately raises FileNotFoundError instead of
        # NotImplementedError so that if this method is accidentally called,
        # it'll still do the right thing.
        raise FileNotFoundError                     # pragma: nocover
