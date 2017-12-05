import sys
import unittest

import importlib_resources as resources
from . import data
from . import util


class ResourceTests:
    # Subclasses are expected to set the `data` attribute.

    def test_is_resource_good_path(self):
        self.assertTrue(resources.is_resource(self.data, 'binary.file'))

    def test_is_resource_missing(self):
        self.assertFalse(resources.is_resource(self.data, 'not-a-file'))

    def test_is_resource_subresource_directory(self):
        # Directories are not resources.
        self.assertFalse(resources.is_resource(self.data, 'subdirectory'))

    def test_contents(self):
        contents = set(resources.contents(self.data))
        # There may be cruft in the directory listing of the data directory.
        # Under Python 3 we could have a __pycache__ directory, and under
        # Python 2 we could have .pyc files.  These are both artifacts of the
        # test suite importing these modules and writing these caches.  They
        # aren't germane to this test, so just filter them out.
        contents.discard('__pycache__')
        contents.discard('__init__.pyc')
        contents.discard('__init__.pyo')
        self.assertEqual(contents, {
            '__init__.py',
            'subdirectory',
            'utf-8.file',
            'binary.file',
            'utf-16.file',
            })


class ResourceDiskTests(ResourceTests, unittest.TestCase):
    def setUp(self):
        self.data = data


class ResourceZipTests(ResourceTests, util.ZipSetup, unittest.TestCase):
    pass


@unittest.skipIf(sys.version_info < (3,), 'No ResourceReader in Python 2')
class ResourceLoaderTests(unittest.TestCase):
    def test_resource_contents(self):
        package = util.create_package(
            file=data, path=data.__file__, contents=['A', 'B', 'C'])
        self.assertEqual(
            set(resources.contents(package)),
            {'A', 'B', 'C'})

    def test_resource_is_resource(self):
        package = util.create_package(
            file=data, path=data.__file__,
            contents=['A', 'B', 'C', 'D/E', 'D/F'])
        self.assertTrue(resources.is_resource(package, 'B'))

    def test_resource_directory_is_not_resource(self):
        package = util.create_package(
            file=data, path=data.__file__,
            contents=['A', 'B', 'C', 'D/E', 'D/F'])
        self.assertFalse(resources.is_resource(package, 'D'))

    def test_resource_missing_is_not_resource(self):
        package = util.create_package(
            file=data, path=data.__file__,
            contents=['A', 'B', 'C', 'D/E', 'D/F'])
        self.assertFalse(resources.is_resource(package, 'Z'))


class ResourceCornerCaseTests(unittest.TestCase):
    def test_package_has_no_reader_fallback(self):
        # Test odd ball packages which:
        # 1. Do not have a ResourceReader as a loader
        # 2. Are not on the file system
        # 3. Are not in a zip file
        module = util.create_package(
            file=data, path=data.__file__, contents=['A', 'B', 'C'])
        # Give the module a dummy loader.
        module.__loader__ = object()
        # Give the module a dummy origin.
        module.__file__ = '/path/which/shall/not/be/named'
        if sys.version_info >= (3,):
            module.__spec__.loader = module.__loader__
            module.__spec__.origin = module.__file__
        self.assertFalse(resources.is_resource(module, 'A'))


if __name__ == '__main__':
    unittest.main()
