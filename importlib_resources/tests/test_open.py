import os.path
import pathlib
import unittest

import importlib_resources as resources


PACKAGE = __spec__.name.rpartition('.')[0]


class CommonTests(unittest.TestCase):

    def test_string_path(self):
        path = 'data/test.file'
        # Passing in a string for the path should succeed.
        with resources.open(PACKAGE, path) as file:
            pass  # No error.

    def test_pathlib_path(self):
        # Passing in a pathlib.PurePath object for the path should succeed.
        path = pathlib.PurePath('data')/'test.file'
        with resources.open(PACKAGE, path) as file:
            pass  # No error.

    def test_absolute_path(self):
        # An absolute path is a ValueError.
        path = pathlib.Path(__spec__.origin).resolve()
        with self.assertRaises(ValueError):
            with resources.open(PACKAGE, path) as file:
                pass

    def test_traversing_path(self):
        # A path that traverses -- e.g. has ``..`` -- is a ValueError.
        path = 'data/../../__init__.py'
        with self.assertRaises(ValueError):
            with resources.open(PACKAGE, path) as file:
                pass

    def test_importing_module_as_side_effect(self):
        # The anchor package can already be imported.
        pass

    def test_non_package(self):
        # The anchor package cannot be a module.
        with self.assertRaises(TypeError):
            with resources.open(__spec__.name, 'data/test.file') as file:
                pass


class OpenTests(unittest.TestCase):

    def test_opened_for_reading(self):
        # The file-like object is ready for reading.
        with resources.open(PACKAGE, 'data/test.file') as file:
            self.assertEqual(b"Hello, World!\n", file.read())


if __name__ == '__main__':
    unittest.main()
