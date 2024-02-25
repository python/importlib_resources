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

    def get_resource_reader(self, name):
        return (
            # local ZipReader if a zip module
            self._zip_reader()
            or
            # local NamespaceReader if a namespace module
            self._namespace_reader()
            or
            # local FileReader
            self._file_reader()
            or
            # fallback
            super().get_resource_reader(name)
        )

    @property
    def path(self):
        return self.spec.origin

    def _zip_reader(self):
        with suppress(AttributeError):
            return readers.ZipReader(self.spec.loader, self.spec.name)

    def _namespace_reader(self):
        with suppress(AttributeError, ValueError):
            return readers.NamespaceReader(self.spec.submodule_search_locations)

    def _file_reader(self):
        try:
            path = pathlib.Path(self.path)
        except TypeError:
            return None
        if path.exists():
            return readers.FileReader(self)


def wrap_spec(package):
    """
    Override _adapters.wrap_spec to use TraversableResourcesLoader
    from above. Ensures that future behavior is always available on older
    Pythons.
    """
    return _adapters.SpecLoaderAdapter(package.__spec__, TraversableResourcesLoader)