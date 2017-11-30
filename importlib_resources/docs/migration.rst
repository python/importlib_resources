.. _migration:

=================
 Migration guide
=================

The following guide will help you migrate common ``pkg_resources`` APIs to
``importlib_resources``.  Only a small number of the most common APIs are
supported by ``importlib_resources``, so projects that use other features
(e.g. entry points) will have to find other solutions.
``importlib_resources`` primarily supports the following `basic resource
access`_ APIs:

* ``pkg_resources.resource_filename()``
* ``pkg_resources.resource_stream()``
* ``pkg_resources.resource_string()``

Keep in mind that ``pkg_resources`` defines *resources* to include
directories.  ``importlib_resources`` does not treat directories as resources;
since only file are allowed as resources, file names in the
``importlib_resources`` API may *not* include path separators (e.g. slashes).


resource_filename()
===================

``resource_filename()`` is one of the more interesting APIs because it
guarantees that the return value names a file on the file system.  This means
that if the resource is in a zip file, ``pkg_resources()`` will extract the
file and return the name of the temporary file it created.  The problem is
that ``pkg_resources()`` also *implicitly* cleans up this temporary file,
without control or its lifetime by the programmer.

``importlib_resources`` takes a different approach.  Its equivalent API is the
``path()`` function, which returns a context manager providing a
:py:class:`pathlib.Path` object.  This means users have both the flexibility
and responsibility to manage the lifetime of the temporary file.  Note though
that if the resource is *already* on the file system, ``importlib_resources``
still returns a context manager, but nothing needs to get cleaned up.

Here's an example from ``pkg_resources()``::

    path = pkg_resources.resource_filename('my.package', 'resource.dat')

The best way to convert this is with the following idiom::

    with importlib_resources.path('my.package', 'resource.dat') as path:
        # Do something with path.  After the with-state exits, any temporary
        # file created will be immediately cleaned up.

That's all fine is you only need the file temporarily, but what if you need it
to stick around for a while?  One way of doing this is to use an
:py:class:`contextlib.ExitStack` instance and manage the resource explicitly::

    from contextlib import ExitStack
    file_manager = ExitStack()
    path = file_manager.enter_context(
        importlib_resources.path('my.package', 'resource.dat'))

Now ``path`` will continue to exist until you explicitly call
``file_manager.close()``.  What if you want the file to exist until the
process exits, or you can't pass ``file_manager`` around in your code?  Use an
:py:mod:`atexit` handler::

    import atexit
    file_manager = ExitStack()
    atexit.register(file_manager.close)
    path = file_manager.enter_context(
        importlib_resources.path('my.package', 'resource.dat'))

Assuming your Python interpreter exits gracefully, the temporary file will be
cleaned up when Python exits.


resource_stream()
=================

``pkg_resources.resource_stream()`` returns a readable file-like object opened
in binary mode.  When you read from the returned file-like object, you get
bytes.  E.g.::

    with pkg_resources.resource_stream('my.package', 'resource.dat') as fp:
        my_bytes = fp.read()

The equivalent code in ``importlib_resources`` is pretty straightforward::

    with importlib_resources.open('my.package', 'resource.dat') as fp:
        my_bytes = fp.read()


resource_string()
=================

In Python 2, ``pkg_resources.resource_string()`` returns the contents of a
resource as a ``str``.  In Python 3, this function is a misnomer; it actually
returns the contents of the named resource as ``bytes``.  That's why the
following example is often written for clarity as::

    from pkg_resources import resource_string as resource_bytes
    contents = resource_bytes('my.package', 'resource.dat')

This can be easily rewritten like so::

    contents = importlib_resources.read(
        'my.package', 'resource.dat', encoding=None)

The ``encoding=None`` argument is needed because by default ``read()`` returns
a ``unicode`` in Python 2 or a ``str`` in Python 3, read and decoded with the
``utf-8`` encoding.


.. _`basic resource access`: http://setuptools.readthedocs.io/en/latest/pkg_resources.html#basic-resource-access
