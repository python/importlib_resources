==========================
 importlib_resources NEWS
==========================

0.3 (2018-02-17)
================
* The API, implementation, and documenttion is synchronized with the Python
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
