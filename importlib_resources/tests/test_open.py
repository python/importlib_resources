import unittest

from importlib_resources import files
from . import data01
from . import util
from .._compat import FileNotFoundError


class CommonBinaryTests(util.CommonTests, unittest.TestCase):
    def execute(self, package, path):
        with files(package).joinpath(path).open('rb'):
            pass


class CommonTextTests(util.CommonTests, unittest.TestCase):
    def execute(self, package, path):
        with files(package).joinpath(path).open():
            pass


class OpenTests:
    def test_open_binary(self):
        with files(self.data).joinpath('utf-8.file').open('rb') as fp:
            result = fp.read()
            self.assertEqual(result, b'Hello, UTF-8 world!\n')

    def test_open_text_default_encoding(self):
        with files(self.data).joinpath('utf-8.file').open() as fp:
            result = fp.read()
            self.assertEqual(result, 'Hello, UTF-8 world!\n')

    def test_open_text_given_encoding(self):
        path = files(self.data).joinpath('utf-16.file')
        with path.open(encoding='utf-16') as fp:
            result = fp.read()
        self.assertEqual(result, 'Hello, UTF-16 world!\n')

    def test_open_text_with_errors(self):
        # Raises UnicodeError without the 'errors' argument.
        path = files(self.data).joinpath('utf-16.file')
        with path.open(encoding='utf-8', errors='strict') as fp:
            self.assertRaises(UnicodeError, fp.read)
        with path.open(encoding='utf-8', errors='ignore') as fp:
            result = fp.read()
        self.assertEqual(
            result,
            'H\x00e\x00l\x00l\x00o\x00,\x00 '
            '\x00U\x00T\x00F\x00-\x001\x006\x00 '
            '\x00w\x00o\x00r\x00l\x00d\x00!\x00\n\x00')

    def test_open_binary_FileNotFoundError(self):
        path = files(self.data) / 'does-not-exist'
        self.assertRaises(
            FileNotFoundError,
            path.open,
            'rb')

    def test_open_text_FileNotFoundError(self):
        path = files(self.data) / 'does-not-exist'
        self.assertRaises(
            FileNotFoundError,
            path.open)


class OpenDiskTests(OpenTests, unittest.TestCase):
    def setUp(self):
        self.data = data01


class OpenZipTests(OpenTests, util.ZipSetup, unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
