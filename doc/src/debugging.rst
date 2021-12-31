Debugging guide
===============

This section is supposed to provide hints on what to check if
pytest-dependency does not seem to behave as expected.

Example
-------

We consider the following example in this guide:

.. literalinclude:: ../examples/debugging.py

This example contains several cases where the presumably intended
behavior of the code differs from what happens in practice.  We will
show below how diagnostic tools in pytest may be used to unravel the
discrepancies.  The results that may (or may not) be surprising
include:

+ The test method `test_c` in class `TestClass` depending on `test_b`
  is run, although the test method `test_b` fails.

+ All instances of `test_colors` succeed.  Yet `test_multicolored`
  that only depends on `test_colors` is skipped.

+ Similarly `test_alert` depending only on `test_colors[Color.RED]` is
  skipped, although `test_colors` with the parameter value `Color.RED`
  succeeds.

+ `test_k` depending only on `test_b` is skipped, although `test_b`
  succeeds.

+ Same with `test_m` depending only on `test_b` is skipped.

+ `test_o` depending only on `test_h` is skipped, although `test_h`
  succeeds.

+ `test_q` depending only on `test_p` is skipped, although `test_p`
  succeeds.

+ `test_r` is run, although `test_a` fails.

+ `test_s` depending only on `test_l` is skipped, although `test_l`
  succeeds.

Diagnostic tools
----------------

There are different ways to request diagnostic output from pytest.  We
will discuss how they may be used to better understand the behavior of
pytest-dependency.

pytest summary
..............

You can request a short summary from pytest including information on
skipped tests using the ``-rs`` `command line option`__:

.. literalinclude:: ../examples/debugging-summary.out

This summary indicates if a test has been skipped by pytest-dependency
in the first place.  In the present example, the summary hints that
`test_k` has been skipped due to another reason, unrelated to
pytest-dependency.  If the test has been skipped by pytest-dependency,
the summary displays the name of the missing dependency.

.. __: https://docs.pytest.org/en/stable/usage.html#detailed-summary-report

Verbose pytest output
.....................

A list of all tests with their respective outcome will be displayed if
you call pytest with the ``--verbose`` command line option:

.. literalinclude:: ../examples/debugging-verbose.out

The verbose listing is particular useful, because it shows the pytest
node id for each test, which is not always obvious.  As explained in
Section :ref:`names`, this node id is the basis to form the default
test name that need to be used to reference the test in the
dependencies.

From this list we can understand why `test_multicolored` has been
skipped: it depends on `test_colors`.  But `test_colors` is
parametrized and thus the parameter value is included in the node id.
As a result, a dependency by the name `test_colors` can not be found.
The same thing happens in the case of `test_s`: it depends on
`test_l`, but the latter uses a parametrized fixture, so it indirectly
takes a parameter value and that value must be included in the
reference for the dependency.

In the case of `test_alert`, the parameter value is included in the
dependency `test_colors[Color.RED]`.  But in the node id as displayed
in the verbose list, that test appears as `test_colors[RED]`.  Note
that `class Color` overrides the string representation operator and
that affects how the parameter value appears in the node id in this
case.

The verbose list also displays the execution order of the tests.  In
the present example, this order differs from the order in the source
code.  That is the reason why both instances of `test_q` are skipped:
they are executed before the dependency `test_p`.  So the outcome of
the latter is yet unknown at the moment that the dependency is
checked.

Logging
.......

pytest-dependency emits log messages when registering test results and
when checking dependencies for a test.  You can request these log
messages to be displayed at runtime using `log command line options`__
in the pytest call.  Beware that this may produce a large amount of
output, even for medium size test suites.  We will present only a few
fragments of the output here.  Consider the start of that output,
covering the first test `test_a`:

.. literalinclude:: ../examples/debugging-logging.out
   :end-before: debugging.py::test_b

It is shown how the test outcome for each of the three test phases
(setup, call, and teardown) is registered in pytest-dependency.  It is
also shown which name is used to register the test outcome depending
on the scope.

Considering the relevant fragments of the output, we can check why
`TestClass::test_c` is not skipped:

.. literalinclude:: ../examples/debugging-logging.out
   :lines: 20-31,86-116

The dependency `test_b` is checked in module scope.  If that
dependency was meant to reference the method of the same class, it
would either need to be referenced as `test_b` in class scope or as
`TestClass::test_b` in module scope or as
`debugging.py::TestClass::test_b` in session scope.  The way it is
formulated in the example, it actually references the test function
`test_b`, which succeeds.

A similar case is `test_m`:

.. literalinclude:: ../examples/debugging-logging.out
   :lines: 20-31,264-274

The dependency `test_b` is checked in session scope.  There is no test
that matches this name.  If that dependency was mean to reference the
test function `test_b` in the example, it would either need to be
referenced as `debugging.py::test_b` in session scope or as `test_b`
in module scope.

A slightly different situation is given in the case of `test_o`:

.. literalinclude:: ../examples/debugging-logging.out
   :lines: 190-201,276-286

In the :func:`pytest.mark.dependency` marker for `test_h` in the
example, the name is overridden as `h`.  The outcome of that test is
registered using that name.  It can thus not be found by the name
`test_h`.

Considering the case of `test_r`:

.. literalinclude:: ../examples/debugging-logging.out
   :lines: 300-310

That test has no dependencies.  The error in the example is that the
:func:`pytest.mark.dependency` marker is applied twice to the test.
That doesn't work in pytest, only the last invocation is effective.
As a result, the second invocation setting a name, effectively clears
the dependency list that was set in the first invocation.

.. __: https://docs.pytest.org/en/stable/logging.html#live-logs
