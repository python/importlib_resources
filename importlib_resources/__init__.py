"""Read resources contained within a package."""

import sys

__version__ = '0.2'


if sys.version_info >= (3,):
    from importlib_resources._py3 import (
        Package, Resource, contents, is_resource, open_binary, open_text, path,
        read_binary, read_text)
    from importlib_resources.abc import ResourceReader
else:
    from importlib_resources._py2 import (
        contents, is_resource, open_binary, open_text, path, read_binary,
        read_text)
