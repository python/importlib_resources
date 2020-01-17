=========================
 ``importlib_resources``
=========================

``importlib_resources`` is a backport of Python 3.7's standard library
`importlib.resources
<https://docs.python.org/3.7/library/importlib.html#module-importlib.resources>`_
module for Python 2.7, and 3.4 through 3.6.  Users of Python 3.7 and beyond
should use the standard library module, since for these versions,
``importlib_resources`` just delegates to that module.

The key goal of this module is to replace parts of `pkg_resources
<https://setuptools.readthedocs.io/en/latest/pkg_resources.html>`_ with a
solution in Python's stdlib that relies on well-defined APIs.  This makes
reading resources included in packages easier, with more stable and consistent
semantics.


Project details
===============

 * Project home: https://gitlab.com/python-devs/importlib_resources
 * Report bugs at: https://gitlab.com/python-devs/importlib_resources/issues
 * Code hosting: https://gitlab.com/python-devs/importlib_resources.git
 * Documentation: https://importlib-resources.readthedocs.io/
