=========================
 ``importlib.resources``
=========================

This repository is to house the design and implementation of a planned
``importlib.resources`` module for Python's stdlib -- aiming for Python 3.7 --
along with a backport to target Python 2.7, and 3.4 - 3.6.

The key goal of this module is to replace parts of `pkg_resources
<https://setuptools.readthedocs.io/en/latest/pkg_resources.html>`_ with a
solution in Python's stdlib that relies on well-defined APIs.  This should not
only make reading resources included in packages easier, but have the
semantics be stable and consistent.


Project details
===============

 * Project home: https://gitlab.com/python-devs/importlib_resources
 * Report bugs at: https://gitlab.com/python-devs/importlib_resources/issues
 * Code hosting: https://gitlab.com/python-devs/importlib_resources.git
 * Documentation: http://importlib_resources.readthedocs.io/
