#!/usr/bin/env python3

"""Remake the ziptestdata.zip file.

Run this to rebuild the importlib_resources/tests/data/ziptestdata.zip file,
e.g. if you want to add a new file to the zip.

This will replace the file with the new build, but it won't commit anything to
git.
"""

import os
from zipfile import ZipFile

RELPATH = 'importlib_resources/tests/data'
BASEPATH = 'ziptestdata'
ZIP_FILE_PATH = 'importlib_resources/tests/zipdata/ziptestdata.zip'


with ZipFile(ZIP_FILE_PATH, 'w') as zf:
    for dirpath, dirnames, filenames in os.walk(RELPATH):
        for filename in filenames:
            src = os.path.join(dirpath, filename)
            if '__pycache__' in src:
                continue
            if src == ZIP_FILE_PATH:
                continue
            commonpath = os.path.commonpath((RELPATH, dirpath))
            dst = os.path.join(BASEPATH, dirpath[len(commonpath)+1:], filename)
            print(src, '->', dst)
            zf.write(src, dst)
