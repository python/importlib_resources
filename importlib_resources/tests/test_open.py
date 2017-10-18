import io
import os.path
import pathlib
import sys
import unittest

import importlib_resources as resources
from importlib_resources.tests import data


class CommonTests(unittest.TestCase):

    def test_package_name(self):
        # Passing in the package name should succeed.
        with resources.open(data.__name__, 'utf-8.file') as file:
            pass  # No error.

    def test_package_object(self):
        # Passing in the package itself should succeed.
        with resources.open(data, 'utf-8.file') as file:
            pass  # No error.

    def test_string_path(self):
        path = 'utf-8.file'
        # Passing in a string for the path should succeed.
        with resources.open(data, path) as file:
            pass  # No error.

    @unittest.skipIf(sys.version_info < (3, 6), 'requires os.PathLike support')
    def test_pathlib_path(self):
        # Passing in a pathlib.PurePath object for the path should succeed.
        path = pathlib.PurePath('utf-8.file')
        with resources.open(data, path) as file:
            pass  # No error.

    def test_absolute_path(self):
        # An absolute path is a ValueError.
        path = pathlib.Path(__spec__.origin)
        full_path = path.parent/'utf-8.file'
        with self.assertRaises(ValueError):
            with resources.open(data, str(full_path)) as file:
                pass

    def test_relative_path(self):
        # A reative path is a ValueError.
        with self.assertRaises(ValueError):
            with resources.open(data, '../data/utf-8.file') as file:
                pass

    def test_importing_module_as_side_effect(self):
        # The anchor package can already be imported.
        del sys.modules[data.__name__]
        with resources.open(data.__name__, 'utf-8.file') as file:
            pass  # No Errors.

    def test_non_package(self):
        # The anchor package cannot be a module.
        with self.assertRaises(TypeError):
            with resources.open(__spec__.name, 'utf-8.file') as file:
                pass


class OpenTests(unittest.TestCase):

    def test_opened_for_reading(self):
        # The file-like object is ready for reading.
        with resources.open(data, 'utf-8.file') as file:
            self.assertEqual(b"Hello, world!\n", file.read())

    def test_wrap_for_text(self):
        # The file-like object can be wrapped for text reading.
        with resources.open(data, 'utf-8.file') as file:
            text_file = io.TextIOWrapper(file, encoding='utf-8')
            self.assertEqual('Hello, world!\n', text_file.read())


if __name__ == '__main__':
    unittest.main()
