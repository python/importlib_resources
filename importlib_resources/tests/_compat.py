try:
    from test.support import import_helper  # type: ignore
except ImportError:
    try:
        # Python 3.9 and earlier
        class import_helper:  # type: ignore
            from test.support import modules_setup, modules_cleanup
    except ImportError:
        from . import py27compat

        class import_helper:  # type: ignore
            modules_setup = staticmethod(py27compat.modules_setup)
            modules_cleanup = staticmethod(py27compat.modules_cleanup)


try:
    from os import fspath  # type: ignore
except ImportError:
    # Python 3.5
    fspath = str  # type: ignore


try:
    # Python 3.10
    from test.support.os_helper import unlink
except ImportError:
    from test.support import unlink as _unlink

    def unlink(target):
        return _unlink(fspath(target))
