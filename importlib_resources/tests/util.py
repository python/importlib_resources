import abc
import importlib
import importlib.machinery
import io
import pathlib
import sys
import types
import unittest

from .. import abc as resources_abc
from . import data


def create_package(*, file, path, is_package=True):
    class Reader(resources_abc.ResourceReader):
        def open_resource(self, path):
            self._path = path
            if isinstance(file, Exception):
                raise file
            else:
                return file

        def resource_path(self, path_):
            self._path = path_
            if isinstance(path, Exception):
                raise path
            else:
                return path

    name = 'testingpackage'
    spec = importlib.machinery.ModuleSpec(
        name, Reader(),
        origin='does-not-exist',
        is_package=is_package)
    # Unforunately importlib.util.module_from_spec() was not introduced until
    # Python 3.5.
    module = types.ModuleType(name)
    module.__spec__ = spec
    return module


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

    def test_non_package_by_name(self):
        # The anchor package cannot be a module.
        with self.assertRaises(TypeError):
            self.execute(__spec__.name, 'utf-8.file')

    def test_non_package_by_package(self):
        # The anchor package cannot be a module.
        with self.assertRaises(TypeError):
            module = sys.modules['importlib_resources.tests.util']
            self.execute(module, 'utf-8.file')

    def test_resource_opener(self):
        data = io.BytesIO(b'Hello, world!')
        package = create_package(file=data, path=FileNotFoundError())
        self.execute(package, 'utf-8.file')
        self.assertEqual(package.__spec__.loader._path, 'utf-8.file')

    def test_resource_path(self):
        data = io.BytesIO(b'Hello, world!')
        path = __file__
        package = create_package(file=data, path=path)
        self.execute(package, 'utf-8.file')
        self.assertEqual(package.__spec__.loader._path, 'utf-8.file')

    def test_useless_loader(self):
        package = create_package(file=FileNotFoundError(),
                                 path=FileNotFoundError())
        with self.assertRaises(FileNotFoundError):
            self.execute(package, 'utf-8.file')


class ZipSetup:

    @classmethod
    def setUpClass(cls):
        data_path = pathlib.Path(data.__spec__.origin)
        data_dir = data_path.parent
        cls._zip_path = str(data_dir / 'ziptestdata.zip')
        sys.path.append(cls._zip_path)
        cls.data = importlib.import_module('ziptestdata')

    @classmethod
    def tearDownClass(cls):
        try:
            sys.path.remove(cls._zip_path)
        except ValueError:
            pass

        try:
            del sys.path_importer_cache[cls._zip_path]
            del sys.modules[cls.data.__spec__.name]
        except KeyError:
            pass

        try:
            del cls.data
            del cls._zip_path
        except AttributeError:
            pass
