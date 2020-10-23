import os.path

from . import abc

from ._compat import suppress, Path, ZipPath


class FileReader(abc.TraversableResources):
    def __init__(self, loader):
        self.path = Path(loader.path).parent

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
        self._paths = list(map(Path, set(paths)))
        if not self._paths:
            message = 'MultiplexedPath must contain at least one path'
            raise FileNotFoundError(message)
        if any(not path.is_dir() for path in self._paths):
            raise NotADirectoryError(
                'MultiplexedPath only supports directories')

    def iterdir(self):
        visited = []
        for path in self._paths:
            for file in path.iterdir():
                if file.name in visited:
                    continue
                visited.append(file.name)
                yield file

    def read_bytes(self):
        return self.open(mode='rb').read()

    def read_text(self, *args, **kwargs):
        return self.open(mode='r', *args, **kwargs).read()

    def is_dir(self):
        return True

    def is_file(self):
        return False

    def joinpath(self, child):
        # first try to find child in current paths
        for file in self.iterdir():
            if file.name == child:
                return file
        # if it does not exist, construct it with the first path
        return Path(os.path.join(self._paths[0], child))

    __truediv__ = joinpath

    def open(self, *args, **kwargs):
        for path in self._paths[:-1]:
            with suppress(Exception):
                return path.open(*args, **kwargs)
        return self._paths[-1].open(*args, **kwargs)

    def name(self):
        return os.path.basename(self._paths[0])

    def __repr__(self):
        return 'MultiplexedPath({})'.format(
            ', '.join("'{}'".format(path) for path in self._paths))


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
