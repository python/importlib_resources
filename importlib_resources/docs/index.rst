================================
 Welcome to importlib_resources
================================

``importlib_resources`` is a library which provides for access to *resources*
in Python packages.  It provides functionality similar to ``pkg_resources``
`Basic Resource Access`_ API, but without all of the overhead and performance
problems of ``pkg_resources``.

In our terminology, a *resource* is a file tree that is located within an
importable `Python package`_.  Resources can live on the file system or in a
zip file, with limited support for loader_ supporting the appropriate API for
reading resources.

``importlib_resources`` is a backport of Python 3.9's standard library
`importlib.resources`_ module for Python 2.7, and 3.5 through 3.8.  Users of
Python 3.9 and beyond are encouraged to use the standard library module.
Developers looking for detailed API descriptions should refer to the Python
3.9 standard library documentation.

The documentation here includes a general :ref:`usage <using>` guide and a
:ref:`migration <migration>` guide for projects that want to adopt
``importlib_resources`` instead of ``pkg_resources``.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   using.rst
   migration.rst
   changelog.rst


Project details
===============

 * Project home: https://gitlab.com/python-devs/importlib_resources
 * Report bugs at: https://gitlab.com/python-devs/importlib_resources/issues
 * Code hosting: https://gitlab.com/python-devs/importlib_resources.git
 * Documentation: http://importlib_resources.readthedocs.io/


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _`importlib.resources`: https://docs.python.org/3.7/library/importlib.html#module-importlib.resources
.. _`Basic Resource Access`: http://setuptools.readthedocs.io/en/latest/pkg_resources.html#basic-resource-access
.. _`Python package`: https://docs.python.org/3/reference/import.html#packages
.. _loader: https://docs.python.org/3/reference/import.html#finders-and-loaders
