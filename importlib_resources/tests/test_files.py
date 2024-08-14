import textwrap
import unittest
import warnings
import importlib
import contextlib

import importlib_resources as resources
from ..abc import Traversable
from . import util
from .compat.py39 import os_helper
from .compat.py312 import import_helper


@contextlib.contextmanager
def suppress_known_deprecation():
    with warnings.catch_warnings(record=True) as ctx:
        warnings.simplefilter('default', category=DeprecationWarning)
        yield ctx


class FilesTests:
    def test_read_bytes(self):
        files = resources.files(self.data)
        actual = files.joinpath('utf-8.file').read_bytes()
        assert actual == b'Hello, UTF-8 world!\n'

    def test_read_text(self):
        files = resources.files(self.data)
        actual = files.joinpath('utf-8.file').read_text(encoding='utf-8')
        assert actual == 'Hello, UTF-8 world!\n'

    def test_traversable(self):
        assert isinstance(resources.files(self.data), Traversable)

    def test_joinpath_with_multiple_args(self):
        files = resources.files(self.data)
        binfile = files.joinpath('subdirectory', 'binary.file')
        self.assertTrue(binfile.is_file())

    def test_old_parameter(self):
        """
        Files used to take a 'package' parameter. Make sure anyone
        passing by name is still supported.
        """
        with suppress_known_deprecation():
            resources.files(package=self.data)


class OpenDiskTests(FilesTests, util.DiskSetup, unittest.TestCase):
    pass


class OpenZipTests(FilesTests, util.ZipSetup, unittest.TestCase):
    pass


class OpenNamespaceTests(FilesTests, util.DiskSetup, unittest.TestCase):
    MODULE = 'namespacedata01'


class OpenNamespaceZipTests(FilesTests, util.ZipSetup, unittest.TestCase):
    ZIP_MODULE = 'namespacedata01'


class SiteDir:
    def setUp(self):
        self.fixtures = contextlib.ExitStack()
        self.addCleanup(self.fixtures.close)
        self.site_dir = self.fixtures.enter_context(os_helper.temp_dir())
        self.fixtures.enter_context(import_helper.DirsOnSysPath(self.site_dir))
        self.fixtures.enter_context(import_helper.isolated_modules())


class DirectSpec:
    """
    Override behavior of ModuleSetup to write a full spec directly.
    """

    MODULE = 'unused'

    def load_fixture(self, name):
        self.tree_on_path(self.spec)


class ModulesFiles:
    spec = {
        'mod.py': '',
        'res.txt': 'resources are the best',
    }

    def test_module_resources(self):
        """
        A module can have resources found adjacent to the module.
        """
        import mod

        actual = resources.files(mod).joinpath('res.txt').read_text(encoding='utf-8')
        assert actual == self.spec['res.txt']


class ModuleFilesDiskTests(DirectSpec, util.DiskSetup, ModulesFiles, unittest.TestCase):
    pass


class ImplicitContextFiles:
    spec = {
        'somepkg': {
            '__init__.py': textwrap.dedent(
                """
                import importlib_resources as res
                val = res.files().joinpath('res.txt').read_text(encoding='utf-8')
                """
            ),
            'res.txt': 'resources are the best',
        },
    }

    def test_implicit_files(self):
        """
        Without any parameter, files() will infer the location as the caller.
        """
        assert importlib.import_module('somepkg').val == 'resources are the best'


class ImplicitContextFilesDiskTests(
    DirectSpec, util.DiskSetup, ImplicitContextFiles, unittest.TestCase
):
    pass


if __name__ == '__main__':
    unittest.main()
