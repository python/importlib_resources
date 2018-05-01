"""Read resources contained within a package."""

import sys

__version__ = '0.5'


# Use the Python 3.7 stdlib implementation if available.
if sys.version_info >= (3, 7):
    from importlib.resources import (
        Package, Resource, contents, is_resource, open_binary, open_text, path,
        read_binary, read_text)
elif sys.version_info >= (3,):
    from importlib_resources._py3 import (
        Package, Resource, contents, is_resource, open_binary, open_text, path,
        read_binary, read_text)
    from importlib_resources.abc import ResourceReader
else:
    from importlib_resources._py2 import (
        contents, is_resource, open_binary, open_text, path, read_binary,
        read_text)
