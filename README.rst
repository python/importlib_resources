.. image:: https://img.shields.io/pypi/v/importlib_resources.svg
   :target: `PyPI link`_

.. image:: https://img.shields.io/pypi/pyversions/importlib_resources.svg
   :target: `PyPI link`_

.. _PyPI link: https://pypi.org/project/importlib_resources

.. image:: https://github.com/python/importlib_resources/workflows/tests/badge.svg
   :target: https://github.com/python/importlib_resources/actions?query=workflow%3A%22tests%22
   :alt: tests

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Code style: Black

.. image:: https://readthedocs.org/projects/importlib-resources/badge/?version=latest
   :target: https://importlib-resources.readthedocs.io/en/latest/?badge=latest

``importlib_resources`` is a backport of Python standard library
`importlib.resources
<https://docs.python.org/3/library/importlib.html#module-importlib.resources>`_
module for older Pythons.  Users of Python 3.9 and beyond
should use the standard library module, since for these versions,
``importlib_resources`` just delegates to that module.

The key goal of this module is to replace parts of `pkg_resources
<https://setuptools.readthedocs.io/en/latest/pkg_resources.html>`_ with a
solution in Python's stdlib that relies on well-defined APIs.  This makes
reading resources included in packages easier, with more stable and consistent
semantics.
