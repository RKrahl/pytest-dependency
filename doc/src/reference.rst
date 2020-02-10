Reference
=========

.. py:decorator:: pytest.mark.dependency(name=None, depends=[], scope='module')

    Mark a test to be used as a dependency for other tests or to
    depend on other tests.

    This will cause the test results to be registered internally and
    thus other tests may depend on the test.  The list of dependencies
    for the test may be set in the depends argument.

    :param name: the name of the test to be used for referencing by
        dependent tests.  If not set, it defaults to the node ID
        defined by pytest.  The name must be unique.
    :type name: :class:`str`
    :param depends: dependencies, a list of names of tests that this
        test depends on.  The test will be skipped unless all of the
        dependencies have been run successfully.  The dependencies
        must also have been decorated by the marker.  The names of the
        dependencies must be adapted to the scope.
    :type depends: iterable of :class:`str`
    :param scope: the scope to search for the dependencies.  Must be
        either `'session'`, `'package'`, `'module'`, or `'class'`.
    :type scope: :class:`str`

    See Section :ref:`names` for details on the default name if the
    `name` argument is not set and on how references in the `depends`
    argument must be adapted to the scope.

    .. versionchanged:: 0.5.0
        the scope parameter has been added.

.. py:module:: pytest_dependency

.. autofunction:: pytest_dependency.depends
