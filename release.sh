#!/bin/bash

source .tox/release/bin/activate
pip wheel -w wheels .
rm -rf artifacts
mkdir artifacts
mv wheels/importlib_resources*.whl artifacts/
python setup.py sdist
mv dist/importlib_resources*.tar.gz artifacts/
rm -rf wheels dist
