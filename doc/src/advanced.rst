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
