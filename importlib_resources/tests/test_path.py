import io
import os
import pathlib
import unittest

import importlib_resources as resources
from importlib_resources.abc import TraversableResources
from . import data01
from . import util


class CommonTests(util.CommonTests, unittest.TestCase):
    def execute(self, package, path):
        with resources.path(package, path):
            pass


class PathTests:
    def test_reading(self):
        # Path should be readable.
        # Test also implicitly verifies the returned object is a pathlib.Path
        # instance.
        with resources.path(self.data, 'utf-8.file') as path:
            self.assertTrue(path.name.endswith("utf-8.file"), repr(path))
            # pathlib.Path.read_text() was introduced in Python 3.5.
            with path.open('r', encoding='utf-8') as file:
                text = file.read()
            self.assertEqual('Hello, UTF-8 world!\n', text)


class PathDiskTests(PathTests, unittest.TestCase):
    data = data01

    def test_natural_path(self):
        """
        Guarantee the internal implementation detail that
        file-system-backed resources do not get the tempdir
        treatment.
        """
        with resources.path(self.data, 'utf-8.file') as path:
            assert 'data' in str(path)


class PathMemoryTests(PathTests, unittest.TestCase):
    def setUp(self):
        file = io.BytesIO(b'Hello, UTF-8 world!\n')
        self.addCleanup(file.close)
        self.data = util.create_package(
            file=file, path=FileNotFoundError("package exists only in memory")
        )
        self.data.__spec__.origin = None
        self.data.__spec__.has_location = False


class PathZipTests(PathTests, util.ZipSetup, unittest.TestCase):
    def test_remove_in_context_manager(self):
        # It is not an error if the file that was temporarily stashed on the
        # file system is removed inside the `with` stanza.
        with resources.path(self.data, 'utf-8.file') as path:
            path.unlink()


class PathLikeTests(PathTests, unittest.TestCase):
    class PathLikeTraversable:
        """pathlib.Path proxy, is os.PathLike but is not pathlib.Path"""

        def __init__(self, *args, **kwargs):
            self._path = pathlib.Path(*args, **kwargs)

        def __fspath__(self):
            return os.fspath(self._path)

        def joinpath(self, other):
            return self.__class__(self, other)

        __truediv__ = joinpath

        @property
        def parent(self):
            return self.__class__(self._path.parent)

    class PathLikeResources(TraversableResources):
        def __init__(self, loader):
            self.path = PathLikeTests.PathLikeTraversable(loader.path).parent

        def get_resource_reader(self, package):
            return self

        def files(self):
            return self.path

    def setUp(self):
        reader = self.PathLikeResources(data01.__loader__)
        self.data = util.create_package_from_loader(reader)


if __name__ == '__main__':
    unittest.main()
