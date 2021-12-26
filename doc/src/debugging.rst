Debugging guide
===============

This section is supposed to provide hints on what to check if
pytest-dependency does not seem to behave as expected.

Example
-------

Throughout this debugging guide, we will consider the following
example:

.. literalinclude:: ../examples/debugging.py

Diagnostic tools
----------------

pytest summary
..............

You can request a short summary from pytest including information on
skipped tests using the ``-rs`` `command line option`__:

.. literalinclude:: ../examples/debugging-summary.out

.. __: https://docs.pytest.org/en/stable/usage.html#detailed-summary-report

Verbose pytest output
.....................

A list of all tests with their respective outcome will be displayed if
you call pytest with the ``--verbose`` command line option:

.. literalinclude:: ../examples/debugging-verbose.out

Logging
.......

pytest-dependency emits log messages when registering test results and
when checking dependencies for a test.  You can request these log
messages to be displayed at runtime using `log command line options`__
in the pytest call:

.. literalinclude:: ../examples/debugging-logging.out

.. __: https://docs.pytest.org/en/stable/logging.html#live-logs
