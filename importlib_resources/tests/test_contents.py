import unittest
import importlib_resources as resources

from . import data01
from . import util


class ContentsTests:
    @property
    def contents(self):
        return sorted(
            [el for el in list(resources.contents(self.data)) if el != '__pycache__']
        )


class ContentsDiskTests(ContentsTests, unittest.TestCase):
    def setUp(self):
        self.data = data01

    def test_contents(self):
        self.assertEqual(
            self.contents,
            [
                '__init__.py',
                'binary.file',
                'subdirectory',
                'utf-16.file',
                'utf-8.file',
            ],
        )


class ContentsZipTests(ContentsTests, util.ZipSetup, unittest.TestCase):
    def test_contents(self):
        self.assertEqual(
            self.contents,
            [
                '__init__.py',
                'binary.file',
                'subdirectory',
                'utf-16.file',
                'utf-8.file',
            ],
        )


class ContentsNamespaceTests(ContentsTests, unittest.TestCase):
    def setUp(self):
        from . import namespacedata01

        self.data = namespacedata01

    def test_contents(self):
        self.assertEqual(
            self.contents,
            [
                'binary.file',
                'utf-16.file',
                'utf-8.file',
            ],
        )
