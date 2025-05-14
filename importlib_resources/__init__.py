"""
Read resources contained within a package.

This codebase is shared between importlib.resources in the stdlib
and importlib_resources in PyPI. See
https://github.com/python/importlib_metadata/wiki/Development-Methodology
for more detail.
"""

from ._common import (
    as_file,
    files,
)
from ._functional import (
    contents,
    is_resource,
    open_binary,
    open_text,
    path,
    read_binary,
    read_text,
)
from .abc import ResourceReader

__all__ = [
    'Package',
    'Anchor',
    'ResourceReader',
    'as_file',
    'files',
    'contents',
    'is_resource',
    'open_binary',
    'open_text',
    'path',
    'read_binary',
    'read_text',
]

TYPE_CHECKING = False

# Type checkers needs this block to understand what __getattr__() exports currently.
if TYPE_CHECKING:
    from ._typing import Anchor, Package


def __getattr__(name: str) -> object:
    # Defer import to avoid an import-time dependency on typing, since Package and
    # Anchor are type aliases that use symbols from typing.
    if name in {"Anchor", "Package"}:
        from . import _typing

        obj = getattr(_typing, name)

    else:
        msg = f"module {__name__!r} has no attribute {name!r}"
        raise AttributeError(msg)

    globals()[name] = obj
    return obj

def __dir__() -> list[str]:
    return sorted(globals().keys() | {"Anchor", "Package"})
