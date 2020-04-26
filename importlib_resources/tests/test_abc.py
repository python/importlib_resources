import io
import zipfile
import typing
import unittest

from importlib_resources._compat import ZipPath, Path
from importlib_resources.abc import Traversable


@unittest.skipUnless(
    hasattr(typing, 'runtime_checkable'),
    "Only suitable when typing supports runtime_checkable",
    )
class TraversableTests(unittest.TestCase):
    def test_zip_path_traversable(self):
        zf = zipfile.ZipFile(io.BytesIO(), 'w')
        assert isinstance(ZipPath(zf), Traversable)

    def test_pathlib_path_traversable(self):
        assert isinstance(Path(), Traversable)
