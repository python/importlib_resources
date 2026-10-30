import io
import unittest

from importlib_resources.simple import TraversableReader


class MemoryReader(TraversableReader):
    def __init__(self, package, resources=None, children=None):
        self._package = package
        self._resources = resources or {}
        self._children = children or []

    @property
    def package(self):
        return self._package

    def children(self):
        return self._children

    def resources(self):
        return list(self._resources)

    def open_binary(self, resource):
        return io.BytesIO(self._resources[resource])


class SimpleReaderTest(unittest.TestCase):
    def setUp(self):
        child = MemoryReader('sample.package.child', {'nested.txt': b'nested'})
        self.reader = MemoryReader(
            'sample.package',
            {'data.txt': 'hello, café'.encode()},
            [child],
        )

    def test_files(self):
        root = self.reader.files()
        assert root.name == 'package'
        assert root.is_dir()
        assert not root.is_file()
        assert root.joinpath() is root
        with self.assertRaises(IsADirectoryError):
            root.open()

    def test_iterdir(self):
        entries = {item.name: item for item in self.reader.files().iterdir()}
        assert set(entries) == {'data.txt', 'child'}
        assert entries['data.txt'].is_file()
        assert not entries['data.txt'].is_dir()
        assert entries['child'].is_dir()
        assert not entries['child'].is_file()
        assert set(self.reader.contents()) == {'data.txt', 'child'}

    def test_read_resource(self):
        resource = self.reader.files().joinpath('data.txt')
        assert resource.read_bytes() == 'hello, café'.encode()
        assert resource.read_text(encoding='utf-8') == 'hello, café'
        with self.reader.open_resource('data.txt') as stream:
            assert stream.read() == 'hello, café'.encode()
        assert self.reader.is_resource('data.txt')
        assert not self.reader.is_resource('child')

    def test_nested_resource(self):
        root = self.reader.files()
        assert root.joinpath('child', 'nested.txt').read_bytes() == b'nested'
        assert root.joinpath('child/nested.txt').read_bytes() == b'nested'
        assert (root / 'child' / 'nested.txt').read_bytes() == b'nested'

    def test_resource_has_no_children(self):
        resource = self.reader.files().joinpath('data.txt')
        assert list(resource.iterdir()) == []
        assert resource.joinpath() is resource
        with self.assertRaisesRegex(RuntimeError, 'Cannot traverse into a resource'):
            resource.joinpath('child')

    def test_empty_reader(self):
        root = MemoryReader('empty').files()
        assert root.name == 'empty'
        assert list(root.iterdir()) == []
