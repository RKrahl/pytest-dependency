"""Usage with test classes.
"""

import pytest


def test_class_simple(ctestdir):
    """Simple dependencies of test methods in a class.
    test_a() deliberately fails, some other methods depend on it, some don't.
    """
    ctestdir.makepyfile("""
        import pytest

        class TestClass(object):

            @pytest.mark.dependency()
            def test_a(self):
                assert False

            @pytest.mark.dependency()
            def test_b(self):
                pass

            @pytest.mark.dependency(depends=["TestClass::test_a"])
            def test_c(self):
                pass

            @pytest.mark.dependency(depends=["TestClass::test_b"])
            def test_d(self):
                pass

            @pytest.mark.dependency(depends=["TestClass::test_b", 
                                             "TestClass::test_c"])
            def test_e(self):
                pass
    """)
    result = ctestdir.runpytest("--verbose")
    result.assert_outcomes(passed=2, skipped=2, failed=1)
    result.stdout.re_match_lines(r"""
        .*::TestClass::test_a FAILED
        .*::TestClass::test_b PASSED
        .*::TestClass::test_c SKIPPED(?:\s+\(.*\))?
        .*::TestClass::test_d PASSED
        .*::TestClass::test_e SKIPPED(?:\s+\(.*\))?
    """)


def test_class_simple_named(ctestdir):
    """Mostly the same as test_class_simple(), but name the test methods
    now explicitly.
    """
    ctestdir.makepyfile("""
        import pytest

        class TestClassNamed(object):

            @pytest.mark.dependency(name="a")
            def test_a(self):
                assert False

            @pytest.mark.dependency(name="b")
            def test_b(self):
                pass

            @pytest.mark.dependency(name="c", depends=["a"])
            def test_c(self):
                pass

            @pytest.mark.dependency(name="d", depends=["b"])
            def test_d(self):
                pass

            @pytest.mark.dependency(name="e", depends=["b", "c"])
            def test_e(self):
                pass
    """)
    result = ctestdir.runpytest("--verbose")
    result.assert_outcomes(passed=2, skipped=2, failed=1)
    result.stdout.re_match_lines(r"""
        .*::TestClassNamed::test_a FAILED
        .*::TestClassNamed::test_b PASSED
        .*::TestClassNamed::test_c SKIPPED(?:\s+\(.*\))?
        .*::TestClassNamed::test_d PASSED
        .*::TestClassNamed::test_e SKIPPED(?:\s+\(.*\))?
    """)


def test_class_default_name(ctestdir):
    """Issue #6: for methods of test classes, the default name used to be
    the method name.  This could have caused conflicts if there is a
    function having the same name outside the class.  In the following
    example, before fixing this issue, the method test_a() of class
    TestClass would have shadowed the failure of function test_a().

    Now the class name is prepended to the default test name, removing
    this conflict.
    """
    ctestdir.makepyfile("""
        import pytest

        @pytest.mark.dependency()
        def test_a():
            assert False

        class TestClass(object):

            @pytest.mark.dependency()
            def test_a(self):
                pass

        @pytest.mark.dependency(depends=["test_a"])
        def test_b():
            pass
    """)
    result = ctestdir.runpytest("--verbose")
    result.assert_outcomes(passed=1, skipped=1, failed=1)
    result.stdout.re_match_lines(r"""
        .*::test_a FAILED
        .*::TestClass::test_a PASSED
        .*::test_b SKIPPED(?:\s+\(.*\))?
    """)


def test_nested_class_scope_names(ctestdir):
    """Class-scoped names are relative to the innermost collected class."""
    ctestdir.makepyfile("""
        import pytest
        from pytest_dependency import depends

        class TestOuter:
            class TestFirst:
                @pytest.mark.dependency()
                def test_a(self):
                    pass

                @pytest.mark.dependency(depends=["test_a"], scope="class")
                def test_b(self, request):
                    depends(request, ["test_a"], scope="class")

            class TestSecond:
                @pytest.mark.dependency()
                def test_a(self):
                    assert False

                @pytest.mark.dependency(depends=["test_a"], scope="class")
                def test_b(self):
                    pass

        @pytest.mark.dependency(depends=["TestOuter::TestFirst::test_a"])
        def test_module_reference():
            pass
    """)
    result = ctestdir.runpytest("--verbose")
    result.assert_outcomes(passed=3, failed=1, skipped=1)


def test_nested_class_parametrized_scope_names(ctestdir):
    """Parameter IDs containing double colons remain part of method names."""
    ctestdir.makepyfile("""
        import pytest

        class TestOuter:
            class TestInner:
                @pytest.mark.dependency()
                @pytest.mark.parametrize("value", [1], ids=["part::value"])
                def test_a(self, value):
                    pass

                @pytest.mark.dependency(
                    depends=["test_a[part::value]"], scope="class")
                def test_b(self):
                    pass
    """)
    result = ctestdir.runpytest()
    result.assert_outcomes(passed=2)
