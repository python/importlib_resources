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
        with resources.path(data.__name__, 'utf-8.file') as path:
            pass  # No error.

    def test_package_object(self):
        # Passing in the package itself should succeed.
        with resources.path(data, 'utf-8.file') as path:
            pass  # No error.

    def test_string_path(self):
        path = 'utf-8.file'
        # Passing in a string for the path should succeed.
        with resources.path(data, path) as path:
            pass  # No error.

    @unittest.skipIf(sys.version_info < (3, 6), 'requires os.PathLike support')
    def test_pathlib_path(self):
        # Passing in a pathlib.PurePath object for the path should succeed.
        path = pathlib.PurePath('utf-8.file')
        with resources.path(data, path) as path:
            pass  # No error.

    # Don't fail if run under e.g. pytest.
    def test_absolute_path(self):
        # An absolute path is a ValueError.
        path = pathlib.Path(__file__)
        full_path = path.parent/'utf-8.file'
        with self.assertRaises(ValueError):
            with resources.path(data, str(full_path)) as path:
                pass

    def test_relative_path(self):
        # A reative path is a ValueError.
        with self.assertRaises(ValueError):
            with resources.path(data, '../data/utf-8.file') as path:
                pass

    def test_importing_module_as_side_effect(self):
        # The anchor package can already be imported.
        del sys.modules[data.__name__]
        with resources.path(data.__name__, 'utf-8.file') as path:
            pass  # No Errors.

    def test_non_package(self):
        # The anchor package cannot be a module.
        with self.assertRaises(TypeError):
            with resources.path(__spec__.name, 'utf-8.file') as path:
                pass


class PathTests(unittest.TestCase):

    def test_reading(self):
        # Path should be readable.
        # Test also implicitly verifies the returned object is a pathlib.Path
        # instance.
        with resources.path(data, 'utf-8.file') as path:
            # pathlib.Path.read_text() was introduced in Python 3.5.
            with path.open('r', encoding='utf-8') as file:
                text = file.read()
            self.assertEqual('Hello, UTF-8 world!\n', text)
