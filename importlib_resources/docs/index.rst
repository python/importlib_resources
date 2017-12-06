================================
 Welcome to importlib_resources
================================

``importlib_resources`` is a library which provides for access to *resources*
in Python packages.  It provides functionality similar to ``pkg_resources``
`Basic Resource Access`_ API, but without all of the overhead and performance
problems of ``pkg_resources``.

In our terminology, a *resource* is a file that is located within an
importable `Python package`_.  Resources can live on the file system, in a zip
file, or in any place that has a loader_ supporting the appropriate API for
reading resources.  Directories are not resources.

``importlib_resources`` is a standalone version of the API available for users
of Python 2.7, or Python 3.4 through 3.6.  It is available in Python 3.7's
standard library as ``importlib.resources``.  Its API is currently
`provisional`_.

This documentation includes a general :ref:`usage <using>` guide and a
:ref:`migration <migration>` guide for projects that want to adopt
``importlib_resources`` instead of ``pkg_resources``.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   using.rst
   migration.rst
   api.rst
   abc.rst
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


.. _`Basic Resource Access`: http://setuptools.readthedocs.io/en/latest/pkg_resources.html#basic-resource-access
.. _`provisional`: https://www.python.org/dev/peps/pep-0411/
.. _`Python package`: https://docs.python.org/3/reference/import.html#packages
.. _loader: https://docs.python.org/3/reference/import.html#finders-and-loaders
