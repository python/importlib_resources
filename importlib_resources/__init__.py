"""Read resources contained within a package."""

import sys

__version__ = '0.1.0'


if sys.version_info >= (3,):
    from importlib_resources._py3 import open, path, read
else:
    from importlib_resources._py2 import open, path, read
