"""Read resources contained within a package."""

import sys


__all__ = [
    'Package',
    'Resource',
    'ResourceReader',
    'contents',
    'files',
    'is_resource',
    'open_binary',
    'open_text',
    'path',
    'read_binary',
    'read_text',
    ]


if sys.version_info >= (3,):
    from importlib_resources._py3 import (
        Package,
        Resource,
        contents,
        files,
        is_resource,
        open_binary,
        open_text,
        path,
        read_binary,
        read_text,
        )
    from importlib_resources.abc import ResourceReader
else:
    from importlib_resources._py2 import (
        contents,
        files,
        is_resource,
        open_binary,
        open_text,
        path,
        read_binary,
        read_text,
        )
    del __all__[:3]


__version__ = \
    files('importlib_resources').joinpath('version.txt').read_text().strip()
