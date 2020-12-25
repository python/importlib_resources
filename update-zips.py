#!/usr/bin/env python3

"""Remake the ziptestdata.zip file.

Run this to rebuild the importlib_resources/tests/data/ziptestdata.zip file,
e.g. if you want to add a new file to the zip.

This will replace the file with the new build, but it won't commit anything to
git.
"""

import contextlib
import os
from zipfile import ZipFile

RELPATH = 'importlib_resources/tests/data{suffix}'
BASEPATH = 'ziptestdata'
ZF_BASE = 'importlib_resources/tests/zipdata{suffix}/ziptestdata.zip'
suffixes = '01', '02'


def main():
    tuple(map(generate, suffixes))


def generate(suffix):
    zfpath = ZF_BASE.format(suffix=suffix)
    with ZipFile(zfpath, 'w') as zf:
        relpath = RELPATH.format(suffix=suffix)
        for dirpath, dirnames, filenames in os.walk(relpath):
            with contextlib.suppress(KeyError):
                dirnames.remove('__pycache__')
            for filename in filenames:
                src = os.path.join(dirpath, filename)
                if src == zfpath:
                    continue
                commonpath = os.path.commonpath((relpath, dirpath))
                dst = os.path.join(BASEPATH, dirpath[len(commonpath) + 1 :], filename)
                print(src, '->', dst)
                zf.write(src, dst)


__name__ == '__main__' and main()
