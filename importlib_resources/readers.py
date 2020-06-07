from . import abc

from ._compat import Path, ZipPath


class FileReader(abc.TraversableResources):
    def __init__(self, spec):
        self.path = Path(spec.origin).parent

    def files(self):
        return self.path


class ZipReader(FileReader):
    def __init__(self, spec):
        _, _, name = spec.name.rpartition('.')
        prefix = spec.loader.prefix.replace('\\', '/') + name + '/'
        self.path = ZipPath(spec.loader.archive, prefix)

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


class DegenerateReader(abc.TraversableResources):
    """
    A degenerate reader for loaders with no `get_resource_reader`
    """
    def __init__(self, spec):
        self.spec = spec

    class Path(abc.Traversable):
        def iterdir(self):
            return iter(())

        def read_bytes(self):
            raise ValueError()

        def read_text(self):
            raise ValueError()

        def is_dir(self):
            return False

        is_file = exists = is_dir

        def joinpath(self, other):
            return DegenerateReader.Path()

        __truediv__ = joinpath

        def name(self):
            return ''

        def open(self):
            raise ValueError()

    def files(self):
        return DegenerateReader.Path()
