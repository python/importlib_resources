.. _using:

===========================
 Using importlib_resources
===========================

``importlib_resources`` is a library that leverages Python's import system to
provide access to *resources* within *packages*.  Given that this library is
built on top of the import system, it is highly efficient and easy to use.
This library's philosophy is that, if you can import a package, you can access
resources within that package.  Resources can be opened or read, in either
binary or text mode.

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
            resources1/
                resource1.1.txt
        two/
            __init__.py
            resource2.txt

then the directories are ``data``, ``data/one``, and ``data/two``.  Each of
these are also Python packages by virtue of the fact that they all contain
``__init__.py`` files [#fn1]_.  That means that in Python, all of these import
statements work::

    import data
    import data.one
    from data import two

Each import statement gives you a Python *module* corresponding to the
``__init__.py`` file in each of the respective directories.  These modules are
packages since packages are just special module instances that have an
additional attribute, namely a ``__path__`` [#fn2]_.

In this analogy then, resources are just files or directories contained in a
package directory, so
``data/one/resource1.txt`` and ``data/two/resource2.txt`` are both resources,
as are the ``__init__.py`` files in all the directories.

Resources are always accessed relative to the package that they live in.
``resource1.txt`` and ``resources1/resource1.1.txt`` are resources within
the ``data.one`` package, and
``two/resource2.txt`` is a resource within the
``data`` package.


Caveats
=======

Subdirectory Access
-------------------

Prior to importlib_resources 1.1 and the ``files()`` API, resources that were
not direct descendents of a package's folder were inaccessible through the
API, so in the example above ``resources1/resource1.1`` is not a resource of
the ``data.one`` package and ``two/resource2.txt`` is not a resource of the
``data`` package. Therefore, if subdirectory access is required, use the
``files()`` API.

Resource Reader Support
-----------------------

Due to the limitations on resource readers to access files beyond direct
descendents of a package, the ``files()`` API does not rely
on the importlib ResourceReader interface and thus only supports resources
exposed by the built-in path and zipfile loaders. If support for arbitrary
resource readers is required, the other API functions still support loading
those resources.

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


Packages or package names
=========================

All of the ``importlib_resources`` APIs take a *package* as their first
parameter, but this can either be a package name (as a ``str``) or an actual
module object, though the module *must* be a package [#fn3]_.  If a string is
passed in, it must name an importable Python package, and this is first
imported.  Thus the above example could also be written as::

    import email.tests.data
    eml = files(email.tests.data).joinpath('message.eml').read_text()


File system or zip file
=======================

In general you never have to worry whether your package is on the file system
or in a zip file, as the ``importlib_resources`` APIs hide those details from
you.  Sometimes though, you need a path to an actual file on the file system.
For example, some SSL APIs require a certificate file to be specified by a
real file system path, and C's ``dlopen()`` function also requires a real file
system path.

To support this, ``importlib_resources`` provides an API that will extract the
resource from a zip file to a temporary file, and return the file system path
to this temporary file as a :py:class:`pathlib.Path` object.  In order to
properly clean up this temporary file, what's actually returned is a context
manager that you can use in a ``with``-statement::

    from importlib_resources import files
    from importlib_resources.trees import as_file

    source = files(email.tests.data).joinpath('message.eml')
    with as_file(source) as eml:
        third_party_api_requiring_file_system_path(eml)

You can use all the standard :py:mod:`contextlib` APIs to manage this context
manager.

.. attention::

   There is an odd interaction with Python 3.4, 3.5, and 3.6 regarding adding
   zip or wheel file paths to ``sys.path``.  Due to limitations in `zipimport
   <https://docs.python.org/3/library/zipimport.html>`_, which can't be
   changed without breaking backward compatibility, you **must** use an
   absolute path to the zip/wheel file.  If you use a relative path, you will
   not be able to find resources inside these zip files.  E.g.:

   **No**::

       sys.path.append('relative/path/to/foo.whl')
       files('foo')  # This will fail!

   **Yes**::

       sys.path.append(os.path.abspath('relative/path/to/foo.whl'))
       files('foo')

Both relative and absolute paths work for Python 3.7 and newer.


.. rubric:: Footnotes

.. [#fn1] We're ignoring `PEP 420
          <https://www.python.org/dev/peps/pep-0420/>`_ style namespace
          packages, since ``importlib_resources`` does not support resources
          within namespace packages.  Also, the example assumes that the
          parent directory containing ``data/`` is on ``sys.path``.

.. [#fn2] As of `PEP 451 <https://www.python.org/dev/peps/pep-0451/>`_ this
          information is also available on the module's
          ``__spec__.submodule_search_locations`` attribute, which will not be
          ``None`` for packages.

.. [#fn3] Specifically, this means that in Python 2, the module object must
          have an ``__path__`` attribute, while in Python 3, the module's
          ``__spec__.submodule_search_locations`` must not be ``None``.
          Otherwise a ``TypeError`` is raised.


.. _`pkg_resources API`: http://setuptools.readthedocs.io/en/latest/pkg_resources.html#basic-resource-access
.. _`loader`: https://docs.python.org/3/reference/import.html#finders-and-loaders
.. _`ResourceReader`: https://docs.python.org/3.7/library/importlib.html#importlib.abc.ResourceReader
