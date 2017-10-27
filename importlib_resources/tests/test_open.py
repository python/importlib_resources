import io
import os.path
import pathlib
import sys
import unittest

import importlib_resources as resources
from . import data
from . import util


ZIP_DATA_PATH = None  # type: Optional[pathlib.Path]
zip_data = None  # type: Optional[]
def setUpModule():
    global ZIP_DATA_PATH, zip_data
    data_path = pathlib.Path(data.__spec__.origin)
    data_dir = data_path.parent
    ZIP_DATA_PATH = str(data_dir / 'ziptestdata.zip')
    sys.path.append(ZIP_DATA_PATH)
    import ziptestdata
    zip_data = ziptestdata


def tearDownModule():
    global zip_data
    try:
        sys.path.remove(ZIP_DATA_PATH)
        del sys.path_importer_cache[ZIP_DATA_PATH]
        del sys.modules[zip_data.__spec__.name]
    except ValueError:
        pass


class CommonTests(util.CommonTests, unittest.TestCase):

    def execute(self, package, path):
        with resources.open(package, path):
            pass


class OpenTests:

    # Subclasses are expected to set the 'data' attribute.

    def test_opened_for_reading(self):
        # The file-like object is ready for reading.
        with resources.open(self.data, 'utf-8.file') as file:
            self.assertEqual(b"Hello, UTF-8 world!\n", file.read())

    def test_wrap_for_text(self):
        # The file-like object can be wrapped for text reading.
        with resources.open(self.data, 'utf-8.file') as file:
            text_file = io.TextIOWrapper(file, encoding='utf-8')
            self.assertEqual('Hello, UTF-8 world!\n', text_file.read())

    def test_FileNotFoundError(self):
        with self.assertRaises(FileNotFoundError):
            with resources.open(self.data, 'does-not-exist') as file:
                pass


class OpenDiskTests(OpenTests, unittest.TestCase):

    def setUp(self):
        self.data = data


class OpenZipTests(OpenTests, unittest.TestCase):

    def setUp(self):
        self.data = zip_data


if __name__ == '__main__':
    unittest.main()
