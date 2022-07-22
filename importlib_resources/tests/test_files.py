import typing
import unittest
import contextlib

import importlib_resources as resources
from importlib_resources.abc import Traversable
from . import data01
from . import util
from . import _path
from ._compat import os_helper, import_helper


class FilesTests:
    def test_read_bytes(self):
        files = resources.files(self.data)
        actual = files.joinpath('utf-8.file').read_bytes()
        assert actual == b'Hello, UTF-8 world!\n'

    def test_read_text(self):
        files = resources.files(self.data)
        actual = files.joinpath('utf-8.file').read_text(encoding='utf-8')
        assert actual == 'Hello, UTF-8 world!\n'

    @unittest.skipUnless(
        hasattr(typing, 'runtime_checkable'),
        "Only suitable when typing supports runtime_checkable",
    )
    def test_traversable(self):
        assert isinstance(resources.files(self.data), Traversable)


class OpenDiskTests(FilesTests, unittest.TestCase):
    def setUp(self):
        self.data = data01


class OpenZipTests(FilesTests, util.ZipSetup, unittest.TestCase):
    pass


class OpenNamespaceTests(FilesTests, unittest.TestCase):
    def setUp(self):
        from . import namespacedata01

        self.data = namespacedata01


class ModulesFilesTests(unittest.TestCase):
    def setUp(self):
        self.fixtures = contextlib.ExitStack()
        self.addCleanup(self.fixtures.close)
        self.site_dir = self.fixtures.enter_context(os_helper.temp_dir())
        self.fixtures.enter_context(import_helper.DirsOnSysPath(self.site_dir))
        self.fixtures.enter_context(import_helper.CleanImport())

    def test_module_resources(self):
        """
        A module can have resources found adjacent to the module.
        """
        spec = {
            'mod.py': '',
            'res.txt': 'resources are the best',
        }
        _path.build(spec, self.site_dir)
        import mod

        # currently a failure occurs; ref #203
        with self.assertRaisesRegex(TypeError, '.*mod.* is not a package'):
            actual = resources.files(mod).joinpath('res.txt').read_text()
            assert actual == spec['res.txt']


if __name__ == '__main__':
    unittest.main()
