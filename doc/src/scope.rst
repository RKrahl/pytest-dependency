Defining the scope of dependencies
==================================

In the previous examples, we didn't specify a scope for the
dependencies.  All dependencies were taken in module scope, which is
the default.  As a consequence, tests were constraint to depend only
from other tests in the same test module.

The :func:`pytest.mark.dependency` marker as well as the
:func:`pytest_dependency.depends` function take an optional `scope`
argument.  Possible values are `'session'`, `'package'`, `'module'`,
or `'class'`.

.. versionadded:: 0.5.0
    the scope of dependencies has been introduced.  In earlier
    versions, all dependencies were implicitly in module scope.


Explicitely specifying the scope
--------------------------------

The default value for the `scope` argument is `'module'`.  Thus, the
very first example from Section :ref:`usage-basic` could also be
written as:

.. literalinclude:: ../examples/scope_module.py

It works exactly the same.  The only difference is that the default
scope has been made explicit.

Dependencies in session scope
-----------------------------

If a test depends on another test in a different test module, the
dependency must either be in session or package scope.  Consider the
following two test modules:

.. literalinclude:: ../examples/scope_session_mod_01.py

and

.. literalinclude:: ../examples/scope_session_mod_02.py

Let's assume the modules to be stored as `tests/test_mod_01.py` and
`tests/test_mod_02.py` relative to the current working directory
respectively.  The test `test_e` in `tests/test_mod_02.py` will be run
and succeed.  It depends on `test_a` and `test_c` in
`tests/test_mod_01.py` that both succeed.  It does not matter that
there is another `test_a` in `tests/test_mod_02.py` that fails.  Test
`test_f` in `tests/test_mod_02.py` will be skipped, because it depends
on `test_b` in `tests/test_mod_01.py` that fails.  Test `test_g` in
turn will be run and succeed.  It depends on the test method `test_b`
of class `TestClass` in `tests/test_mod_01.py`, not on the test
function of the same name.

The `scope` argument only affects the references in the `depends`
argument of the marker.  It does not matter which scope is set for the
dependencies: the dependency of `test_e` in `tests/test_mod_02.py` on
`test_a` in `tests/test_mod_01.py` is in session scope.  It is not
needed to set the scope also for `test_a`.

Note that the references in session scope must use the full node id of
the dependencies.  This node id is composed of the module path, the
name of the test class if applicable, and the name of the test,
separated by a double colon "::", see Section :ref:`names` for
details.  References in module scope on the other hand must omit the
module path in the node id, because that is implied by the scope.

Package scope is only available if the test is in a package and then
restricts the dependencies to tests within the same package.
Otherwise it works the same as session scope.

The class scope
---------------

Test dependencies may also be in class scope.  This is only available
for methods of a test class and restricts the dependencies to other
test methods of the same class.

Consider the following example:

.. literalinclude:: ../examples/scope_class.py

The test method `test_c` of class `TestClass2` will be skipped because
it depends on `test_a`.  The marker does not have a `scope` argument,
so this dependency defaults to module scope.  The dependency thus
resolves to the function `test_a` at module level, which failed.  The
fact that there is also a method `test_a` in this class does not
matter, because that would need to be referenced as
`TestClass2::test_a` in module scope.  The test method `test_d` of
class `TestClass2` depends on `test_a` in class scope.  This resolves
to the method `test_a` of `TestClass2` which succeeds.  As a result,
`test_d` will be run and succeed as well.  Test method `test_e` of
class `TestClass2` will be skipped, because it depends on `test_b` in
class scope, but there is no method by that name in this class.  The
fact that there is another class `TestClass1` having a method by that
name is irrelevant.
