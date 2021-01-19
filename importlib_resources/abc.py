import abc
import io
import itertools
from typing import BinaryIO, Iterable, Text, List

from ._compat import runtime_checkable, Protocol


class ResourceReader(metaclass=abc.ABCMeta):
    """Abstract base class for loaders to provide resource reading support."""

    @abc.abstractmethod
    def open_resource(self, resource: Text) -> BinaryIO:
        """Return an opened, file-like object for binary reading.

        The 'resource' argument is expected to represent only a file name.
        If the resource cannot be found, FileNotFoundError is raised.
        """
        # This deliberately raises FileNotFoundError instead of
        # NotImplementedError so that if this method is accidentally called,
        # it'll still do the right thing.
        raise FileNotFoundError

    @abc.abstractmethod
    def resource_path(self, resource: Text) -> Text:
        """Return the file system path to the specified resource.

        The 'resource' argument is expected to represent only a file name.
        If the resource does not exist on the file system, raise
        FileNotFoundError.
        """
        # This deliberately raises FileNotFoundError instead of
        # NotImplementedError so that if this method is accidentally called,
        # it'll still do the right thing.
        raise FileNotFoundError

    @abc.abstractmethod
    def is_resource(self, path: Text) -> bool:
        """Return True if the named 'path' is a resource.

        Files are resources, directories are not.
        """
        raise FileNotFoundError

    @abc.abstractmethod
    def contents(self) -> Iterable[str]:
        """Return an iterable of entries in `package`."""
        raise FileNotFoundError


@runtime_checkable
class Traversable(Protocol):
    """
    An object with a subset of pathlib.Path methods suitable for
    traversing directories and opening files.
    """

    @abc.abstractmethod
    def iterdir(self):
        """
        Yield Traversable objects in self
        """

    def read_bytes(self):
        """
        Read contents of self as bytes
        """
        with self.open('rb') as strm:
            return strm.read()

    def read_text(self, encoding=None):
        """
        Read contents of self as text
        """
        with self.open(encoding=encoding) as strm:
            return strm.read()

    @abc.abstractmethod
    def is_dir(self):
        # type: () -> bool
        """
        Return True if self is a dir
        """

    @abc.abstractmethod
    def is_file(self):
        # type: () -> bool
        """
        Return True if self is a file
        """

    @abc.abstractmethod
    def joinpath(self, child):
        """
        Return Traversable child in self
        """

    def __truediv__(self, child):
        """
        Return Traversable child in self
        """
        return self.joinpath(child)

    @abc.abstractmethod
    def open(self, mode='r', *args, **kwargs):
        """
        mode may be 'r' or 'rb' to open as text or binary. Return a handle
        suitable for reading (same as pathlib.Path.open).

        When opening as text, accepts encoding parameters such as those
        accepted by io.TextIOWrapper.
        """

    @abc.abstractproperty
    def name(self) -> str:
        """
        The base name of this object without any parent references.
        """


class SimpleReader(abc.ABC):
    """
    The minimum, low-level interface required from a resource
    provider.
    """

    @abc.abstractproperty
    def package(self):
        # type: () -> str
        """
        The name of the package for which this reader loads resources.
        """

    @abc.abstractmethod
    def children(self):
        # type: () -> List['SimpleReader']
        """
        Obtain an iterable of SimpleReader for available
        child containers (e.g. directories).
        """

    @abc.abstractmethod
    def resources(self):
        # type: () -> List[str]
        """
        Obtain available named resources for this virtual package.
        """

    @abc.abstractmethod
    def open_binary(self, resource):
        # type: (str) -> BinaryIO
        """
        Obtain a File-like for a named resource.
        """

    @property
    def name(self):
        return self.package.split('.')[-1]


class TraversableResources(ResourceReader):
    """
    The required interface for providing traversable
    resources.
    """

    @abc.abstractmethod
    def files(self):
        """Return a Traversable object for the loaded package."""

    def open_resource(self, resource):
        return self.files().joinpath(resource).open('rb')

    def resource_path(self, resource):
        raise FileNotFoundError(resource)

    def is_resource(self, path):
        return self.files().joinpath(path).is_file()

    def contents(self):
        return (item.name for item in self.files().iterdir())


class ResourceHandle(Traversable):
    """
    Handle to a named resource in a ResourceReader.
    """

    def __init__(self, parent, name):
        # type: (ResourceContainer, str) -> None
        self.parent = parent
        self.name = name

    def is_file(self):
        return True

    def is_dir(self):
        return False

    def open(self, mode='r', *args, **kwargs):
        stream = self.parent.reader.open_binary(self.name)
        if 'b' not in mode:
            stream = io.TextIOWrapper(*args, **kwargs)
        return stream

    def joinpath(self, name):
        raise RuntimeError("Cannot traverse into a resource")


class ResourceContainer(Traversable):
    """
    Traversable container for a package's resources via its reader.
    """

    def __init__(self, reader):
        # type: (SimpleReader) -> None
        self.reader = reader

    def is_dir(self):
        return True

    def is_file(self):
        return False

    def iterdir(self):
        files = (ResourceHandle(self, name) for name in self.reader.resources)
        dirs = map(ResourceContainer, self.reader.children())
        return itertools.chain(files, dirs)

    def open(self, *args, **kwargs):
        raise IsADirectoryError()

    def joinpath(self, name):
        return next(
            traversable for traversable in self.iterdir() if traversable.name == name
        )


class TraversableReader(TraversableResources, SimpleReader):
    """
    A TraversableResources based on SimpleReader. Resource providers
    may derive from this class to provide the TraversableResources
    interface by supplying the SimpleReader interface.
    """

    def files(self):
        return ResourceContainer(self)
