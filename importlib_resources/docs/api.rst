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

.. py:class:: FileName

    This type describes the resource names passed into the various functions
    in this package.  For Python 3.6 and later, this is defined as
    ``Union[str, os.PathLike]``.  For earlier versions (which don't have
    ``os.PathLike``), this is defined as ``str``.


Functions
=========

.. py:function:: importlib_resources.open(package, file_name, encoding=None, errors=None)

    Open for reading the resource named ``file_name`` within the ``package``
    package.  By default, the resource is opened for reading in binary mode.
    With a non-``None`` ``encoding`` argument, the resource is opened in text
    mode, with ``errors`` having the same meaning as for built-in
    :py:func:`open`.

    :param package: A package name or module object.  See above for the API
                    that such module objects must support.
    :type package: ``Package``
    :param file_name: The name of the resource to open within ``package``.
                      ``file_name`` may not contain path separators and it may
                      not have sub-resources (i.e. it cannot be a directory).
    :type file_name: ``FileName``
    :param encoding: When ``None``, the resource is opened in binary mode.
                     When an encoding is given, the resource is opened in text
                     mode.  ``encoding`` has the same meaning as with
                     :py:func:`open`.
    :type encoding: str
    :param errors: This parameter is ignored when ``encoding`` is ``None``.
                   Otherwise it has the same meaning as with :py:func:`open`.
    :type errors: str
    :returns: an I/O stream open for reading.
    :rtype: ``typing.IO``


.. py:function:: importlib_resources.read(package, file_name, encoding='utf-8', errors='strict')

    Read and return the contents of the resource named ``file_name`` within
    the ``package`` package.  By default, the contents are read in UTF-8 and
    returned as a ``str`` (in Python 3 - ``unicode`` in Python 2).  With
    ``encoding`` set to ``None``, the resource contents are read in binary
    mode and returned as ``bytes``.

    :param package: A package name or module object.  See above for the API
                    that such module objects must support.
    :type package: ``Package``
    :param file_name: The name of the resource to read within ``package``.
                      ``file_name`` may not contain path separators and it may
                      not have sub-resources (i.e. it cannot be a directory).
    :type file_name: ``FileName``
    :param encoding: When ``None``, the resource is read in binary mode.
                     When an encoding is given, the resource is read in text
                     mode.  ``encoding`` has the same meaning as with
                     :py:func:`open`.
    :type encoding: str
    :param errors: This parameter is ignored when ``encoding`` is ``None``.
                   Otherwise it has the same meaning as with :py:func:`open`.
    :type errors: str
    :returns: the contents of the resource.
    :rtype: ``bytes`` or ``str``

.. py:function:: importlib_resources.path(package, file_name)

    Return the path to the resource as an actual file system path.  This
    function returns a `context manager`_ for use in a ``with``-statement.
    The context manager provides a :py:class:`pathlib.Path` object.

    Exiting the context manager cleans up any temporary file created when the
    resource needs to be extracted from e.g. a zip file.

    :param package: A package name or module object.  See above for the API
                    that such module objects must support.
    :type package: ``Package``
    :param file_name: The name of the resource to read within ``package``.
                      ``file_name`` may not contain path separators and it may
                      not have sub-resources (i.e. it cannot be a directory).
    :type file_name: ``FileName``
    :returns: A context manager for use in a ``with``-statement.  Entering
              the context manager provides a :py:class:`pathlib.Path`
              object.
    :rtype: context manager providing a :py:class:`pathlib.Path` object


.. _`context manager`: https://docs.python.org/3/library/stdtypes.html#typecontextmanager
