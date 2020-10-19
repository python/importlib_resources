import sys


def modules_setup():
    return sys.modules.copy(),


def modules_cleanup(oldmodules):
    # Encoders/decoders are registered permanently within the internal
    # codec cache. If we destroy the corresponding modules their
    # globals will be set to None which will trip up the cached functions.
    encodings = [(k, v) for k, v in sys.modules.items()
                 if k.startswith('encodings.')]
    sys.modules.clear()
    sys.modules.update(encodings)
    # XXX: This kind of problem can affect more than just encodings.
    # In particular extension modules (such as _ssl) don't cope
    # with reloading properly. Really, test modules should be cleaning
    # out the test specific modules they know they added (ala test_runpy)
    # rather than relying on this function (as test_importhooks and test_pkg
    # do currently). Implicitly imported *real* modules should be left alone
    # (see issue 10556).
    sys.modules.update(oldmodules)
