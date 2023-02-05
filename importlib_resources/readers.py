import collections
import contextlib
import pathlib
import operator

from . import abc

from ._itertools import unique_everseen
from ._pathlib import by_type
from ._compat import ZipPath


def remove_duplicates(items):
    return iter(collections.OrderedDict.fromkeys(items))


class FileReader(abc.TraversableResources):
    def __init__(self, loader):
        self.path = pathlib.Path(loader.path).parent

    def resource_path(self, resource):
        """
        Return the file system path to prevent
        `resources.path()` from creating a temporary
        copy.
        """
        return str(self.path.joinpath(resource))

    def files(self):
        return self.path


class ZipReader(abc.TraversableResources):
    def __init__(self, loader, module):
        _, _, name = module.rpartition('.')
        self.prefix = loader.prefix.replace('\\', '/') + name + '/'
        self.archive = loader.archive

    def open_resource(self, resource):
        try:
            return super().open_resource(resource)
        except KeyError as exc:
            raise FileNotFoundError(exc.args[0])

    def is_resource(self, path):
        # workaround for `zipfile.Path.is_file` returning true
        # for non-existent paths.
        target = self.files().joinpath(path)
        return target.is_file() and target.exists()

    def files(self):
        return ZipPath(self.archive, self.prefix)


class MultiplexedPath(abc.Traversable):
    """
    Given a series of Traversable objects, implement a merged
    version of the interface across all objects. Useful for
    namespace packages which may be multihomed at a single
    name.
    """

    def __init__(self, *paths):
        self._paths = list(map(pathlib.Path, remove_duplicates(paths)))
        if not self._paths:
            message = 'MultiplexedPath must contain at least one path'
            raise FileNotFoundError(message)
        if not all(path.is_dir() for path in self._paths):
            raise NotADirectoryError('MultiplexedPath only supports directories')

    def iterdir(self):
        files = (file for path in self._paths for file in path.iterdir())
        return unique_everseen(files, key=operator.attrgetter('name'))

    def read_bytes(self):
        raise FileNotFoundError(f'{self} is not a file')

    def read_text(self, *args, **kwargs):
        raise FileNotFoundError(f'{self} is not a file')

    def is_dir(self):
        return True

    def is_file(self):
        return False

    def joinpath(self, *descendants):
        if not descendants:
            return self

        children = (
            joined
            for joined in (p.joinpath(*descendants) for p in self._paths)
            if joined.exists()
        )

        files, subdirs = by_type(children)

        return (
            # If a file matches, use it.
            next(files, None)
            # Attempt to construct a MultiplexedPath from subdirs.
            or self._maybe(subdirs)
            # No children matched, so return a non-existing path based on
            # the first path in self.
            or self._paths[0].joinpath(*descendants)
        )

    @classmethod
    def _maybe(cls, subdirs):
        """
        Construct a MultiplexedPath if needed.

        If the subdirs is empty, return None.
        If subdirs contains a sole element, return it.
        Otherwise, return a MultiplexedPath of the items.
        """
        try:
            result = cls(*subdirs)
        except FileNotFoundError:
            return

        with contextlib.suppress(ValueError):
            (result,) = result._paths

        return result

    def open(self, *args, **kwargs):
        raise FileNotFoundError(f'{self} is not a file')

    @property
    def name(self):
        return self._paths[0].name

    def __repr__(self):
        paths = ', '.join(f"'{path}'" for path in self._paths)
        return f'MultiplexedPath({paths})'


class NamespaceReader(abc.TraversableResources):
    def __init__(self, namespace_path):
        if 'NamespacePath' not in str(namespace_path):
            raise ValueError('Invalid path')
        self.path = MultiplexedPath(*list(namespace_path))

    def resource_path(self, resource):
        """
        Return the file system path to prevent
        `resources.path()` from creating a temporary
        copy.
        """
        return str(self.path.joinpath(resource))

    def files(self):
        return self.path
