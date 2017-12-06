========================
 The ResourceReader ABC
========================

``importlib_resources`` relies heavily on a package's module loader_ for
accessing that package's resources, with fallbacks for common cases when the
loader doesn't provide this information (e.g. for zip files in versions of
Python before 3.7).  These fallbacks are not perfect, and there will be cases
where custom loaders are implemented which subvert the usefulness of these
fallback.

For this reason, a new `abstract base class`_ is introduced for loaders that
want to participate in resource introspection and access.  Loaders can
implement the ``ResourceReader`` ABC to provide support for resources where
the fallbacks don't work, or for providing more efficient access to
resources.

``importlib_resources`` will first [#fn1]_ introspect the package's loader to
see if it supports the ``ResourceReader`` interface.  If it does, it will use
that for all resource access.


ResourceReader API
==================

The ``ResourceReader`` ABC decorates its methods with ``@abstractmethod`` to
indicate that they must all be overridden by the loader that implements this
interface.  However, the default implementation of each of these methods is to
raise :py:exc:`FileNotFoundError` rather than :py:exc:`NotImplementedError`.
This is so that if the ABC method is accidentally called,
``importlib_resources`` should still be able to try its fallbacks.


.. py:class:: ResourceReader

   The abstract base class for loaders to implement if they provide resource
   reading and access support.  Loaders should implement all of these methods.

   .. py:method:: open_resource(resource)

      Open the named **resource** for binary reading.  The argument must be
      filename-like, i.e. it cannot have any path separators in the string.
      If the resource cannot be found, :py:exc:`FileNotFoundError` should be
      raised.

      :param resource: The resource within the package to open.
      :type resource: importlib_resources.Resource
      :return: A stream open for binary reading.  Text decoding is handled at
               a higher level.
      :rtype: typing.BinaryIO
      :raises FileNotFoundError: when the named resource is not found within
                                 the package.

   .. py:method:: resource_path(resource)

      Return the path to the named **resource** as found on the file
      system.

      If the resource is not natively accessible on the file system
      (e.g. can't be accessed through :py:class:`pathlib.Path`), then
      :py:exc:`FileNotFoundError` should be raised.  In this case,
      :py:meth:`importlib_resources.path()` will read the contents of the
      resource, create a temporary file, and return a context manager that
      will manage the lifetime of the temporary file.

      :param resource: The resource within the package to open.
      :type resource: importlib_resources.Resource
      :return: The path to the named resource, relative to the package.
      :rtype: str
      :raises FileNotFoundError: when the named resource is not found within
                                 the package, or the resources is not directly
                                 accessible on the file system.

   .. py:method:: is_resource(name)

      Return a boolean indicating whether **name** is a resource within the
      package.  *Remember that directories are not resources!*

      :param name: A filename-like string (i.e. no path separators) to check
                   whether it is a resource within the package.
      :type resource: str
      :return: Flag indicating whether **name** is a resource or not.
      :rtype: bool
      :raises FileNotFoundError: when the named resource is not found within
                                 the package.

   .. py:method:: contents()

      Return a sequence of all the contents of the package.  This is like
      doing a directory listing.  This returns resources (e.g. file names) and
      non-resource (e.g. subdirectories) alike.  Thus, entries in this
      sequence may or may not be resources.

      :return: A sequence of string names.
      :rtype: Iterator[str]

.. rubric:: Footnotes

.. [#fn1] In Python 3 only.  ``importlib_resources`` does not support the
          ``ResourceReader`` ABC for Python 2.

.. _loader: https://docs.python.org/3/reference/import.html#finders-and-loaders
.. _`abstract base class`: https://docs.python.org/3/library/abc.html
