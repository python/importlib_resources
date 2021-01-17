#!/usr/bin/env python3

"""Remake the ziptestdata.zip file.

Run this to rebuild the importlib_resources/tests/data/ziptestdata.zip file,
e.g. if you want to add a new file to the zip.

This will replace the file with the new build, but it won't commit anything to
git.
"""

import contextlib
import os
import pathlib
from zipfile import ZipFile


def main():
    suffixes = '01', '02'
    tuple(map(generate, suffixes))


def generate(suffix):
    root = pathlib.Path('importlib_resources/tests')
    zfpath = root / f'zipdata{suffix}/ziptestdata.zip'
    with ZipFile(zfpath, 'w') as zf:
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
