.. _api:

=========================
 importlib_resources API
=========================

``importlib_resources`` exposes a small number of functions, and it references
a limited number of types, both as arguments to functions and as return types.


Types
=====

.. py:class:: Package

    ``Package`` types are defined as ``Union[ModuleType, str]``.  This means
    that where the function describes accepting a ``Package``, you can pass in
    either a module or a string.  Note that in Python 2, the module object
    *must* have a ``__path__`` attribute, while in Python 3, the module object
    must have a resolvable ``__spec__.submodule_search_locations`` that is not
    ``None``.

.. py:class:: Resource

    This type describes the resource names passed into the various functions
    in this package.  For Python 3.6 and later, this is defined as
    ``Union[str, os.PathLike]``.  For earlier versions (which don't have
    ``os.PathLike``), this is defined as ``str``.


Functions
=========

.. py:function:: importlib_resources.open_binary(package, resource)

    Open for binary reading the *resource* within *package*.

    :param package: A package name or module object.  See above for the API
                    that such module objects must support.
    :type package: ``Package``
    :param resource: The name of the resource to open within *package*.
                     *resource* may not contain path separators and it may
                     not have sub-resources (i.e. it cannot be a directory).
    :type resource: ``Resource``
    :returns: a binary I/O stream open for reading.
    :rtype: ``typing.io.BinaryIO``


.. py:function:: importlib_resources.open_text(package, resource, encoding='utf-8', errors='strict')

    Open for text reading the *resource* within *package*.  By default, the
    resource is opened for reading as UTF-8.

    :param package: A package name or module object.  See above for the API
                    that such module objects must support.
    :type package: ``Package``
    :param resource: The name of the resource to open within *package*.
                     *resource* may not contain path separators and it may
                     not have sub-resources (i.e. it cannot be a directory).
    :type resource: ``Resource``
    :param encoding: The encoding to open the resource in.  *encoding* has
                     the same meaning as with :py:func:`open`.
    :type encoding: str
    :param errors: This parameter has the same meaning as with :py:func:`open`.
    :type errors: str
    :returns: an I/O stream open for reading.
    :rtype: ``typing.TextIO``

.. py:function:: importlib_resources.read_binary(package, resource)

    Read and return the contents of the *resource* within *package* as ``bytes``.

    :param package: A package name or module object.  See above for the API
                    that such module objects must support.
    :type package: ``Package``
    :param resource: The name of the resource to read within *package*.
                     *resource* may not contain path separators and it may
                     not have sub-resources (i.e. it cannot be a directory).
    :type resource: ``Resource``
    :returns: the contents of the resource.
    :rtype: ``bytes``

.. py:function:: importlib_resources.read_text(package, resource, encoding='utf-8', errors='strict')

    Read and return the contents of *resource* within *package* as a ``str`` 
    [#fn1]_.  By default, the contents are read as strict UTF-8.

    :param package: A package name or module object.  See above for the API
                    that such module objects must support.
    :type package: ``Package``
    :param resource: The name of the resource to read within *package*.
                     *resource* may not contain path separators and it may
                     not have sub-resources (i.e. it cannot be a directory).
    :type resource: ``Resource``
    :param encoding: The encoding to read the contents of the resource in.
                     *encoding* has the same meaning as with :py:func:`open`.
    :type encoding: str
    :param errors: This parameter has the same meaning as with :py:func:`open`.
    :type errors: str
    :returns: the contents of the resource.
    :rtype: ``str``

.. py:function:: importlib_resources.path(package, resource)

    Return the path to the *resource* as an actual file system path.  This
    function returns a `context manager`_ for use in a ``with``-statement.
    The context manager provides a :py:class:`pathlib.Path` object.

    Exiting the context manager cleans up any temporary file created when the
    resource needs to be extracted from e.g. a zip file.

    :param package: A package name or module object.  See above for the API
                    that such module objects must support.
    :type package: ``Package``
    :param resource: The name of the resource to read within *package*.
                     *resource* may not contain path separators and it may
                     not have sub-resources (i.e. it cannot be a directory).
    :type resource: ``Resource``
    :returns: A context manager for use in a ``with``-statement.  Entering
              the context manager provides a :py:class:`pathlib.Path` object.
    :rtype: context manager providing a :py:class:`pathlib.Path` object


.. py:function:: importlib_resources.is_resource(package, name)

    Return ``True`` if there is a resource named *name* in the package,
    otherwise ``False``.  Remember that directories are *not* resources!

    :param package: A package name or module object.  See above for the API
                    that such module objects must support.
    :type package: ``Package``
    :param name: The name of the resource to read within *package*.
                 *resource* may not contain path separators and it may
                 not have sub-resources (i.e. it cannot be a directory).
    :type name: ``str``
    :returns: A flag indicating whether the resource exists or not.
    :rtype: ``bool``


.. py:function:: importlib_resources.contents(package)

    Return an iterator over the contents of the package.  The iterator can
    return resources (e.g. files) and non-resources (e.g. directories).  The
    iterator does not recurse into subdirectories.

    :param package: A package name or module object.  See above for the API
                    that such module objects must support.
    :type package: ``Package``
    :returns: The contents of the package, both resources and non-resources.
    :rtype: An iterator over ``str``


.. rubric:: Footnotes

.. [#fn1] The contents are returned as a ``str`` in Python 3, but as a
          ``unicode`` in Python 2.

.. _`context manager`: https://docs.python.org/3/library/stdtypes.html#typecontextmanager
