.. _using:

===========================
 Using importlib_resources
===========================

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

**This is a requirement for ``importlib_resources`` too!**

The problem with the ``pkg_resources`` approach is that, depending on the
structure of your package, ``pkg_resources`` can be very inefficient even to
just import.  ``pkg_resources`` is a sort of grab-bag of APIs and
functionalities, and to support all of this, it sometimes has to do a ton of
work at import time, e.g. to scan every package on your ``sys.path``.  This
can have a serious negative impact on things like command line startup time
for Python implement commands.

``importlib_resources`` solves this by being built entirely on the back of the
stdlib :py:mod:`importlib`.  By taking advantage of all the efficiencies in
Python's import system, and the fact that it's built into Python, using
``importlib_resources`` can be much more performant.  The equivalent code
using ``importlib_resources`` would look like::

    from importlib_resources import read
    # Reads contents with UTF-8 encoding and returns str.
    eml = read('email.tests.data', 'message.eml')


Packages or package names
=========================

All of the ``importlib_resources`` APIs take a *package* as their first
parameter, but this can either be a package name (as a ``str``) or an actual
module object, though the module *must* be a package [#fn1]_.  If a string is
passed in, it must name an importable Python package, and this is first
imported.  Thus the above example could also be written as::

    import email.tests.data
    eml = read(email.tests.data, 'message.eml')


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

    from importlib_resources import path
    with path(email.tests.data, 'message.eml') as eml:
        third_party_api_requiring_file_system_path(eml)

You can use all the standard :py:mod:`contextlib` APIs to manage this context
manager.


.. rubric:: Footnotes

.. [#fn1] Specifically, this means that in Python 2, the module object must
          have an ``__path__`` attribute, while in Python 3, the module's
          ``__spec__.submodule_search_locations`` must not be ``None``.
          Otherwise a ``TypeError`` is raised.


.. _`pkg_resources API`: http://setuptools.readthedocs.io/en/latest/pkg_resources.html#basic-resource-access
