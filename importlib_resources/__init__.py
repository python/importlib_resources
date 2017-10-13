import importlib
import io
import os.path
from typing import Union
from typing.io import BinaryIO


Path = Union[str, os.PathLike]


def _get_package(module_name):
    module = importlib.import_module(module_name)
    if module.__spec__.submodule_search_locations is None:
        raise TypeError(f"{module_name!r} is not a package")
    else:
        return module


def _normalize_path(path):
    if os.path.isabs(path):
        raise ValueError(f"{path!r} is absolute")
    normalized_path = os.path.normpath(path)
    if normalized_path.startswith(".."):
        raise ValueError("{path!r} attempts to traverse past package".format(path))
    else:
        return normalized_path


def open(package_name: str, path: Path) -> BinaryIO:
    """Return a file-like object opened for binary-reading of the resource."""
    normalized_path = _normalize_path(path)
    package = _get_package(package_name)
    package_path = os.path.dirname(os.path.abspath(package.__spec__.origin))
    full_path = os.path.join(package_path, normalized_path)
    data = package.__spec__.loader.get_data(full_path)
    return io.BytesIO(data)
