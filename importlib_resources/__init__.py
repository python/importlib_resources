"""Read resources contained within a package."""

import sys


__all__ = [
    'files',
    ]


if sys.version_info >= (3,):
    from importlib_resources._py3 import files
else:
    from importlib_resources._py2 import files


__version__ = \
    files('importlib_resources').joinpath('version.txt').read_text().strip()
