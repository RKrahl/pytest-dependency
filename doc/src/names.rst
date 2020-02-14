.. _names:

Names
=====

Dependencies of tests are referenced by name.  The default name is the
`node id`__ assigned to the test by pytest.  This default may be
overridden by an explicit `name` argument to the
:func:`pytest.mark.dependency` marker.  The references also depend on
the scope.

.. __: https://docs.pytest.org/en/latest/example/markers.html#node-id

Node ids
--------

The node ids in pytest are built of several components, separated by a
double colon "::".  For test functions, these components are the
relative path of the test module and the name of the function.  In the
case of a method of a test class the components are the module path,
the name of the class, and the name of the method.  If the function or
method is parameterized, the parameter values, separated by minus "-",
in square brackets "[]" are appended to the node id.  The
representation of the parameter values in the node id may be
overridden using the `ids` argument to the
`pytest.mark.parametrize()`__ marker.

.. __: https://docs.pytest.org/en/latest/reference.html#pytest-mark-parametrize-ref


One may check the node ids of all tests calling pytest with the
`--verbose` command line option.  As an example, consider the
following test module:

.. literalinclude:: ../examples/nodeid.py

If this module is stored as `tests/test_nodeid.py`, the output will
look like:

.. literalinclude:: ../examples/nodeid.out

.. note::
    Old versions of pytest used to include an extra "()" component to
    the node ids of methods of test classes.  This has been
    `removed in pytest 4.0.0`__.  pytest-dependency strips this
    if present.  Thus, when referencing dependencies, the new style
    node ids as described above may (and must) be used, regardless of
    the pytest version.

.. __: https://docs.pytest.org/en/latest/changelog.html#pytest-4-0-0-2018-11-13

References and scope
--------------------

When referencing dependencies of tests, the names to be used in the
`depends` argument to the :func:`pytest.mark.dependency` marker or the
`other` argument to the :func:`pytest_dependency.depends` function
depend on the scope as follows:

`session`
    The full node id must be used.
`package`
    The full node id must be used.
`module`
    The node id with the leading module path including the "::"
    separator removed must be used.
`class`
    The node id with the module path and the class name including the
    "::" separator removed must be used.

That is, in the example above, when referencing `test_a` as a
dependency, it must be referenced as `tests/test_nodeid.py::test_a` in
session scope and as `test_a` in module scope.  When referencing the
first invocation of `test_d` as a dependency, it must be referenced as
`tests/test_nodeid.py::TestClass::test_d[order]` in session scope, as
`TestClass::test_d[order]` in module scope, and as `test_d[order]` in
class scope.

If the name of the dependency has been set with an explicit `name`
argument to the :func:`pytest.mark.dependency` marker, this name must
always be used as is, regardless of the scope.

.. note::
    The module path in the node id is the path relative to the current
    working directory.  This depends on the invocation of pytest.  In
    the example above, if you change into the `tests` directory before
    invoking pytest, the module path in the node ids will be
    `test_nodeid.py`.  If you use references in session scope, you'll
    need to make sure pytest is always invoked from the same working
    directory.
