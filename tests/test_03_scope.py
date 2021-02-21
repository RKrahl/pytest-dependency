"""Specifying the scope of dependencies.
"""

import pytest


def test_scope_module(ctestdir):
    """One single module, module scope is explicitely set in the
    pytest.mark.dependency() marker.
    """
    ctestdir.makepyfile("""
        import pytest

        @pytest.mark.dependency()
        def test_a():
            assert False

        @pytest.mark.dependency()
        def test_b():
            pass

        @pytest.mark.dependency(depends=["test_a"], scope='module')
        def test_c():
            pass

        @pytest.mark.dependency(depends=["test_b"], scope='module')
        def test_d():
            pass

        @pytest.mark.dependency(depends=["test_b", "test_c"], scope='module')
        def test_e():
            pass
    """)
    result = ctestdir.runpytest("--verbose")
    result.assert_outcomes(passed=2, skipped=2, failed=1)
    result.stdout.re_match_lines(r"""
        test_scope_module.py::test_a FAILED
        test_scope_module.py::test_b PASSED
        test_scope_module.py::test_c SKIPPED(?:\s+\(.*\))?
        test_scope_module.py::test_d PASSED
        test_scope_module.py::test_e SKIPPED(?:\s+\(.*\))?
    """)

def test_scope_session(ctestdir):
    """Two modules, some cross module dependencies in session scope.
    """
    ctestdir.makepyfile(test_scope_session_01="""
        import pytest

        @pytest.mark.dependency()
        def test_a():
            pass

        @pytest.mark.dependency()
        def test_b():
            assert False

        @pytest.mark.dependency(depends=["test_a"])
        def test_c():
            pass

        class TestClass(object):

            @pytest.mark.dependency()
            def test_b(self):
                pass
    """, test_scope_session_02="""
        import pytest

        @pytest.mark.dependency()
        def test_a():
            assert False

        @pytest.mark.dependency(
            depends=["test_scope_session_01.py::test_a",
                     "test_scope_session_01.py::test_c"],
            scope='session'
        )
        def test_e():
            pass

        @pytest.mark.dependency(
            depends=["test_scope_session_01.py::test_b"],
            scope='session'
        )
        def test_f():
            pass

        @pytest.mark.dependency(
            depends=["test_scope_session_02.py::test_e"],
            scope='session'
        )
        def test_g():
            pass

        @pytest.mark.dependency(
            depends=["test_scope_session_01.py::TestClass::test_b"],
            scope='session'
        )
        def test_h():
            pass
    """)
    result = ctestdir.runpytest("--verbose")
    result.assert_outcomes(passed=6, skipped=1, failed=2)
    result.stdout.re_match_lines(r"""
        test_scope_session_01.py::test_a PASSED
        test_scope_session_01.py::test_b FAILED
        test_scope_session_01.py::test_c PASSED
        test_scope_session_01.py::TestClass::test_b PASSED
        test_scope_session_02.py::test_a FAILED
        test_scope_session_02.py::test_e PASSED
        test_scope_session_02.py::test_f SKIPPED(?:\s+\(.*\))?
        test_scope_session_02.py::test_g PASSED
        test_scope_session_02.py::test_h PASSED
    """)

def test_scope_package(ctestdir):
    """Two packages, some cross module dependencies within the package and
    across package boundaries.
    """
    ctestdir.mkpydir("test_scope_package_a")
    ctestdir.mkpydir("test_scope_package_b")
    srcs = {
        'test_scope_package_a/test_01': """
            import pytest

            @pytest.mark.dependency()
            def test_a():
                pass
        """,
        'test_scope_package_b/test_02': """
            import pytest

            @pytest.mark.dependency()
            def test_c():
                pass

            @pytest.mark.dependency()
            def test_d():
                assert False
        """,
        'test_scope_package_b/test_03': """
            import pytest

            @pytest.mark.dependency(
                depends=["test_scope_package_a/test_01.py::test_a"],
                scope='session'
            )
            def test_e():
                pass

            @pytest.mark.dependency(
                depends=["test_scope_package_a/test_01.py::test_a"],
                scope='package'
            )
            def test_f():
                pass

            @pytest.mark.dependency(
                depends=["test_scope_package_b/test_02.py::test_c"],
                scope='package'
            )
            def test_g():
                pass

            @pytest.mark.dependency(
                depends=["test_scope_package_b/test_02.py::test_d"],
                scope='package'
            )
            def test_h():
                pass
        """,
    }
    ctestdir.makepyfile(**srcs)
    result = ctestdir.runpytest("--verbose")
    result.assert_outcomes(passed=4, skipped=2, failed=1)
    result.stdout.re_match_lines(r"""
        test_scope_package_a/test_01.py::test_a PASSED
        test_scope_package_b/test_02.py::test_c PASSED
        test_scope_package_b/test_02.py::test_d FAILED
        test_scope_package_b/test_03.py::test_e PASSED
        test_scope_package_b/test_03.py::test_f SKIPPED(?:\s+\(.*\))?
        test_scope_package_b/test_03.py::test_g PASSED
        test_scope_package_b/test_03.py::test_h SKIPPED(?:\s+\(.*\))?
    """)

def test_scope_class(ctestdir):
    """Dependencies in class scope.
    """
    ctestdir.makepyfile("""
        import pytest

        @pytest.mark.dependency()
        def test_a():
            assert False

        @pytest.mark.dependency()
        def test_b():
            pass

        class TestClass1(object):

            @pytest.mark.dependency()
            def test_c(self):
                pass

        class TestClass2(object):

            @pytest.mark.dependency()
            def test_a(self):
                pass

            @pytest.mark.dependency()
            def test_b(self):
                assert False

            @pytest.mark.dependency(depends=["test_a"])
            def test_d(self):
                pass

            @pytest.mark.dependency(depends=["test_b"])
            def test_e(self):
                pass

            @pytest.mark.dependency(depends=["test_a"], scope='class')
            def test_f(self):
                pass

            @pytest.mark.dependency(depends=["test_b"], scope='class')
            def test_g(self):
                pass

            @pytest.mark.dependency(depends=["test_c"], scope='class')
            def test_h(self):
                pass
    """)
    result = ctestdir.runpytest("--verbose")
    result.assert_outcomes(passed=5, skipped=3, failed=2)
    result.stdout.re_match_lines(r"""
        test_scope_class.py::test_a FAILED
        test_scope_class.py::test_b PASSED
        test_scope_class.py::TestClass1::test_c PASSED
        test_scope_class.py::TestClass2::test_a PASSED
        test_scope_class.py::TestClass2::test_b FAILED
        test_scope_class.py::TestClass2::test_d SKIPPED(?:\s+\(.*\))?
        test_scope_class.py::TestClass2::test_e PASSED
        test_scope_class.py::TestClass2::test_f PASSED
        test_scope_class.py::TestClass2::test_g SKIPPED(?:\s+\(.*\))?
        test_scope_class.py::TestClass2::test_h SKIPPED(?:\s+\(.*\))?
    """)

def test_scope_nodeid(ctestdir):
    """The default name of a test is the node id.
    The references to the default names must be adapted according to
    the scope.
    """
    ctestdir.makepyfile("""
        import pytest

        @pytest.mark.dependency()
        def test_a():
            pass

        @pytest.mark.dependency(
            depends=["test_a"],
            scope='module'
        )
        def test_b():
            pass

        @pytest.mark.dependency(
            depends=["test_scope_nodeid.py::test_a"],
            scope='module'
        )
        def test_c():
            pass

        @pytest.mark.dependency(
            depends=["test_a"],
            scope='session'
        )
        def test_d():
            pass

        @pytest.mark.dependency(
            depends=["test_scope_nodeid.py::test_a"],
            scope='session'
        )
        def test_e():
            pass

        class TestClass(object):

            @pytest.mark.dependency()
            def test_f(self):
                pass

            @pytest.mark.dependency(
                depends=["test_f"],
                scope='class'
            )
            def test_g(self):
                pass

            @pytest.mark.dependency(
                depends=["TestClass::test_f"],
                scope='class'
            )
            def test_h(self):
                pass

            @pytest.mark.dependency(
                depends=["test_scope_nodeid.py::TestClass::test_f"],
                scope='class'
            )
            def test_i(self):
                pass

            @pytest.mark.dependency(
                depends=["test_f"],
                scope='module'
            )
            def test_j(self):
                pass

            @pytest.mark.dependency(
                depends=["TestClass::test_f"],
                scope='module'
            )
            def test_k(self):
                pass

            @pytest.mark.dependency(
                depends=["test_scope_nodeid.py::TestClass::test_f"],
                scope='module'
            )
            def test_l(self):
                pass

            @pytest.mark.dependency(
                depends=["test_f"],
                scope='session'
            )
            def test_m(self):
                pass

            @pytest.mark.dependency(
                depends=["TestClass::test_f"],
                scope='session'
            )
            def test_n(self):
                pass

            @pytest.mark.dependency(
                depends=["test_scope_nodeid.py::TestClass::test_f"],
                scope='session'
            )
            def test_o(self):
                pass
    """)
    result = ctestdir.runpytest("--verbose")
    result.assert_outcomes(passed=7, skipped=8, failed=0)
    result.stdout.re_match_lines(r"""
        test_scope_nodeid.py::test_a PASSED
        test_scope_nodeid.py::test_b PASSED
        test_scope_nodeid.py::test_c SKIPPED(?:\s+\(.*\))?
        test_scope_nodeid.py::test_d SKIPPED(?:\s+\(.*\))?
        test_scope_nodeid.py::test_e PASSED
        test_scope_nodeid.py::TestClass::test_f PASSED
        test_scope_nodeid.py::TestClass::test_g PASSED
        test_scope_nodeid.py::TestClass::test_h SKIPPED(?:\s+\(.*\))?
        test_scope_nodeid.py::TestClass::test_i SKIPPED(?:\s+\(.*\))?
        test_scope_nodeid.py::TestClass::test_j SKIPPED(?:\s+\(.*\))?
        test_scope_nodeid.py::TestClass::test_k PASSED
        test_scope_nodeid.py::TestClass::test_l SKIPPED(?:\s+\(.*\))?
        test_scope_nodeid.py::TestClass::test_m SKIPPED(?:\s+\(.*\))?
        test_scope_nodeid.py::TestClass::test_n SKIPPED(?:\s+\(.*\))?
        test_scope_nodeid.py::TestClass::test_o PASSED
    """)

def test_scope_named(ctestdir):
    """Explicitely named tests are always referenced by that name,
    regardless of the scope.
    """
    ctestdir.makepyfile("""
        import pytest

        @pytest.mark.dependency(name="a")
        def test_a():
            pass

        @pytest.mark.dependency(
            depends=["a"],
            scope='module'
        )
        def test_b():
            pass

        @pytest.mark.dependency(
            depends=["test_a"],
            scope='module'
        )
        def test_c():
            pass

        @pytest.mark.dependency(
            depends=["a"],
            scope='session'
        )
        def test_d():
            pass

        @pytest.mark.dependency(
            depends=["test_scope_named.py::test_a"],
            scope='session'
        )
        def test_e():
            pass

        class TestClass(object):

            @pytest.mark.dependency(name="f")
            def test_f(self):
                pass

            @pytest.mark.dependency(
                depends=["f"],
                scope='class'
            )
            def test_g(self):
                pass

            @pytest.mark.dependency(
                depends=["test_f"],
                scope='class'
            )
            def test_h(self):
                pass

            @pytest.mark.dependency(
                depends=["f"],
                scope='module'
            )
            def test_i(self):
                pass

            @pytest.mark.dependency(
                depends=["TestClass::test_f"],
                scope='module'
            )
            def test_j(self):
                pass

            @pytest.mark.dependency(
                depends=["f"],
                scope='session'
            )
            def test_k(self):
                pass

            @pytest.mark.dependency(
                depends=["test_scope_named.py::TestClass::test_f"],
                scope='session'
            )
            def test_l(self):
                pass
    """)
    result = ctestdir.runpytest("--verbose")
    result.assert_outcomes(passed=7, skipped=5, failed=0)
    result.stdout.re_match_lines(r"""
        test_scope_named.py::test_a PASSED
        test_scope_named.py::test_b PASSED
        test_scope_named.py::test_c SKIPPED(?:\s+\(.*\))?
        test_scope_named.py::test_d PASSED
        test_scope_named.py::test_e SKIPPED(?:\s+\(.*\))?
        test_scope_named.py::TestClass::test_f PASSED
        test_scope_named.py::TestClass::test_g PASSED
        test_scope_named.py::TestClass::test_h SKIPPED(?:\s+\(.*\))?
        test_scope_named.py::TestClass::test_i PASSED
        test_scope_named.py::TestClass::test_j SKIPPED(?:\s+\(.*\))?
        test_scope_named.py::TestClass::test_k PASSED
        test_scope_named.py::TestClass::test_l SKIPPED(?:\s+\(.*\))?
    """)

def test_scope_dependsfunc(ctestdir):
    """Test the scope argument to the depends() function.
    """
    ctestdir.makepyfile(test_scope_dependsfunc_01="""
        import pytest

        @pytest.mark.dependency()
        def test_a():
            pass

        @pytest.mark.dependency()
        def test_b():
            assert False

        @pytest.mark.dependency(depends=["test_a"])
        def test_c():
            pass

        class TestClass(object):

            @pytest.mark.dependency()
            def test_b(self):
                pass
    """, test_scope_dependsfunc_02="""
        import pytest
        from pytest_dependency import depends

        @pytest.mark.dependency()
        def test_a():
            assert False

        @pytest.mark.dependency()
        def test_b():
            pass

        @pytest.mark.dependency()
        def test_e(request):
            depends(request,
                    ["test_scope_dependsfunc_01.py::test_a",
                     "test_scope_dependsfunc_01.py::test_c"],
                    scope='session')
            pass

        @pytest.mark.dependency()
        def test_f(request):
            depends(request,
                    ["test_scope_dependsfunc_01.py::test_b"],
                    scope='session')
            pass

        @pytest.mark.dependency()
        def test_g(request):
            depends(request,
                    ["test_scope_dependsfunc_02.py::test_e"],
                    scope='session')
            pass

        @pytest.mark.dependency()
        def test_h(request):
            depends(request,
                    ["test_scope_dependsfunc_01.py::TestClass::test_b"],
                    scope='session')
            pass

        @pytest.mark.dependency()
        def test_i(request):
            depends(request, ["test_a"], scope='module')
            pass

        @pytest.mark.dependency()
        def test_j(request):
            depends(request, ["test_b"], scope='module')
            pass

        class TestClass(object):

            @pytest.mark.dependency()
            def test_a(self):
                pass

            @pytest.mark.dependency()
            def test_b(self):
                assert False

            @pytest.mark.dependency()
            def test_c(self, request):
                depends(request, ["test_a"], scope='class')
                pass

            @pytest.mark.dependency()
            def test_d(self, request):
                depends(request, ["test_b"], scope='class')
                pass
    """)
    result = ctestdir.runpytest("--verbose")
    result.assert_outcomes(passed=10, skipped=3, failed=3)
    result.stdout.re_match_lines(r"""
        test_scope_dependsfunc_01.py::test_a PASSED
        test_scope_dependsfunc_01.py::test_b FAILED
        test_scope_dependsfunc_01.py::test_c PASSED
        test_scope_dependsfunc_01.py::TestClass::test_b PASSED
        test_scope_dependsfunc_02.py::test_a FAILED
        test_scope_dependsfunc_02.py::test_b PASSED
        test_scope_dependsfunc_02.py::test_e PASSED
        test_scope_dependsfunc_02.py::test_f SKIPPED(?:\s+\(.*\))?
        test_scope_dependsfunc_02.py::test_g PASSED
        test_scope_dependsfunc_02.py::test_h PASSED
        test_scope_dependsfunc_02.py::test_i SKIPPED(?:\s+\(.*\))?
        test_scope_dependsfunc_02.py::test_j PASSED
        test_scope_dependsfunc_02.py::TestClass::test_a PASSED
        test_scope_dependsfunc_02.py::TestClass::test_b FAILED
        test_scope_dependsfunc_02.py::TestClass::test_c PASSED
        test_scope_dependsfunc_02.py::TestClass::test_d SKIPPED(?:\s+\(.*\))?
    """)
