import abc
import importlib
import sys
import unittest

from . import data01
from . import zipdata01
from .._compat import ABC, Path, PurePath

try:
    from test.support import modules_setup, modules_cleanup
except ImportError:
    # Python 2.7.
    def modules_setup():
        return sys.modules.copy(),

    def modules_cleanup(oldmodules):
        # Encoders/decoders are registered permanently within the internal
        # codec cache. If we destroy the corresponding modules their
        # globals will be set to None which will trip up the cached functions.
        encodings = [(k, v) for k, v in sys.modules.items()
                     if k.startswith('encodings.')]
        sys.modules.clear()
        sys.modules.update(encodings)
        # XXX: This kind of problem can affect more than just encodings. In
        # particular extension modules (such as _ssl) don't cope with reloading
        # properly.  Really, test modules should be cleaning out the test
        # specific modules they know they added (ala test_runpy) rather than
        # relying on this function (as test_importhooks and test_pkg do
        # currently).  Implicitly imported *real* modules should be left alone
        # (see issue 10556).
        sys.modules.update(oldmodules)


try:
    from importlib.machinery import ModuleSpec
except ImportError:
    ModuleSpec = None                               # type: ignore


class CommonTests(ABC):

    @abc.abstractmethod
    def execute(self, package, path):
        raise NotImplementedError

    def test_package_name(self):
        # Passing in the package name should succeed.
        self.execute(data01.__name__, 'utf-8.file')

    def test_package_object(self):
        # Passing in the package itself should succeed.
        self.execute(data01, 'utf-8.file')

    def test_string_path(self):
        # Passing in a string for the path should succeed.
        path = 'utf-8.file'
        self.execute(data01, path)

    @unittest.skipIf(sys.version_info < (3, 6), 'requires os.PathLike support')
    def test_pathlib_path(self):
        # Passing in a pathlib.PurePath object for the path should succeed.
        path = PurePath('utf-8.file')
        self.execute(data01, path)

    def test_absolute_path(self):
        path = Path(__file__)
        full_path = path.parent/'utf-8.file'
        with self.assertRaises(FileNotFoundError):
            self.execute(data01, full_path)

    def test_relative_path(self):
        self.execute(data01, '../data01/utf-8.file')

    def test_importing_module_as_side_effect(self):
        # The anchor package can already be imported.
        del sys.modules[data01.__name__]
        self.execute(data01.__name__, 'utf-8.file')

    def test_non_package_by_name(self):
        # The anchor package cannot be a module.
        with self.assertRaises(TypeError):
            self.execute(__name__, 'utf-8.file')

    def test_non_package_by_package(self):
        # The anchor package cannot be a module.
        with self.assertRaises(TypeError):
            module = sys.modules['importlib_resources.tests.util']
            self.execute(module, 'utf-8.file')


class ZipSetupBase:
    ZIP_MODULE = None

    @classmethod
    def setUpClass(cls):
        data_path = Path(cls.ZIP_MODULE.__file__)
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
            del sys.modules[cls.data.__name__]
        except KeyError:
            pass

        try:
            del cls.data
            del cls._zip_path
        except AttributeError:
            pass

    def setUp(self):
        modules = modules_setup()
        self.addCleanup(modules_cleanup, *modules)


class ZipSetup(ZipSetupBase):
    ZIP_MODULE = zipdata01                          # type: ignore
