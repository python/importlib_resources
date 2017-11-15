import os
import tempfile

from ._compat import FileNotFoundError
from __builtin__ import open as builtin_open
from contextlib import contextmanager
from importlib import import_module
from io import BytesIO
from pathlib2 import Path


def _get_package(package):
    # `package` will be a string or a module.  Always return a module which is
    # a package, otherwise raise an exception.
    if isinstance(package, basestring):                      # noqa: F821
        module = import_module(package)
    else:
        module = package
    if not hasattr(module, '__path__'):
        raise TypeError("{!r} is not a package".format(package))
    return module


def _normalize_path(path):
    # Ensure that the incoming `path`, which may be a string or a Path object,
    # is a bare file name with no hierarchy.
    str_path = str(path)
    parent, file_name = os.path.split(str_path)
    if parent:
        raise ValueError("{!r} must be only a file name".format(path))
    else:
        return file_name


def open(package, file_name):
    """Return a file-like object opened for binary-reading of the resource."""
    file_name = _normalize_path(file_name)
    package = _get_package(package)
    # Using pathlib doesn't work well here due to the lack of 'strict' argument
    # for pathlib.Path.resolve() prior to Python 3.6.
    package_path = os.path.dirname(package.__file__)
    relative_path = os.path.join(package_path, file_name)
    full_path = os.path.abspath(relative_path)
    try:
        return builtin_open(full_path, 'rb')
    except IOError:
        # This might be a package in a zip file.  zipimport provides a loader
        # with a functioning get_data() method, however we have to strip the
        # archive (i.e. the .zip file's name) off the front of the path.  This
        # is because the zipimport loader in Python 2 doesn't actually follow
        # PEP 302.  It should allow the full path, but actually requires that
        # the path be relative to the zip file.
        try:
            loader = package.__loader__
            full_path = relative_path[len(loader.archive)+1:]
            data = loader.get_data(full_path)
        except (IOError, AttributeError):
            package_name = package.__name__
            message = '{!r} resource not found in {!r}'.format(
                file_name, package_name)
            raise FileNotFoundError(message)
        else:
            return BytesIO(data)


def read(package, file_name, encoding='utf-8', errors='strict'):
    """Return the decoded string of the resource.

    The decoding-related arguments have the same semantics as those of
    bytes.decode().
    """
    file_name = _normalize_path(file_name)
    package = _get_package(package)
    # Note this is **not** builtins.open()!
    with open(package, file_name) as binary_file:
        return binary_file.read().decode(encoding=encoding, errors=errors)


@contextmanager
def path(package, file_name):
    """A context manager providing a file path object to the resource.

    If the resource does not already exist on its own on the file system,
    a temporary file will be created. If the file was created, the file
    will be deleted upon exiting the context manager (no exception is
    raised if the file was deleted prior to the context manager
    exiting).
    """
    file_name = _normalize_path(file_name)
    package = _get_package(package)
    package_directory = Path(package.__file__).parent
    file_path = package_directory / file_name
    # If the file actually exists on the file system, just return it.
    # Otherwise, it's probably in a zip file, so we need to create a temporary
    # file and copy the contents into that file, hence the contextmanager to
    # clean up the temp file resource.
    if file_path.exists():
        yield file_path
    else:
        # Note this is **not** builtins.open()!
        with open(package, file_name) as fileobj:
            data = fileobj.read()
        # Not using tempfile.NamedTemporaryFile as it leads to deeper 'try'
        # blocks due to the need to close the temporary file to work on Windows
        # properly.
        fd, raw_path = tempfile.mkstemp()
        try:
            os.write(fd, data)
            os.close(fd)
            yield Path(raw_path)
        finally:
            try:
                os.remove(raw_path)
            except FileNotFoundError:
                pass
