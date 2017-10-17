import importlib
import io
import os.path
import sys
import types
from typing import Union
from typing.io import BinaryIO


Package = Union[types.ModuleType, str]
if sys.version_info >= (3, 6):
    Path = Union[str, os.PathLike]
else:
    Path = str


def _get_package(package):
    if hasattr(package, '__spec__'):
        if package.__spec__.submodule_search_locations is None:
            raise TypeError("{!r} is not a package".format(package.__spec__.name))
        else:
            return package
    else:
        module = importlib.import_module(package)
        if module.__spec__.submodule_search_locations is None:
            raise TypeError("{!r} is not a package".format(package))
        else:
            return module


def _normalize_path(path):
    parent, file_name = os.path.split(path)
    if parent:
        raise ValueError("{!r} is not only a file name".format(path))
    else:
        return file_name


def open(package: Package, file_name: Path) -> BinaryIO:
    """Return a file-like object opened for binary-reading of the resource."""
    file_name = _normalize_path(file_name)
    package = _get_package(package)
    package_path = os.path.dirname(os.path.abspath(package.__spec__.origin))
    full_path = os.path.join(package_path, file_name)
    if not os.path.exists(full_path):
        package_name = package.__spec__.name
        message = "{!r} does not exist"
        raise FileNotFoundError(message.format(full_path))
    data = package.__spec__.loader.get_data(full_path)
    return io.BytesIO(data)
