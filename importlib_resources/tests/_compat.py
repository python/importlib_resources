try:
    # Python 3.10
    from test.support import import_helper
except ImportError:
    class import_helper:
        from test.support import modules_setup, modules_cleanup


try:
    from os import fspath
except ImportError:
    # Python 3.5
    fspath = str


try:
    # Python 3.10
    from test.support.os_helper import unlink
except ImportError:
    from test.support import unlink as _unlink

    def unlink(target):
        return _unlink(fspath(target))
