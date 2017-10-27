import abc
import pathlib
import sys
import unittest

from . import data


class CommonTests(abc.ABC):

    @abc.abstractmethod
    def execute(self, package, path):
        raise NotImplementedError

    def test_package_name(self):
        # Passing in the package name should succeed.
        self.execute(data.__name__, 'utf-8.file')

    def test_package_object(self):
        # Passing in the package itself should succeed.
        self.execute(data, 'utf-8.file')

    def test_string_path(self):
        # Passing in a string for the path should succeed.
        path = 'utf-8.file'
        self.execute(data, path)

    @unittest.skipIf(sys.version_info < (3, 6), 'requires os.PathLike support')
    def test_pathlib_path(self):
        # Passing in a pathlib.PurePath object for the path should succeed.
        path = pathlib.PurePath('utf-8.file')
        self.execute(data, path)

    def test_absolute_path(self):
        # An absolute path is a ValueError.
        path = pathlib.Path(__file__)
        full_path = path.parent/'utf-8.file'
        with self.assertRaises(ValueError):
            self.execute(data, full_path)

    def test_relative_path(self):
        # A reative path is a ValueError.
        with self.assertRaises(ValueError):
            self.execute(data, '../data/utf-8.file')

    def test_importing_module_as_side_effect(self):
        # The anchor package can already be imported.
        del sys.modules[data.__name__]
        self.execute(data.__name__, 'utf-8.file')

    def test_non_package(self):
        # The anchor package cannot be a module.
        with self.assertRaises(TypeError):
            self.execute(__spec__.name, 'utf-8.file')
