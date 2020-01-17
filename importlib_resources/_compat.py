from __future__ import absolute_import

# flake8: noqa

try:
    from pathlib import Path, PurePath
except ImportError:
    from pathlib2 import Path, PurePath                         # type: ignore


try:
    from abc import ABC                                         # type: ignore
except ImportError:
    from abc import ABCMeta

    class ABC(object):                                          # type: ignore
        __metaclass__ = ABCMeta


try:
    FileNotFoundError = FileNotFoundError                       # type: ignore
except NameError:
    FileNotFoundError = OSError                                 # type: ignore


class PackageSpec(object):
	def __init__(self, **kwargs):
		vars(self).update(kwargs)


def package_spec(package):
	return getattr(package, '__spec__', None) or \
		PackageSpec(
			origin=package.__file__,
			loader=getattr(package, '__loader__', None),
		)
