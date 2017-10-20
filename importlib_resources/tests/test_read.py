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
        resources.read(data.__name__, 'utf-8.file')

    def test_package_object(self):
        # Passing in the package itself should succeed.
        resources.read(data, 'utf-8.file')

    def test_string_path(self):
        path = 'utf-8.file'
        # Passing in a string for the path should succeed.
        resources.read(data, path)

    @unittest.skipIf(sys.version_info < (3, 6), 'requires os.PathLike support')
    def test_pathlib_path(self):
        # Passing in a pathlib.PurePath object for the path should succeed.
        path = pathlib.PurePath('utf-8.file')
        resources.read(data, path)

    def test_absolute_path(self):
        # An absolute path is a ValueError.
        path = pathlib.Path(__file__)
        full_path = path.parent/'utf-8.file'
        with self.assertRaises(ValueError):
            resources.read(data, str(full_path))

    def test_relative_path(self):
        # A reative path is a ValueError.
        with self.assertRaises(ValueError):
            resources.read(data, '../data/utf-8.file')

    def test_importing_module_as_side_effect(self):
        # The anchor package can already be imported.
        del sys.modules[data.__name__]
        resources.read(data.__name__, 'utf-8.file')

    def test_non_package(self):
        # The anchor package cannot be a module.
        with self.assertRaises(TypeError):
            resources.read(__spec__.name, 'utf-8.file')


class ReadTests(unittest.TestCase):

    def test_default_encoding(self):
        result = resources.read(data, 'utf-8.file')
        self.assertEqual("Hello, UTF-8 world!\n", result)

    def test_encoding(self):
        result = resources.read(data, 'utf-16.file', encoding='utf-16')
        self.assertEqual("Hello, UTF-16 world!\n", result)

    def test_errors(self):
        # Raises UnicodeError without the 'errors' argument.
        result = resources.read(data, 'utf-16.file', encoding='utf-8',
                                errors='ignore')
