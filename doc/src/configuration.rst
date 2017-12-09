Configuring pytest-dependency
=============================

This section explains configuration options for pytest-dependency and
also other configuration that is recommended for the use with
pytest-dependency.

Configuration file options
--------------------------

Configuration file options can be set in the `ini file`.

   minversion
      This is a builtin configuration of pytest itself.  Since
      pytest-dependency requires pytest 2.8.0 or newer, it is
      recommended to set this option accordingly.

   automark_dependency
      This is a flag.  If set to `False`, the default, the outcome of
      a test will only be registered if the test has been decorated
      with the :func:`pytest.mark.dependency` marker.  As a results,
      all tests, the dependencies and the dependent tests must be
      decorated.  If set to `True`, the outcome of all tests will be
      registered.  It has the same effect as if all tests are
      implicitly decorated with :func:`pytest.mark.dependency`.
