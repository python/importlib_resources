import abc
import sys
from contextlib import suppress

# flake8: noqa

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
    Protocol = abc.ABC  # type: ignore


class SpecLoaderAdapter:
    """
    Adapt a package spec to adapt the underlying loader.
    """

    def __init__(self, spec, adapter=lambda spec: spec.loader):
        self.spec = spec
        self.loader = adapter(spec)

    def __getattr__(self, name):
        return getattr(self.spec, name)


class TraversableResourcesLoader:
    """
    Adapt loaders to provide TraversableResources and other
    compatibility.
    """

    def __init__(self, spec):
        self.spec = spec

    @property
    def path(self):
        return self.spec.origin

    def get_resource_reader(self, name):
        # Python < 3.9
        from . import readers

        def _zip_reader(spec):
            with suppress(AttributeError):
                return readers.ZipReader(spec.loader, spec.name)

        def _namespace_reader(spec):
            with suppress(AttributeError, ValueError):
                return readers.NamespaceReader(spec.submodule_search_locations)

        def _available_reader(spec):
            with suppress(AttributeError):
                return spec.loader.get_resource_reader(spec.name)

        def _native_reader(spec):
            reader = _available_reader(spec)
            return reader if hasattr(reader, 'files') else None

        return (
            # native reader if it supplies 'files'
            _native_reader(self.spec)
            or
            # local ZipReader if a zip module
            _zip_reader(self.spec)
            or
            # local NamespaceReader if a namespace module
            _namespace_reader(self.spec)
            or
            # local FileReader
            readers.FileReader(self)
        )


def package_spec(package):
    """
    Construct a minimal package spec suitable for
    matching the interfaces this library relies upon
    in later Python versions.
    """
    spec = package.__spec__
    # avoid adapting the spec in test_package_has_no_reader_fallback
    adapt = spec.loader.__class__ is not object
    return SpecLoaderAdapter(spec, TraversableResourcesLoader) if adapt else spec
