import unittest

import importlib_resources as resources
from . import data
from . import util
from .._compat import FileNotFoundError


class CommonTests(util.CommonTests, unittest.TestCase):

    def execute(self, package, path):
        with resources.open(package, path):
            pass


class OpenTests:

    # Subclasses are expected to set the 'data' attribute.

    def test_open_for_binary(self):
        # By default, the resource is opened for binary reads.
        with resources.open(self.data, 'utf-8.file') as fp:
            self.assertEqual(b'Hello, UTF-8 world!\n', fp.read())

    def test_wrap_for_text(self):
        # The file-like object can be wrapped for text reading.
        with resources.open(self.data, 'utf-8.file') as fp:
            text = fp.read().decode(encoding='utf-8')
            self.assertEqual('Hello, UTF-8 world!\n', text)

    def test_FileNotFoundError(self):
        with self.assertRaises(FileNotFoundError):
            with resources.open(self.data, 'does-not-exist'):
                pass

    def test_open_for_text(self):
        # open() takes an optional encoding and errors parameter.
        with resources.open(self.data, 'utf-8.file', 'utf-8', 'strict') as fp:
            self.assertEqual('Hello, UTF-8 world!\n', fp.read())


class OpenDiskTests(OpenTests, unittest.TestCase):

    def setUp(self):
        self.data = data


class OpenZipTests(OpenTests, util.ZipSetup, unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
