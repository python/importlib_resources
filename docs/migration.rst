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
* ``pkg_resources.resource_listdir()``
* ``pkg_resources.resource_isdir()``

Note that although the steps below provide a drop-in replacement for the
above methods, for many use-cases, a better approach is to use the
``Traversable`` path from ``files()`` directly.


pkg_resources.resource_filename()
=================================

``resource_filename()`` is one of the more interesting APIs because it
guarantees that the return value names a file on the file system.  This means
that if the resource is in a zip file, ``pkg_resources`` will extract the
file and return the name of the temporary file it created.  The problem is
that ``pkg_resources`` also *implicitly* cleans up this temporary file,
without control over its lifetime by the programmer.

``importlib_resources`` takes a different approach.  Its equivalent API is the
``files()`` function, which returns a Traversable object implementing a
subset of the
:py:class:`pathlib.Path` interface suitable for reading the contents and
provides a wrapper for creating a temporary file on the system in a
context whose lifetime is managed by the user.  Note though
that if the resource is *already* on the file system, ``importlib_resources``
still returns a context manager, but nothing needs to get cleaned up.

Here's an example from ``pkg_resources``::

    path = pkg_resources.resource_filename('my.package', 'resource.dat')

The best way to convert this is with the following idiom::

    ref = importlib_resources.files('my.package') / 'resource.dat'
    with importlib_resources.as_file(ref) as path:
        # Do something with path.  After the with-statement exits, any
        # temporary file created will be immediately cleaned up.

That's all fine if you only need the file temporarily, but what if you need it
to stick around for a while?  One way of doing this is to use an
:py:class:`contextlib.ExitStack` instance and manage the resource explicitly::

    from contextlib import ExitStack
    file_manager = ExitStack()
    ref = importlib_resources.files('my.package') / 'resource.dat'
    path = file_manager.enter_context(
        importlib_resources.as_file(ref))

Now ``path`` will continue to exist until you explicitly call
``file_manager.close()``.  What if you want the file to exist until the
process exits, or you can't pass ``file_manager`` around in your code?  Use an
:py:mod:`atexit` handler::

    import atexit
    file_manager = ExitStack()
    atexit.register(file_manager.close)
    ref = importlib_resources.files('my.package') / 'resource.dat'
    path = file_manager.enter_context(
        importlib_resources.as_file(ref))

Assuming your Python interpreter exits gracefully, the temporary file will be
cleaned up when Python exits.


pkg_resources.resource_stream()
===============================

``pkg_resources.resource_stream()`` returns a readable file-like object opened
in binary mode.  When you read from the returned file-like object, you get
bytes.  E.g.::

    with pkg_resources.resource_stream('my.package', 'resource.dat') as fp:
        my_bytes = fp.read()

The equivalent code in ``importlib_resources`` is pretty straightforward::

    ref = importlib_resources.files('my.package').joinpath('resource.dat')
    with ref.open('rb') as fp:
        my_bytes = fp.read()


pkg_resources.resource_string()
===============================

In Python 2, ``pkg_resources.resource_string()`` returns the contents of a
resource as a ``str``.  In Python 3, this function is a misnomer; it actually
returns the contents of the named resource as ``bytes``.  That's why the
following example is often written for clarity as::

    from pkg_resources import resource_string as resource_bytes
    contents = resource_bytes('my.package', 'resource.dat')

This can be easily rewritten like so::

    ref = importlib_resources.files('my.package').joinpath('resource.dat')
    contents = f.read_bytes()


pkg_resources.resource_listdir()
================================

This function lists the entries in the package, both files and directories,
but it does not recurse into subdirectories, e.g.::

    for entry in pkg_resources.resource_listdir('my.package', 'subpackage'):
        print(entry)

This is easily rewritten using the following idiom::

    for entry in importlib_resources.files('my.package.subpackage').iterdir():
        print(entry.name)

Note:

* ``Traversable.iterdir()`` returns *all* the entries in the
  subpackage, i.e. both resources (files) and non-resources (directories).
* ``Traversable.iterdir()`` returns additional traversable objects, which if
  directories can also be iterated over (recursively).
* ``Traversable.iterdir()``, like ``pathlib.Path`` returns an iterator, not a
  concrete sequence.
* The order in which the elements are returned is undefined.


pkg_resources.resource_isdir()
==============================

You can ask ``pkg_resources`` to tell you whether a particular resource inside
a package is a directory or not::

    if pkg_resources.resource_isdir('my.package', 'resource'):
        print('A directory')

The ``importlib_resources`` equivalent is straightforward::

    if importlib_resources.files('my.package').joinpath('resource').is_dir():
        print('A directory')


.. _`basic resource access`: http://setuptools.readthedocs.io/en/latest/pkg_resources.html#basic-resource-access
