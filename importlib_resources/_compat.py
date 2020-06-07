from __future__ import absolute_import

# flake8: noqa

try:
    from pathlib import Path, PurePath
except ImportError:
    from pathlib2 import Path, PurePath                         # type: ignore


try:
    from contextlib import suppress
except ImportError:
    from contextlib2 import suppress                         # type: ignore


try:
    from functools import singledispatch
except ImportError:
    from singledispatch import singledispatch                   # type: ignore


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


try:
    from importlib import metadata
except ImportError:
    import importlib_metadata as metadata  # type: ignore


try:
    from zipfile import Path as ZipPath  # type: ignore
except ImportError:
    from zipp import Path as ZipPath  # type: ignore


try:
    from typing import runtime_checkable  # type: ignore
except ImportError:
    def runtime_checkable(cls):  # type: ignore
        return cls


try:
    from typing import Protocol  # type: ignore
except ImportError:
    Protocol = ABC  # type: ignore


__metaclass__ = type


class PackageSpec:
    def __init__(self, **kwargs):
        vars(self).update(kwargs)


class TraversableResourcesAdapter:
    def __init__(self, spec):
        self.spec = spec
        self.loader = LoaderAdapter(spec)

    def __getattr__(self, name):
        return getattr(self.spec, name)


class LoaderAdapter:
    """
    Adapt loaders to provide TraversableResources and other
    compatibility.
    """
    def __init__(self, spec):
        self.spec = spec

    @property
    def path(self):
        # Python < 3
        return self.spec.origin

    def get_resource_reader(self, name):
        # Python < 3.9
        from . import readers
        try:
            reader = self.spec.loader.get_resource_reader(name)
            reader.files
        except AttributeError:
            reader = _zip_reader(self.spec) or readers.FileReader(self)
        return reader


def _zip_reader(spec):
    from . import readers
    with suppress(AttributeError):
        return readers.ZipReader(spec.loader, spec.name)


def package_spec(package):
    """
    Construct a minimal package spec suitable for
    matching the interfaces this library relies upon
    in later Python versions.
    """
    spec = getattr(package, '__spec__', None) or \
        PackageSpec(
            origin=package.__file__,
            loader=getattr(package, '__loader__', None),
            name=package.__name__,
            submodule_search_locations=getattr(package, '__path__', None),
        )
    return TraversableResourcesAdapter(spec)
