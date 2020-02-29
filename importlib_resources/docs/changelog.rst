==========================
 importlib_resources NEWS
==========================

1.1.0 (2020-02-29)
==================
* Add support for retrieving resources from subdirectories of packages
  through the new ``files()`` function, which returns a ``Traversable``
  object with ``joinpath`` and ``read_*`` interfaces matching those
  of ``pathlib.Path`` objects. This new function supersedes all of the
  previous functionality as it provides a more general-purpose access
  to a package's resources.

  With this function, subdirectories are supported (Closes #58).

  The
  documentation has been updated to reflect that this function is now
  the preferred interface for loading package resources. It does not,
  however, support resources from arbitrary loaders. It currently only
  supports resources from file system path and zipfile packages (a
  consequence of the ResourceReader interface only operating on
  Python packages).

1.0.2 (2018-11-01)
==================
* Fix ``setup_requires`` and ``install_requires`` metadata in ``setup.cfg``.
  Given by Anthony Sottile.

1.0.1 (2018-06-29)
==================
* Update Trove classifiers.  Closes #63

1.0 (2018-06-28)
================
* Backport fix for test isolation from Python 3.8/3.7.  Closes #61

0.8 (2018-05-17)
================
* Strip ``importlib_resources.__version__``.  Closes #56
* Fix a metadata problem with older setuptools.  Closes #57
* Add an ``__all__`` to ``importlib_resources``.  Closes #59

0.7 (2018-05-15)
================
* Fix ``setup.cfg`` metadata bug.  Closes #55

0.6 (2018-05-15)
================
* Move everything from ``pyproject.toml`` to ``setup.cfg``, with the added
  benefit of fixing the PyPI metadata.  Closes #54
* Turn off mypy's ``strict_optional`` setting for now.

0.5 (2018-05-01)
================
* Resynchronize with Python 3.7; changes the return type of ``contents()`` to
  be an ``Iterable``.  Closes #52

0.4 (2018-03-27)
================
* Correctly find resources in subpackages inside a zip file.  Closes #51

0.3 (2018-02-17)
================
* The API, implementation, and documentation is synchronized with the Python
  3.7 standard library.  Closes #47
* When run under Python 3.7 this API shadows the stdlib versions.  Closes #50

0.2 (2017-12-13)
================
* **Backward incompatible change**.  Split the ``open()`` and ``read()`` calls
  into separate binary and text versions, i.e. ``open_binary()``,
  ``open_text()``, ``read_binary()``, and ``read_text()``.  Closes #41
* Fix a bug where unrelated resources could be returned from ``contents()``.
  Closes #44
* Correctly prevent namespace packages from containing resources.  Closes #20

0.1 (2017-12-05)
================
* Initial release.


..
   Local Variables:
   mode: change-log-mode
   indent-tabs-mode: nil
   sentence-end-double-space: t
   fill-column: 78
   coding: utf-8
   End:
