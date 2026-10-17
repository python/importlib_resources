import sys

__all__ = ['ZipPath']


if sys.version_info >= (3, 10):  # noqa: UP036 (shim retained; removal is a separate change)
    from zipfile import Path as ZipPath
else:
    from zipp import Path as ZipPath
