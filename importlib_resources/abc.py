import abc
import os
from typing import (
    Any,
    BinaryIO,
    Iterable,
    Iterator,
    NoReturn,
    Text,
    Union,
)

from ._typing import TYPE_CHECKING

StrPath = Union[str, os.PathLike[str]]

__all__ = ["ResourceReader", "Traversable", "TraversableResources"]


# A hack for the following targets:
# a) Type checkers, so they can understand what __getattr__() exports.
# b) Internal annotations, so that Traversable can be used in deferred annotations via
#    _self_mod.Traversable.
if TYPE_CHECKING:
    from ._traversable import Traversable

    class _self_mod:
        from ._traversable import Traversable

else:
    _self_mod = __import__("sys").modules[__name__]


def __getattr__(name: str) -> object:
    # Defer import to avoid an import dependency on typing, since Traversable subclasses
    # typing.Protocol.
    if name == "Traversable":
        from ._traversable import Traversable

        return Traversable

    msg = f"module {__name__!r} has no attribute {name!r}"
    raise AttributeError(msg)


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


class TraversalError(Exception):
    pass


class TraversableResources(ResourceReader):
    """
    The required interface for providing traversable
    resources.
    """

    @abc.abstractmethod
    def files(self) -> "_self_mod.Traversable":
        """Return a Traversable object for the loaded package."""

    def open_resource(self, resource: StrPath) -> BinaryIO:
        return self.files().joinpath(resource).open('rb')

    def resource_path(self, resource: Any) -> NoReturn:
        raise FileNotFoundError(resource)

    def is_resource(self, path: StrPath) -> bool:
        return self.files().joinpath(path).is_file()

    def contents(self) -> Iterator[str]:
        return (item.name for item in self.files().iterdir())
