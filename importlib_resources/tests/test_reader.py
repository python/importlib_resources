import os.path
import unittest

from importlib_resources.readers import MultiplexedPath

from .._compat import FileNotFoundError, NotADirectoryError


class MultiplexedPathTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder = os.path.abspath(
            os.path.join(__file__, '..', 'namespacedata01')
            )

    def test_init_no_paths(self):
        with self.assertRaises(FileNotFoundError):
            MultiplexedPath()

    def test_init_file(self):
        with self.assertRaises(NotADirectoryError):
            MultiplexedPath(os.path.join(self.folder, 'binary.file'))

    def test_iterdir(self):
        contents = {
            path.name for path in MultiplexedPath(self.folder).iterdir()
            }
        try:
            contents.remove('__pycache__')
        except (KeyError, ValueError):
            pass
        self.assertEqual(
            contents,
            {'binary.file', 'utf-16.file', 'utf-8.file'}
            )

    def test_iterdir_duplicate(self):
        data01 = os.path.abspath(
            os.path.join(__file__, '..', 'data01')
            )
        contents = {
            path.name for path in
            MultiplexedPath(self.folder, data01).iterdir()
            }
        for remove in ('__pycache__', '__init__.pyc'):
            try:
                contents.remove(remove)
            except (KeyError, ValueError):
                pass
        self.assertEqual(contents, {
            '__init__.py',
            'binary.file',
            'subdirectory',
            'utf-16.file',
            'utf-8.file'
            })

    def test_is_dir(self):
        self.assertEqual(MultiplexedPath(self.folder).is_dir(), True)

    def test_is_file(self):
        self.assertEqual(MultiplexedPath(self.folder).is_file(), False)

    def test_open_file(self):
        path = MultiplexedPath(self.folder)
        with self.assertRaises(FileNotFoundError):
            path.read_bytes()
        with self.assertRaises(FileNotFoundError):
            path.read_text()
        with self.assertRaises(FileNotFoundError):
            path.open()

    def test_join_path(self):
        print('test_join_path')
        prefix = os.path.abspath(os.path.join(__file__, '..'))
        data01 = os.path.join(prefix, 'data01')
        path = MultiplexedPath(self.folder, data01)
        self.assertEqual(
            str(path.joinpath('binary.file'))[len(prefix)+1:],
            os.path.join('namespacedata01', 'binary.file')
            )
        self.assertEqual(
            str(path.joinpath('subdirectory'))[len(prefix)+1:],
            os.path.join('data01', 'subdirectory')
            )
        self.assertEqual(
            str(path.joinpath('imaginary'))[len(prefix)+1:],
            os.path.join('namespacedata01', 'imaginary')
            )

    def test_repr(self):
        self.assertEqual(
            repr(MultiplexedPath(self.folder)),
            "MultiplexedPath('{}')".format(self.folder)
            )


if __name__ == '__main__':
    unittest.main()
