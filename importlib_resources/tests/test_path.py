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
        with resources.path(package, path):
            pass


class PathTests(unittest.TestCase):

    def test_reading(self):
        # Path should be readable.
        # Test also implicitly verifies the returned object is a pathlib.Path
        # instance.
        with resources.path(data, 'utf-8.file') as path:
            # pathlib.Path.read_text() was introduced in Python 3.5.
            with path.open('r', encoding='utf-8') as file:
                text = file.read()
            self.assertEqual('Hello, UTF-8 world!\n', text)
