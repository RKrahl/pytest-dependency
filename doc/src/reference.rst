Reference
=========

.. py:decorator:: pytest.mark.dependency(name=None, depends=[])

    Mark a test to be used as a dependency for other tests or to
    depend on other tests.

    This will cause the test results to be registered internally and
    thus other tests may depend on the test.  The list of dependencies
    for the test may be set in the depends argument.

    :param name: the name of the test to be used for referencing by
	dependent tests.  If not set, it defaults to the internal name
	used in pytest, that is the name of the test function,
	extended by the parameters if applicable.
    :type name: :class:`str`
    :param depends: dependencies, a list of names of tests that this
        test depends on.  The test will be skipped unless all of the
	dependencies have been run successfully.  The dependencies
	must also have been decorated by the marker.
    :type depends: iterable of :class:`str`

.. py:module:: pytest_dependency

.. autofunction:: pytest_dependency.depends
