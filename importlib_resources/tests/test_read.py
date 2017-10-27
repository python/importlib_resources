import io
import os.path
import pathlib
import sys
import unittest

import importlib_resources as resources
from . import data
from . import util


class CommonTests(util.CommonTests, unittest.TestCase):

    def execute(self, package, path):
        resources.read(package, path)


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
