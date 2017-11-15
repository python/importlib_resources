import sys

from setuptools import setup


requirements = []

# Python 2 is missing pathlib in its stdlib.
if sys.version_info < (3,):
    requirements.append('pathlib2')

# Python 3.4 is missing typing in its stdlib.
if (3,) <= sys.version_info < (3, 5):
    requirements.append('typing')


setup(
    name='importlib_resources',
    install_requires=requirements,
    )
