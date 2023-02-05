from ._itertools import bucket


def by_type(paths):
    """
    Bucket path objects into files and dirs.

    >>> import pathlib
    >>> files, dirs = by_type(pathlib.Path(__file__).parent.iterdir())
    >>> len(list(files)) > 1
    True
    >>> list(dirs)
    [...]
    >>> files, dirs = by_type(pathlib.Path().iterdir())
    >>> set(files) & set(dirs)
    set()
    """
    buckets = bucket(paths, key=lambda path: path.is_dir())
    return buckets[False], buckets[True]
