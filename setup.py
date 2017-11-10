import sys

from setuptools import setup


requirements = []
if sys.version_info < (3,):
    requirements.append('pathlib2')


setup(
    name='importlib_resources',
    install_requires=requirements,
    )
