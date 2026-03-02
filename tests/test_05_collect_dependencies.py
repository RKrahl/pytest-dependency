"""Test the collect_dependencies option.
"""

import pytest


def test_no_set_collect_dependencies(ctestdir):
    """No pytest.ini file, e.g. collect_dependencies is not set.

    Explicitly select only a single test that depends on another one.
    Since collect_dependencies defaults to false, and the other test has not been run at all, the selected test
    will be skipped.

    """
    ctestdir.makepyfile("""
        import pytest

        @pytest.mark.dependency()
        def test_a():
            pass

        @pytest.mark.dependency()
        def test_b():
            pass

        @pytest.mark.dependency()
        def test_c():
            pass

        @pytest.mark.dependency(depends=["test_c"])
        def test_d():
            pass
    """)
    result = ctestdir.runpytest("--verbose", "test_no_set_collect_dependencies.py::test_d")
    result.assert_outcomes(passed=0, skipped=1, failed=0)
    result.stdout.re_match_lines(r"""
        .*::test_d SKIPPED(?:\s+\(.*\))?
    """)


def test_collect_dependencies_false(ctestdir):
    """A pytest.ini is present, collect_dependencies is set to false.

    Explicitly select only a single test that depends on another one.
    Since collect_dependencies is set to false, and the other test has not been run at all, the selected test
    will be skipped.

    """
    ctestdir.makefile('.ini', pytest="""
            [pytest]
            collect_dependencies = false
            console_output_style = classic
        """)

    ctestdir.makepyfile("""
        import pytest

        @pytest.mark.dependency()
        def test_a():
            pass

        @pytest.mark.dependency()
        def test_b():
            pass

        @pytest.mark.dependency()
        def test_c():
            pass

        @pytest.mark.dependency(depends=["test_c"])
        def test_d():
            pass
    """)
    result = ctestdir.runpytest("--verbose", "test_collect_dependencies_false.py::test_d")
    result.assert_outcomes(passed=0, skipped=1, failed=0)
    result.stdout.re_match_lines(r"""
        .*::test_d SKIPPED(?:\s+\(.*\))?
    """)


def test_collect_dependencies_true(ctestdir):
    """A pytest.ini is present, collect_dependencies is set to true.

    Explicitly select only a single test that depends on another one.
    Since collect_dependencies is set to true, the other test will be collected, and both tests will be run.
    """
    ctestdir.makefile('.ini', pytest="""
            [pytest]
            collect_dependencies = true
            console_output_style = classic
        """)

    ctestdir.makepyfile("""
        import pytest

        @pytest.mark.dependency()
        def test_a():
            pass

        @pytest.mark.dependency()
        def test_b():
            pass

        @pytest.mark.dependency()
        def test_c():
            pass

        @pytest.mark.dependency(depends=["test_c"])
        def test_d():
            pass
    """)
    result = ctestdir.runpytest("--verbose", "test_collect_dependencies_true.py::test_d")
    result.assert_outcomes(passed=2, skipped=0, failed=0)
    result.stdout.re_match_lines(r"""
            .*::test_c PASSED
            .*::test_d PASSED
        """)


def test_collect_dependencies_true_recursive(ctestdir):
    """A pytest.ini is present, collect_dependencies is set to true.

    Explicitly select only a single test that depends on another one, that depends from others two.
    Since collect_dependencies is set to true, the dependent tests will be recursively collected, and four tests will be run.
    """
    ctestdir.makefile('.ini', pytest="""
            [pytest]
            collect_dependencies = true
            console_output_style = classic
        """)

    ctestdir.makepyfile("""
        import pytest

        @pytest.mark.dependency()
        def test_a():
            pass

        @pytest.mark.dependency()
        def test_b():
            pass

        @pytest.mark.dependency(depends=["test_b", "test_a"])
        def test_c():
            pass

        @pytest.mark.dependency(depends=["test_c"])
        def test_d():
            pass
    """)
    result = ctestdir.runpytest("--verbose", "test_collect_dependencies_true_recursive.py::test_d")
    result.assert_outcomes(passed=4, skipped=0, failed=0)
    result.stdout.re_match_lines(r"""
            .*::test_a PASSED
            .*::test_b PASSED
            .*::test_c PASSED
            .*::test_d PASSED
        """)


def test_scope_session_collect_dependencies_true(ctestdir):
    """Two modules, some cross module dependencies in session scope.
    """
    ctestdir.makefile('.ini', pytest="""
            [pytest]
            collect_dependencies = true
            console_output_style = classic
        """)
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


def test_scope_session_collect_dependencies_true_single_test_run_1(ctestdir):
    """Two modules, some cross module dependencies in session scope.
    """
    ctestdir.makefile('.ini', pytest="""
            [pytest]
            collect_dependencies = true
            console_output_style = classic
        """)
    ctestdir.makepyfile(test_scope_session_01="""
        import pytest

        @pytest.mark.dependency()
        def test_a():
            pass
    """, test_scope_session_02="""
        import pytest

        @pytest.mark.dependency(
            depends=["test_scope_session_01.py::test_a"],
            scope='session'
        )
        def test_b():
            pass

    """)

    result = ctestdir.runpytest("--verbose", "test_scope_session_02.py::test_b")
    result.assert_outcomes(passed=2, skipped=0, failed=0)
    result.stdout.re_match_lines(r"""
            test_scope_session_01.py::test_a PASSED
            test_scope_session_02.py::test_b PASSED
        """)


def test_scope_session_collect_dependencies_true_single_test_run_2(ctestdir):
    """Two modules, some cross module dependencies in session scope.
    """
    ctestdir.makefile('.ini', pytest="""
            [pytest]
            collect_dependencies = true
            console_output_style = classic
        """)
    ctestdir.makepyfile(test_scope_session_01="""
        import pytest

        @pytest.mark.dependency()
        def test_a():
            pass
            
    """, test_scope_session_02="""
        import pytest

        @pytest.mark.dependency()
        def test_a():
            pass

        @pytest.mark.dependency(
            depends=["test_scope_session_01.py::test_a", "test_scope_session_02.py::test_a"],
            scope='session'
        )
        def test_b():
            pass

    """)

    result = ctestdir.runpytest("--verbose", "test_scope_session_02.py::test_b")
    result.assert_outcomes(passed=3, skipped=0, failed=0)
    result.stdout.re_match_lines(r"""
            test_scope_session_02.py::test_a PASSED
            test_scope_session_01.py::test_a PASSED
            test_scope_session_02.py::test_b PASSED
        """)


def test_scope_session_collect_dependencies_true_single_test_run_3(ctestdir):
    """Two modules, some cross module dependencies in session scope.
    """
    ctestdir.makefile('.ini', pytest="""
            [pytest]
            collect_dependencies = true
            console_output_style = classic
        """)
    ctestdir.makepyfile(test_scope_session_01="""
        import pytest

        @pytest.mark.dependency()
        def test_a():
            pass
        
        @pytest.mark.dependency(depends=["test_a"])
        def test_b():
            pass

    """, test_scope_session_02="""
        import pytest

        @pytest.mark.dependency()
        def test_a():
            pass

        @pytest.mark.dependency(
            depends=["test_scope_session_01.py::test_b", "test_scope_session_02.py::test_a"],
            scope='session'
        )
        def test_b():
            pass

    """)

    result = ctestdir.runpytest("--verbose", "test_scope_session_02.py::test_b")
    result.assert_outcomes(passed=4, skipped=0, failed=0)
    result.stdout.re_match_lines(r"""
            test_scope_session_02.py::test_a PASSED
            test_scope_session_01.py::test_a PASSED
            test_scope_session_01.py::test_b PASSED
            test_scope_session_02.py::test_b PASSED
        """)


def test_scope_session_collect_dependencies_true_single_test_run_4a(ctestdir):
    """Two modules, some cross module dependencies in session scope.
    """
    ctestdir.makefile('.ini', pytest="""
            [pytest]
            collect_dependencies = true
            console_output_style = classic
        """)
    ctestdir.makepyfile(test_scope_session_01="""
        import pytest

        @pytest.mark.dependency(depends=["test_c"])
        def test_a():
            pass

        @pytest.mark.dependency()
        def test_b():
            assert False

        @pytest.mark.dependency()
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
    result = ctestdir.runpytest("--verbose", "test_scope_session_02.py::test_e")
    result.assert_outcomes(passed=3, skipped=0, failed=0)
    result.stdout.re_match_lines(r"""
        test_scope_session_01.py::test_c PASSED
        test_scope_session_01.py::test_a PASSED
        test_scope_session_02.py::test_e PASSED
    """)


@pytest.fixture(scope="session")
def pytest_order_plugin(request):
    return pytest.importorskip("pytest_order.plugin", reason="This test requires the pytest-order package")


def test_scope_session_collect_dependencies_true_single_test_run_4b(ctestdir, pytest_order_plugin):
    """Two modules, some cross module dependencies in session scope.
    """
    ctestdir.makefile('.ini', pytest="""
            [pytest]
            collect_dependencies = true
            console_output_style = classic
        """)
    ctestdir.makepyfile(test_scope_session_01="""
        import pytest

        @pytest.mark.dependency()
        def test_a():
            pass

        @pytest.mark.dependency()
        def test_b():
            assert False

        @pytest.mark.dependency(depends=["test_scope_session_01.py::test_a"],    scope='session')
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
    result = ctestdir.runpytest("--verbose", "test_scope_session_02.py::test_e", "--order-dependencies")
    result.assert_outcomes(passed=3, skipped=0, failed=0)
    result.stdout.re_match_lines(r"""
        test_scope_session_01.py::test_a PASSED
        test_scope_session_01.py::test_c PASSED
        test_scope_session_02.py::test_e PASSED
    """)


def test_collect_dependencies_true_single_class(ctestdir):
    """A pytest.ini is present, collect_dependencies is set to true.

    One module with a single class with two tests, one of them depends on the other.
    Explicitly select only a single test that depends on another one.
    Since collect_dependencies is set to true, the other test will be collected, and both tests will be run.
    """
    ctestdir.makefile('.ini', pytest="""
            [pytest]
            collect_dependencies = true
            console_output_style = classic
        """)
    ctestdir.makepyfile(test_scope_session_01="""
        import pytest

        class Tests:
            @pytest.mark.dependency()
            def test_b(self):
                pass

            @pytest.mark.dependency(depends=["Tests::test_b"])
            def test_d(self):
                pass
    """)

    result = ctestdir.runpytest("--verbose", "test_scope_session_01.py::Tests::test_d")
    result.assert_outcomes(passed=2, skipped=0, failed=0)
    result.stdout.re_match_lines(r"""
        test_scope_session_01.py::Tests::test_b PASSED
        test_scope_session_01.py::Tests::test_d PASSED
    """)


def test_collect_dependencies_true_different_classes(ctestdir):
    """A pytest.ini is present, collect_dependencies is set to true.

       One module with two classes, each with a single test, one of them depends on the other.
       Explicitly select only a single test that depends on another one.
       Since collect_dependencies is set to true, the other test will be collected, and both tests will be run.
       """
    ctestdir.makefile('.ini', pytest="""
            [pytest]
            collect_dependencies = true
            console_output_style = classic
        """)
    ctestdir.makepyfile(test_scope_session_01="""
        import pytest

        class Tests:
            @pytest.mark.dependency()
            def test_b(self):
                pass

        class TestOtherTests:
            @pytest.mark.dependency(depends=["Tests::test_b"])
            def test_d(self):
                pass
    """)

    result = ctestdir.runpytest("--verbose", "test_scope_session_01.py::TestOtherTests::test_d")
    result.assert_outcomes(passed=2, skipped=0, failed=0)
    result.stdout.re_match_lines(r"""
        test_scope_session_01.py::Tests::test_b PASSED
        test_scope_session_01.py::TestOtherTests::test_d PASSED
    """)


def test_collect_dependencies_named(ctestdir):
    """A pytest.ini is present, collect_dependencies is set to true.

    Explicitly select only a single test that depends on another one using mark.dependency name attribute.
    Since collect_dependencies is set to true, the other test will be collected, and all tests will be run.
    """
    ctestdir.makefile('.ini', pytest="""
                [pytest]
                collect_dependencies = true
                console_output_style = classic
            """)

    ctestdir.makepyfile("""
        import pytest

        @pytest.mark.dependency(name="a")
        def test_a():
            pass

        @pytest.mark.dependency(name="b")
        def test_b():
            assert False

        @pytest.mark.dependency(name="c", depends=["b"])
        def test_c():
            pass

        @pytest.mark.dependency(name="d", depends=["c","a"])
        def test_d():
            pass
    """)
    result = ctestdir.runpytest("--verbose", "test_collect_dependencies_named.py::test_d")
    result.assert_outcomes(passed=1, skipped=2, failed=1)
    result.stdout.re_match_lines(r"""
        .*::test_a PASSED
        .*::test_b FAILED
        .*::test_c SKIPPED(?:\s+\(.*\))?
        .*::test_d SKIPPED(?:\s+\(.*\))?
    """)


def test_collect_simple_params(ctestdir, pytest_order_plugin):
    """A pytest.ini is present, collect_dependencies is set to true.

    Explicitly select only a single test that depends on another one using mark.dependency name attribute.
    Since collect_dependencies is set to true, the other test will be collected, and all tests will be run.

    Simple test for a dependency on a parametrized test.
    pytest-order is required to reorder the tests in the parametrized cases.
    """
    ctestdir.makefile('.ini', pytest="""
                    [pytest]
                    collect_dependencies = true
                    console_output_style = classic
                """)

    ctestdir.makepyfile("""
        import pytest

        _md = pytest.mark.dependency

        @pytest.mark.parametrize("x", [ 0, 1 ])
        @pytest.mark.dependency()
        def test_a(x):
            assert x == 0

        @pytest.mark.parametrize("x", [
            pytest.param(0, marks=_md(depends=["test_a[0]"])),
            pytest.param(1, marks=_md(depends=["test_a[1]"])),
        ])
        def test_b(x):
            pass
    """)
    result = ctestdir.runpytest("--verbose", "test_collect_simple_params.py::test_b", "--order-dependencies")
    result.assert_outcomes(passed=2, skipped=1, failed=1)
    # match the following output lines without take into account the order of the tests
    result.stdout.re_match_lines(r"""
        .*::test_a\[0\] PASSED
    """)
    result.stdout.re_match_lines(r"""
        .*::test_a\[1\] FAILED
    """)
    result.stdout.re_match_lines(r"""
        .*::test_b\[0\] PASSED
    """)
    result.stdout.re_match_lines(r"""
        .*::test_b\[1\] SKIPPED(?:\s+\(.*\))?
    """)


def test_collect_multiple_param(ctestdir, pytest_order_plugin):
    """A pytest.ini is present, collect_dependencies is set to true.

    Explicitly select only a single test that depends on another one using mark.dependency name attribute.
    Since collect_dependencies is set to true, the other test will be collected, and all tests will be run.

    A scenario featuring parametrized tests.
    pytest-order is required to reorder the tests in the parametrized cases.
    """
    ctestdir.makefile('.ini', pytest="""
                        [pytest]
                        collect_dependencies = true
                        console_output_style = classic
                    """)

    ctestdir.makepyfile("""
        import pytest

        _md = pytest.mark.dependency

        @pytest.mark.parametrize("x,y", [
            pytest.param(0, 0, marks=_md(name="a1")),
            pytest.param(0, 1, marks=_md(name="a2")),
            pytest.param(1, 0, marks=_md(name="a3")),
            pytest.param(1, 1, marks=_md(name="a4"))
        ])
        def test_a(x,y):
            assert x==0 or y==0

        @pytest.mark.parametrize("u,v", [
            pytest.param(1, 2, marks=_md(name="b1", depends=["a1", "a2"])),
            pytest.param(1, 3, marks=_md(name="b2", depends=["a1", "a3"])),
            pytest.param(1, 4, marks=_md(name="b3", depends=["a1", "a4"])),
            pytest.param(2, 3, marks=_md(name="b4", depends=["a2", "a3"])),
            pytest.param(2, 4, marks=_md(name="b5", depends=["a2", "a4"])),
            pytest.param(3, 4, marks=_md(name="b6", depends=["a3", "a4"]))
        ])
        def test_b(u,v):
            pass

        @pytest.mark.parametrize("w", [
            pytest.param(1, marks=_md(name="c1", depends=["b1", "b3", "b5"])),
            pytest.param(2, marks=_md(name="c2", depends=["b1", "b3", "b6"])),
            pytest.param(3, marks=_md(name="c3", depends=["b1", "b2", "b4"]))
        ])
        def test_c(w):
            pass
    """)
    result = ctestdir.runpytest("--verbose", "test_collect_multiple_param.py::test_c", "--order-dependencies")
    result.assert_outcomes(passed=7, skipped=5, failed=1)
    # match the following output lines without take into account the order of the tests
    result.stdout.re_match_lines(r"""
        .*::test_a\[0-0\] PASSED
    """)
    result.stdout.re_match_lines(r"""
        .*::test_a\[0-1\] PASSED
    """)
    result.stdout.re_match_lines(r"""
        .*::test_a\[1-0\] PASSED
    """)
    result.stdout.re_match_lines(r"""
        .*::test_a\[1-1\] FAILED
    """)
    result.stdout.re_match_lines(r"""
        .*::test_b\[1-2\] PASSED
    """)
    result.stdout.re_match_lines(r"""
        .*::test_b\[1-3\] PASSED
    """)
    result.stdout.re_match_lines(r"""
        .*::test_b\[1-4\] SKIPPED(?:\s+\(.*\))?
    """)
    result.stdout.re_match_lines(r"""
        .*::test_b\[2-3\] PASSED
    """)
    result.stdout.re_match_lines(r"""
        .*::test_b\[2-4\] SKIPPED(?:\s+\(.*\))?
    """)
    result.stdout.re_match_lines(r"""
        .*::test_b\[3-4\] SKIPPED(?:\s+\(.*\))?
    """)
    result.stdout.re_match_lines(r"""
        .*::test_c\[1\] SKIPPED(?:\s+\(.*\))?
    """)
    result.stdout.re_match_lines(r"""
        .*::test_c\[2\] SKIPPED(?:\s+\(.*\))?
    """)
    result.stdout.re_match_lines(r"""
        .*::test_c\[3\] PASSED
    """)
