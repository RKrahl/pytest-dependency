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
example for :ref:`usage-parametrized`.  The only difference is that
the lists of parameters are dynamically compiled beforehand.  The test
for child `l` deliberately fails, just to show the effect.  As a
consequence, the test for its parent `d` will be skipped.

.. _advanced-grouping-fixtures:

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

.. __: https://docs.pytest.org/en/stable/fixture.html#automatic-grouping-of-tests-by-fixture-instances

Depend on all instances of a parametrized test at once
------------------------------------------------------

If a test depends on a all instances of a parametrized test at once,
listing all of them in the :func:`pytest.mark.dependency` marker
explicitly might not be the best solution.  But you can dynamically
compile these lists from the parameter values, as in the following
example:

.. literalinclude:: ../examples/all_params.py

Here, `test_b`, `test_d`, and `test_f` will be skipped because they
depend on all instances of `test_a`, `test_c`, and `test_e`
respectively, but `test_a[13]`, `test_c[6-5]`, and `test_e[def]` fail.
The list of the test instances is compiled in the helper function
`instances()`.

Unfortunately you need knowledge how pytest encodes parameter values
in test instance names to write this helper function.  Note in
particular how lists of parameter values are compiled into one single
string in the case of multi parameter tests.  But also note that this
example of the `instances()` helper will only work for simple cases.
It requires the parameter values to be scalars that can easily be
converted to strings.  And it will fail if the same list of parameters
is passed to the same test more then once, because then, pytest will
add an index to the name to disambiguate the parameter values.

Logical combinations of dependencies
------------------------------------

The dependencies passed as in the `depends` argument to the
:func:`pytest.mark.dependency` marker are combined in an and-like
manner: the current test is skipped unless *all* dependencies did
succeed.  Sometimes one may want to combine the dependencies in a
different way.  This is not supported by pytest-dependency out of the
box, but it is not difficult to implement.  Consider the following
example:

.. literalinclude:: ../examples/or_dependency.py

The helper function `depends_or()` is similar to
:func:`pytest_dependency.depends`, it takes the same arguments.  The
only difference is that it combines the dependencies passed in the
`other` argument in an or-like manner: the current test will be run if
*at least one* of the other tests did succeed.

The tests `test_c`, `test_d`, `test_e`, and `test_f` in this example
all depend on two other tests.  Only `test_c` will be skipped, because
all tests in its dependency list fail.  The other ones are run,
because they have at least one succeeding test in their dependency
list.

Other logical combinations of dependencies are conceivable and may be
implemented in a similar way, according to the use case at hand.

.. note::
   The `depends_or()` helper function above is based on pytest
   internals: skipping of tests works by raising an exception and the
   exception class is exposed as :attr:`pytest.skip.Exception`.  This
   is not documented in pytest.  It has been tested to work for pytest
   versions 3.7.0 through 6.2.5, but it is not guaranteed to be stable
   for future pytest versions.
