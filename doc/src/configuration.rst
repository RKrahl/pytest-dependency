Configuring pytest-dependency
=============================

This section explains configuration options for pytest-dependency, but
also options for pytest itself or other plugins that are recommended
for the use with pytest-dependency.

Notes on configuration for other plugins
----------------------------------------

pytest-xdist
   Test run parallelization in pytest-xdist is incompatible with
   pytest-dependency, see :ref:`install-other-packages`.  By default,
   parallelization is disabled in pytest-xdist (`--dist=no`).  You are
   advised to leave this default.

Configuration file options
--------------------------

Configuration file options can be set in the `ini file`.

minversion
   This is a builtin configuration option of pytest itself.  Since
   pytest-dependency requires pytest 3.7.0 or newer, it is recommended
   to set this option accordingly, either to 3.7.0 or to a newer
   version, if required by your test code.

automark_dependency
   This is a flag.  If set to `False`, the default, the outcome of a
   test will only be registered if the test has been decorated with
   the :func:`pytest.mark.dependency` marker.  As a results, all
   tests, the dependencies and the dependent tests must be decorated.
   If set to `True`, the outcome of all tests will be registered.  It
   has the same effect as implicitly decorating all tests with
   :func:`pytest.mark.dependency`.

   .. versionadded:: 0.3

Command line options
--------------------

The following command line options are added by pytest.dependency:

`--ignore-unknown-dependency`
   By default, a test will be skipped unless all the dependencies have
   been run successful.  If this option is set, a test will be skipped
   if any of the dependencies has been skipped or failed.
   E.g. dependencies that have not been run at all will be ignored.

   This may be useful if you run only a subset of the testsuite and
   some tests in the selected set are marked to depend on other tests
   that have not been selected.

   .. versionadded:: 0.3
