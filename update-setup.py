#!/usr/bin/env python3

"""Update the setup.py"""

import os
import tarfile

from contextlib import ExitStack
from flit.buildapi import build_sdist
from flit.sdist import SdistBuilder
from io import TextIOWrapper
from tempfile import TemporaryDirectory
from unittest.mock import patch

# Horrible hack alert.  We have to trick flit into thinking that setup.py
# isn't being tracked by git because otherwise, it will use the existing
# setup.py instead of generating one from flit.ini.
#
# But we can't delete setup.py permanently because we have a chicken-and-egg
# problem!  tox requires the setup.py and there are no hooks available to run
# update-setup.py before tox builds its virtual environments.
#
# We also can't delete setup.py temporarily because flit *also* does a check
# that the git repository isn't dirty.  So we're in a Catch 22.
#
# The solution is to mock the function that flit uses to determine which files
# are tracked by git, and to forcibly remove `setup.py` from that list.


class SneakySdistBuilder(SdistBuilder):
    def find_tracked_files(self):
        file_set = super().find_tracked_files()
        file_set.remove('setup.py')
        return file_set


with ExitStack() as resources:
    enter = resources.enter_context
    td = enter(TemporaryDirectory())
    enter(patch('flit.buildapi.SdistBuilder', SneakySdistBuilder))
    filename = build_sdist(td)
    tf = enter(tarfile.open(os.path.join(td, filename)))
    for name in tf.getnames():
        if os.path.basename(name) == 'setup.py':
            with tf.extractfile(name) as infp:
                setup_py = TextIOWrapper(infp, 'utf-8').read()
            outfp = enter(open('setup.py', 'w', encoding='utf-8'))
            wrote_preamble = False
            for line in setup_py.splitlines():
                if not wrote_preamble and not line.startswith('#'):
                    print("""
# Do not modify this file by hand!  Run ./update-setup.py instead.
""", file=outfp)
                    wrote_preamble = True
                else:
                    print(line, file=outfp)
