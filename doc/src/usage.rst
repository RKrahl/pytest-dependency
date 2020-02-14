Using pytest-dependency
=======================

The plugin defines a new marker :func:`pytest.mark.dependency`.

.. _usage-basic:

Basic usage
-----------

Consider the following example test module:

.. literalinclude:: ../examples/basic.py

All the tests are decorated with :func:`pytest.mark.dependency`.  This
will cause the test results to be registered internally and thus other
tests may depend on them.  The list of dependencies of a test may be
set in the optional `depends` argument to the marker.  Running this
test, we will get the following result:

.. literalinclude:: ../examples/basic.out

The first test has deliberately been set to fail to illustrate the
effect.  We will get the following resuts:

`test_a`
  deliberately fails.

`test_b`
  succeeds.

`test_c`
  will be skipped because it depends on `test_a`.

`test_d`
  depends on `test_b` which did succeed.  It will be run and succeed
  as well.

`test_e`
  depends on `test_b` and `test_c`.  `test_b` did succeed, but
  `test_c` has been skipped.  So this one will also be skipped.

Naming tests
------------

Tests are referenced by their name in the `depends` argument.  The
default for this name is the node id defined by pytest, that is the
name of the test function, extended by the parameters if applicable,
see Section :ref:`names` for details.  In some cases, it's not easy to
predict the names of the node ids.  For this reason, the name of the
tests can be overridden by an explicit `name` argument to the marker.
The names must be unique.  The following example works exactly as the
last one, only the test names are explicitely set:

.. literalinclude:: ../examples/named.py

Using test classes
------------------

Tests may be grouped in classes in pytest.  Marking the dependencies
of methods in test classes works the same way as for simple test
functions.  In the following example we define two test classes.  Each
works in the same manner as the previous examples respectively:

.. literalinclude:: ../examples/testclass.py

In `TestClass` the default names for the tests are used, which is
build from the name of the class and the respective method in this
case, while in `TestClassNamed` these names are overridden by an
explicit `name` argument to the :func:`pytest.mark.dependency` marker.

.. versionchanged:: 0.3
   The name of the class is prepended to the method name to form the
   default name for the test.

.. _usage-parametrized:

Parametrized tests
------------------

In the same way as the :func:`pytest.mark.skip` and
:func:`pytest.mark.xfail` markers, the :func:`pytest.mark.dependency`
marker may be applied to individual test instances in the case of
parametrized tests.  Consider the following example:

.. literalinclude:: ../examples/parametrized.py

The test instance `test_a[0-1]`, named `a2` in the
:func:`pytest.mark.dependency` marker, is going to fail.  As a result,
the dependent tests `b1`, `b4`, `b5`, and in turn `c1` and `c3` will
be skipped.

Marking dependencies at runtime
-------------------------------

Sometimes, dependencies of test instances are too complicated to be
formulated explicitely beforehand using the
:func:`pytest.mark.dependency` marker.  It may be easier to compile
the list of dependencies of a test at run time.  In such cases, the
function :func:`pytest_dependency.depends` comes handy.  Consider the
following example:

.. literalinclude:: ../examples/runtime.py

Tests `test_c` and `test_d` set their dependencies at runtime calling
:func:`pytest_dependency.depends`.  The first argument is the value
of the `request` pytest fixture, the second argument is the list of
dependencies.  It has the same effect as passing this list as the
`depends` argument to the :func:`pytest.mark.dependency` marker.

The present example is certainly somewhat artificial, as the use of
the :func:`pytest_dependency.depends` function would not be needed in
such a simple case.  For a more involved example that can not as
easily be formulated with the static the `depends` argument, see
:ref:`advanced-grouping-fixtures`.
