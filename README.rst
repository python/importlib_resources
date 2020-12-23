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
