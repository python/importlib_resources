.. _using:

===========================
 Using importlib_resources
===========================

``importlib_resources`` is a library that leverages Python's import system to
provide access to *resources* within *packages* and alongside *modules*. Given
that this library is built on top of the import system, it is highly efficient
and easy to use. This library's philosophy is that, if one can import a
module, one can access resources associated with that module. Resources can be
opened or read, in either binary or text mode.

What exactly do we mean by "a resource"?  It's easiest to think about the
metaphor of files and directories on the file system, though it's important to
keep in mind that this is just a metaphor.  Resources and packages **do not**
have to exist as physical files and directories on the file system.

If you have a file system layout such as::

    data/
        __init__.py
        one/
            __init__.py
            resource1.txt
            module1.py
            resources1/
                resource1.1.txt
        two/
            __init__.py
            resource2.txt
    standalone.py
    resource3.txt

then the directories are ``data``, ``data/one``, and ``data/two``.  Each of
these are also Python packages by virtue of the fact that they all contain
``__init__.py`` files.  That means that in Python, all of these import
statements work::

    import data
    import data.one
    from data import two

Each import statement gives you a Python *module* corresponding to the
``__init__.py`` file in each of the respective directories.  These modules are
packages since packages are just special module instances that have an
additional attribute, namely a ``__path__`` [#fn1]_.

In this analogy then, resources are just files or directories contained in a
package directory, so
``data/one/resource1.txt`` and ``data/two/resource2.txt`` are both resources,
as are the ``__init__.py`` files in all the directories.

Resources in packages are always accessed relative to the package that they
live in. ``resource1.txt`` and ``resources1/resource1.1.txt`` are resources
within the ``data.one`` package, and ``two/resource2.txt`` is a resource
within the ``data`` package.

Resources may also be referenced relative to another *anchor*, a module in a
package (``data.one.module1``) or a standalone module (``standalone``). In
this case, resources are loaded from the same loader that loaded that module.


Example
=======

Let's say you are writing an email parsing library and in your test suite you
have a sample email message in a file called ``message.eml``.  You would like
to access the contents of this file for your tests, so you put this in your
project under the ``email/tests/data/message.eml`` path.  Let's say your unit
tests live in ``email/tests/test_email.py``.

Your test could read the data file by doing something like::

    data_dir = os.path.join(os.path.dirname(__file__), 'tests', 'data')
    data_path = os.path.join(data_dir, 'message.eml')
    with open(data_path, encoding='utf-8') as fp:
        eml = fp.read()

But there's a problem with this!  The use of ``__file__`` doesn't work if your
package lives inside a zip file, since in that case this code does not live on
the file system.

You could use the `pkg_resources API`_ like so::

    # In Python 3, resource_string() actually returns bytes!
    from pkg_resources import resource_string as resource_bytes
    eml = resource_bytes('email.tests.data', 'message.eml').decode('utf-8')

This requires you to make Python packages of both ``email/tests`` and
``email/tests/data``, by placing an empty ``__init__.py`` files in each of
those directories.

The problem with the ``pkg_resources`` approach is that, depending on the
packages in your environment, ``pkg_resources`` can be expensive
just to import.  This behavior
can have a serious negative impact on things like command line startup time
for Python implement commands.

``importlib_resources`` solves this performance challenge by being built
entirely on the back of the
stdlib :py:mod:`importlib`.  By taking advantage of all the efficiencies in
Python's import system, and the fact that it's built into Python, using
``importlib_resources`` can be much more performant.  The equivalent code
using ``importlib_resources`` would look like::

    from importlib_resources import files
    # Reads contents with UTF-8 encoding and returns str.
    eml = files('email.tests.data').joinpath('message.eml').read_text()


Anchors
=======

The ``importlib_resources`` ``files`` API takes an *anchor* as its first
parameter, which can either be a package name (as a ``str``) or an actual
module object.  If a string is passed in, it must name an importable Python
module, which is imported prior to loading any resources. Thus the above
example could also be written as::

    import email.tests.data
    eml = files(email.tests.data).joinpath('message.eml').read_text()


Namespace Packages
==================

``importlib_resources`` supports namespace packages as anchors just like
any other package. Similar to modules in a namespace package,
resources in a namespace package are not allowed to collide by name.
For example, if two packages both expose ``nspkg/data/foo.txt``, those
resources are unsupported by this library. The package will also likely
experience problems due to the collision with installers.

It's perfectly valid, however, for two packages to present different resources
in the same namespace package, regular package, or subdirectory.
For example, one package could expose ``nspkg/data/foo.txt`` and another
expose ``nspkg/data/bar.txt`` and those two packages could be installed
into separate paths, and the resources should be queryable::

    data = importlib_resources.files('nspkg').joinpath('data')
    data.joinpath('foo.txt').read_text()
    data.joinpath('bar.txt').read_text()


File system or zip file
=======================

A consumer need not worry whether any given package is on the file system
or in a zip file, as the ``importlib_resources`` APIs abstracts those details.
Sometimes though, the user needs a path to an actual file on the file system.
For example, some SSL APIs require a certificate file to be specified by a
real file system path, and C's ``dlopen()`` function also requires a real file
system path.

To support this need, ``importlib_resources`` provides an API to extract the
resource from a zip file to a temporary file or folder and return the file
system path to this materialized resource as a :py:class:`pathlib.Path`
object. In order to properly clean up this temporary file, what's actually
returned is a context manager for use in a ``with``-statement::

    from importlib_resources import files, as_file

    source = files(email.tests.data).joinpath('message.eml')
    with as_file(source) as eml:
        third_party_api_requiring_file_system_path(eml)

Use all the standard :py:mod:`contextlib` APIs to manage this context manager.


Migrating from Legacy
=====================

Starting with Python 3.9 and ``importlib_resources`` 1.4, this package
introduced the ``files()`` API, to be preferred over the legacy API,
i.e. the functions ``open_binary``, ``open_text``, ``path``,
``contents``, ``read_text``, ``read_binary``, and ``is_resource``.

To port to the ``files()`` API, refer to the
`_legacy module <https://github.com/python/importlib_resources/blob/66ea2dc7eb12b1be2322b7ad002cefb12d364dff/importlib_resources/_legacy.py>`_
to see simple wrappers that enable drop-in replacement based on the
preferred API, and either copy those or adapt the usage to utilize the
``files`` and
`Traversable <https://github.com/python/importlib_resources/blob/b665a3ea907d93b1b6457217f34e1bfc06f51fe6/importlib_resources/abc.py#L49-L114>`_
interfaces directly.


Extending
=========

Starting with Python 3.9 and ``importlib_resources`` 2.0, this package
provides an interface for non-standard loaders, such as those used by
executable bundlers, to supply resources. These loaders should supply a
``get_resource_reader`` method, which is passed a module name and
should return a ``TraversableResources`` instance.


.. rubric:: Footnotes

.. [#fn1] As of `PEP 451 <https://www.python.org/dev/peps/pep-0451/>`_ this
          information is also available on the module's
          ``__spec__.submodule_search_locations`` attribute, which will not be
          ``None`` for packages.

.. _`pkg_resources API`: http://setuptools.readthedocs.io/en/latest/pkg_resources.html#basic-resource-access
.. _`loader`: https://docs.python.org/3/reference/import.html#finders-and-loaders
.. _`ResourceReader`: https://docs.python.org/3.7/library/importlib.html#importlib.abc.ResourceReader
