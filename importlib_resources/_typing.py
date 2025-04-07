"""Internal.

A lazy re-export shim/middleman for typing-related symbols and annotation-related symbols to
avoid import-time dependencies on expensive modules (like `typing`). Some symbols may
eventually be needed at runtime, but their import/creation will be "on demand" to
improve startup performance.

Usage Notes
-----------
Do not directly import annotation-related symbols from this module
(e.g. ``from ._lazy import Any``)! Doing so will trigger the module-level `__getattr__`,
causing the modules of shimmed symbols, e.g. `typing`, to get imported. Instead, import
the module and use symbols via attribute access as needed
(e.g. ``from . import _lazy [as _t]``).

Additionally, to avoid those symbols being evaluated at runtime, which would *also*
cause shimmed modules to get imported, make sure to defer evaluation of annotations via
the following:

    a) <3.14: Manual stringification of annotations, or
        `from __future__ import annotations`.
    b) >=3.14: Nothing, thanks to default PEP 649 semantics.
"""

__all__ = (
    # ---- Typing/annotation symbols ----
    # collections.abc
    "Iterable",
    "Iterator",

    # typing
    "Any",
    "BinaryIO",
    "NoReturn",
    "Optional",
    "Text",
    "Union",

    # Other
    "Package",
    "Anchor",
    "StrPath",

)  # fmt: skip


TYPE_CHECKING = False


# Type checkers needs this block to understand what __getattr__() does currently.
if TYPE_CHECKING:
    import os
    import types
    from collections.abc import Iterable, Iterator
    from typing import (
        Any,
        BinaryIO,
        NoReturn,
        Optional,
        Text,
        Union,
    )

    from typing_extensions import TypeAlias

    Package: TypeAlias = Union[types.ModuleType, str]
    Anchor = Package
    StrPath: TypeAlias = Union[str, os.PathLike[str]]


def __getattr__(name: str) -> object:
    if name in {"Iterable", "Iterator"}:
        import collections.abc

        obj = getattr(collections.abc, name)

    elif name in {"Any", "BinaryIO", "NoReturn", "Text", "Optional", "Union"}:
        import typing

        obj = getattr(typing, name)

    elif name in {"Package", "Anchor"}:
        import types
        from typing import Union

        obj = Union[types.ModuleType, str]

    elif name == "StrPath":
        import os
        from typing import Union

        obj = Union[str, "os.PathLike[str]"]

    else:
        msg = f"module {__name__!r} has no attribute {name!r}"
        raise AttributeError(msg)

    globals()[name] = obj
    return obj


def __dir__() -> list[str]:
    return sorted(globals().keys() | __all__)
