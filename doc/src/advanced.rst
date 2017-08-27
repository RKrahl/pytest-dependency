Advanced usage
==============

This section contains some advanced examples for using
pytest-dependency.

Dynamic compilation of marked parameters
----------------------------------------

Sometimes, the parameter values for parametrized tests cannot easily
be typed as a simple list.  It may need to be compiled at run time
depending on a set of test data.  This also works together with
marking dependencies in the individual test instances.

Consider the following example test module:

.. literalinclude:: ../examples/dyn-parametrized.py

In principle, this example works the very same way as the basic
example for parametrized tests, see :ref:`usage-parametrized`.  The
only difference is that the lists of paramters are dynamically
compiled beforehand.  The test for child `l` deliberately fails, just
to show the effect.  As a consequence, the test for its parent `d`
will be skipped.

Grouping tests using fixtures
-----------------------------

pytest features the `automatic grouping of tests by fixture
instances`__.  This is particularly useful if there is a set of test
cases and a series of tests shall be run for each of the test case
respectively.

Consider the following example:

.. literalinclude:: ../examples/group-fixture.py

The test instances of `test_b` depend on `test_a` for the same
parameter value.  The test `test_a[7]` deliberately fails, as a
consequence `test_b[7]` will be skipped.  Note that we need to call
:func:`pytest_dependency.depends` to mark the dependencies, because
there is no way to use the :func:`pytest.mark.dependency` marker on
the parameter values here.

If many tests in the series depend on a single test, it might be an
option, to move the call to :func:`pytest_dependency.depends` in a
fixture on its own.  Consider:

.. literalinclude:: ../examples/group-fixture2.py

In this example, both `test_b[7]` and `test_c[7]` are skipped, because
`test_a[7]` deliberately fails.

.. __: https://docs.pytest.org/en/latest/fixture.html#automatic-grouping-of-tests-by-fixture-instances
