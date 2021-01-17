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
    basepath = pathlib.Path('ziptestdata')
    base = pathlib.Path('importlib_resources/tests')
    zfpath = base / f'zipdata{suffix}/ziptestdata.zip'
    with ZipFile(zfpath, 'w') as zf:
        datapath = base / f'data{suffix}'
        for dirpath, dirnames, filenames in os.walk(datapath):
            with contextlib.suppress(KeyError):
                dirnames.remove('__pycache__')
            loc = pathlib.Path(dirpath).relative_to(datapath)
            for filename in filenames:
                src = os.path.join(dirpath, filename)
                if src == zfpath:
                    continue
                dst = basepath / loc / filename
                print(src, '->', dst)
                zf.write(src, dst)


__name__ == '__main__' and main()
