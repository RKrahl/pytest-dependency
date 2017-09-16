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

            @pytest.mark.dependency(depends=["test_a"])
            def test_c(self):
                pass

            @pytest.mark.dependency(depends=["test_b"])
            def test_d(self):
                pass

            @pytest.mark.dependency(depends=["test_b", "test_c"])
            def test_e(self):
                pass
    """)
    result = ctestdir.runpytest("--verbose")
    result.assert_outcomes(passed=2, skipped=2, failed=1)
    result.stdout.fnmatch_lines("""
        *::TestClass::test_a FAILED
        *::TestClass::test_b PASSED
        *::TestClass::test_c SKIPPED
        *::TestClass::test_d PASSED
        *::TestClass::test_e SKIPPED
    """)


def test_class_simple_named(ctestdir):
    """Mostly the same as test_class_simple(), but name the test methods
    now explicitely.
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
    result.stdout.fnmatch_lines("""
        *::TestClassNamed::test_a FAILED
        *::TestClassNamed::test_b PASSED
        *::TestClassNamed::test_c SKIPPED
        *::TestClassNamed::test_d PASSED
        *::TestClassNamed::test_e SKIPPED
    """)


@pytest.mark.xfail(reason="Issue #6")
def test_class_default_name(ctestdir):
    """For methods of test classes, the default name is the method name.
    This may cause conflicts if there is a function having the same
    name outside the class.  Note how the method test_a() of class
    TestClass shadows the failure of function test_a().
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
    result.stdout.fnmatch_lines("""
        *::test_a FAILED
        *::TestClass::test_a PASSED
        *::test_b SKIPPED
    """)
