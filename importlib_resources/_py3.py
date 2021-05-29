import os

from types import ModuleType
from typing import Union

Package = Union[str, ModuleType]
Resource = Union[str, os.PathLike]
