#!/usr/bin/env python3

"""Remake the ziptestdata.zip file.

Run this to rebuild the importlib_resources/tests/data/ziptestdata.zip file,
e.g. if you want to add a new file to the zip.

This will replace the file with the new build, but it won't commit anything to
git.
"""

import os
from zipfile import ZipFile

RELPATH = 'importlib_resources/tests/data{suffix}'
BASEPATH = 'ziptestdata'
ZF_BASE = 'importlib_resources/tests/zipdata{suffix}/ziptestdata.zip'

for suffix in ('01', '02'):
    zfpath = ZF_BASE.format(suffix=suffix)
    with ZipFile(zfpath, 'w') as zf:
        relpath = RELPATH.format(suffix=suffix)
        for dirpath, dirnames, filenames in os.walk(relpath):
            for filename in filenames:
                src = os.path.join(dirpath, filename)
                if '__pycache__' in src:
                    continue
                if src == zfpath:
                    continue
                commonpath = os.path.commonpath((relpath, dirpath))
                dst = os.path.join(
                    BASEPATH, dirpath[len(commonpath)+1:], filename)
                print(src, '->', dst)
                zf.write(src, dst)
