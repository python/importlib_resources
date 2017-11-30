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
CONTENTS = [
    # filenames - the source will always be prepended by
    # importlib_resources/tests/data/ziptestdata.zip and the destination will
    # always be prepended by ziptestdata/
    '__init__.py',
    'binary.file',
    'utf-16.file',
    'utf-8.file',
    ]


zip_file_path = os.path.join(RELPATH, 'ziptestdata.zip')

with ZipFile(zip_file_path, 'w') as zf:
    for filename in CONTENTS:
        src = os.path.join(RELPATH, filename)
        dst = os.path.join('ziptestdata', filename)
        zf.write(src, dst)
