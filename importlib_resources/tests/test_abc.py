import io
import zipfile
import unittest

from importlib_resources._compat import ZipPath, Path
from importlib_resources.abc import Traversable


class TraversableTests(unittest.TestCase):
    def test_zip_path_traversable(self):
        zf = zipfile.ZipFile(io.BytesIO(), 'w')
        assert isinstance(ZipPath(zf), Traversable)

    def test_pathlib_path_traversable(self):
        assert isinstance(Path(), Traversable)
