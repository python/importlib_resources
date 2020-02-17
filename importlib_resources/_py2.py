from . import trees
from importlib import import_module


def _resolve(name):
    """If name is a string, resolve to a module."""
    if not isinstance(name, basestring):                    # noqa: F821
        return name
    return import_module(name)


def _get_package(package):
    """Normalize a path by ensuring it is a string.

    If the resulting string contains path separators, an exception is raised.
    """
    module = _resolve(package)
    if not hasattr(module, '__path__'):
        raise TypeError("{!r} is not a package".format(package))
    return module


def files(package):
    return trees.from_package(_get_package(package))
