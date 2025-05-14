import abc
import itertools
import os
import pathlib
from collections.abc import Iterator
from typing import (
    Any,
    BinaryIO,
    Literal,
    Optional,
    Protocol,
    TextIO,
    Union,
    overload,
    runtime_checkable,
)

from .abc import TraversalError

StrPath = Union[str, os.PathLike[str]]


@runtime_checkable
class Traversable(Protocol):
    """
    An object with a subset of pathlib.Path methods suitable for
    traversing directories and opening files.

    Any exceptions that occur when accessing the backing resource
    may propagate unaltered.
    """

    @abc.abstractmethod
    def iterdir(self) -> Iterator["Traversable"]:
        """
        Yield Traversable objects in self
        """

    def read_bytes(self) -> bytes:
        """
        Read contents of self as bytes
        """
        with self.open('rb') as strm:
            return strm.read()

    def read_text(
        self, encoding: Optional[str] = None, errors: Optional[str] = None
    ) -> str:
        """
        Read contents of self as text
        """
        with self.open(encoding=encoding, errors=errors) as strm:
            return strm.read()

    @abc.abstractmethod
    def is_dir(self) -> bool:
        """
        Return True if self is a directory
        """

    @abc.abstractmethod
    def is_file(self) -> bool:
        """
        Return True if self is a file
        """

    def joinpath(self, *descendants: StrPath) -> "Traversable":
        """
        Return Traversable resolved with any descendants applied.

        Each descendant should be a path segment relative to self
        and each may contain multiple levels separated by
        ``posixpath.sep`` (``/``).
        """
        if not descendants:
            return self
        names = itertools.chain.from_iterable(
            path.parts for path in map(pathlib.PurePosixPath, descendants)
        )
        target = next(names)
        matches = (
            traversable for traversable in self.iterdir() if traversable.name == target
        )
        try:
            match = next(matches)
        except StopIteration:
            raise TraversalError(
                "Target not found during traversal.", target, list(names)
            )
        return match.joinpath(*names)

    def __truediv__(self, child: StrPath) -> "Traversable":
        """
        Return Traversable child in self
        """
        return self.joinpath(child)

    @overload
    def open(self, mode: Literal['r'] = 'r', *args: Any, **kwargs: Any) -> TextIO: ...

    @overload
    def open(self, mode: Literal['rb'], *args: Any, **kwargs: Any) -> BinaryIO: ...

    @abc.abstractmethod
    def open(
        self, mode: str = 'r', *args: Any, **kwargs: Any
    ) -> Union[TextIO, BinaryIO]:
        """
        mode may be 'r' or 'rb' to open as text or binary. Return a handle
        suitable for reading (same as pathlib.Path.open).

        When opening as text, accepts encoding parameters such as those
        accepted by io.TextIOWrapper.
        """

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """
        The base name of this object without any parent references.
        """
