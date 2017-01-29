"""Simple dependencies between tests.
"""

import pytest


def test_no_skip(ctestdir):
    """One test is skipped, but no other test depends on it,
    so all other tests pass.
    """
    ctestdir.makepyfile("""
        import pytest

        @pytest.mark.dependency()
        def test_a():
            pytest.skip("explicit skip")

        @pytest.mark.dependency()
        def test_b():
            pass

        @pytest.mark.dependency(depends=["test_b"])
        def test_c():
            pass

        @pytest.mark.dependency(depends=["test_c"])
        def test_d():
            pass
    """)
    result = ctestdir.runpytest("--verbose")
    result.assert_outcomes(passed=3, skipped=1, failed=0)
    result.stdout.fnmatch_lines("""
        *::test_a SKIPPED
        *::test_b PASSED
        *::test_c PASSED
        *::test_d PASSED
    """)

def test_skip_depend(ctestdir):
    """One test is skipped, other depending tests are skipped as well.
    This also includes indirect dependencies.
    """
    ctestdir.makepyfile("""
        import pytest

        @pytest.mark.dependency()
        def test_a():
            pass

        @pytest.mark.dependency()
        def test_b():
            pytest.skip("explicit skip")

        @pytest.mark.dependency(depends=["test_b"])
        def test_c():
            pass

        @pytest.mark.dependency(depends=["test_c"])
        def test_d():
            pass
    """)
    result = ctestdir.runpytest("--verbose")
    result.assert_outcomes(passed=1, skipped=3, failed=0)
    result.stdout.fnmatch_lines("""
        *::test_a PASSED
        *::test_b SKIPPED
        *::test_c SKIPPED
        *::test_d SKIPPED
    """)


def test_fail_depend(ctestdir):
    """One test fails, other depending tests are skipped.
    This also includes indirect dependencies.
    """
    ctestdir.makepyfile("""
        import pytest

        @pytest.mark.dependency()
        def test_a():
            pass

        @pytest.mark.dependency()
        def test_b():
            assert False

        @pytest.mark.dependency(depends=["test_b"])
        def test_c():
            pass

        @pytest.mark.dependency(depends=["test_c"])
        def test_d():
            pass
    """)
    result = ctestdir.runpytest("--verbose")
    result.assert_outcomes(passed=1, skipped=2, failed=1)
    result.stdout.fnmatch_lines("""
        *::test_a PASSED
        *::test_b FAILED
        *::test_c SKIPPED
        *::test_d SKIPPED
    """)


def test_named_fail_depend(ctestdir):
    """Same as test_fail_depend, but using custom test names.
    """
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

        @pytest.mark.dependency(name="d", depends=["c"])
        def test_d():
            pass
    """)
    result = ctestdir.runpytest("--verbose")
    result.assert_outcomes(passed=1, skipped=2, failed=1)
    result.stdout.fnmatch_lines("""
        *::test_a PASSED
        *::test_b FAILED
        *::test_c SKIPPED
        *::test_d SKIPPED
    """)
