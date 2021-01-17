"""
Generate the zip test data files.

Run to build the tests/zipdataNN/ziptestdata.zip files from
files in tests/dataNN.

Replaces the file with the working copy, but does commit anything
to the source repo.
"""

import contextlib
import os
import pathlib
import zipfile


def main():
    """
    >>> from unittest import mock
    >>> monkeypatch = getfixture('monkeypatch')
    >>> monkeypatch.setattr(zipfile, 'ZipFile', mock.MagicMock())
    >>> main()
    .../data01/utf-16.file -> ziptestdata/utf-16.file
    .../data01/utf-8.file -> ziptestdata/utf-8.file
    .../data01/__init__.py -> ziptestdata/__init__.py
    .../data01/binary.file -> ziptestdata/binary.file
    .../data01/subdirectory/__init__.py -> ziptestdata/subdirectory/__init__.py
    .../data01/subdirectory/binary.file -> ziptestdata/subdirectory/binary.file
    .../data02/__init__.py -> ziptestdata/__init__.py
    .../data02/one/__init__.py -> ziptestdata/one/__init__.py
    .../data02/one/resource1.txt -> ziptestdata/one/resource1.txt
    .../data02/two/__init__.py -> ziptestdata/two/__init__.py
    .../data02/two/resource2.txt -> ziptestdata/two/resource2.txt
    """
    suffixes = '01', '02'
    tuple(map(generate, suffixes))


def generate(suffix):
    root = pathlib.Path(__file__).parent.relative_to(os.getcwd())
    zfpath = root / f'zipdata{suffix}/ziptestdata.zip'
    with zipfile.ZipFile(zfpath, 'w') as zf:
        for src, rel in walk(root / f'data{suffix}'):
            dst = 'ziptestdata' / rel
            print(src, '->', dst)
            zf.write(src, dst)


def walk(datapath):
    for dirpath, dirnames, filenames in os.walk(datapath):
        with contextlib.suppress(KeyError):
            dirnames.remove('__pycache__')
        for filename in filenames:
            res = pathlib.Path(dirpath) / filename
            rel = res.relative_to(datapath)
            yield res, rel


__name__ == '__main__' and main()
