# flake8: noqa

import abc
import os
import sys
import pathlib
import warnings
from contextlib import suppress
from typing import Union

from .. import readers, _adapters


class TraversableResourcesLoader(_adapters.TraversableResourcesLoader):
    """
    Adapt loaders to provide TraversableResources and other
    compatibility.

    Ensures the readers from importlib_resources are preferred
    over stdlib readers.
    """

    @property
    def path(self):
        return self.spec.origin

    def get_resource_reader(self, name):
        def _zip_reader(spec):
            with suppress(AttributeError):
                return readers.ZipReader(spec.loader, spec.name)

        def _namespace_reader(spec):
            with suppress(AttributeError, ValueError):
                return readers.NamespaceReader(spec.submodule_search_locations)

        def _file_reader(spec):
            try:
                path = pathlib.Path(self.path)
            except TypeError:
                return None
            if path.exists():
                return readers.FileReader(self)

        return (
            # local ZipReader if a zip module
            _zip_reader(self.spec)
            or
            # local NamespaceReader if a namespace module
            _namespace_reader(self.spec)
            or
            # local FileReader
            _file_reader(self.spec)
            or
            # fallback
            super().get_resource_reader(name)
        )


def wrap_spec(package):
    """
    Override _adapters.wrap_spec to use TraversableResourcesLoader
    from above. Ensures that future behavior is always available on older
    Pythons.
    """
    return _adapters.SpecLoaderAdapter(package.__spec__, TraversableResourcesLoader)
