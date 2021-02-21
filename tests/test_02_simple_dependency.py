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
    result.stdout.re_match_lines(r"""
        .*::test_a SKIPPED(?:\s+\(.*\))?
        .*::test_b PASSED
        .*::test_c PASSED
        .*::test_d PASSED
    """)


def test_skip_depend(ctestdir):
    """One test is skipped, other dependent tests are skipped as well.
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
    result.stdout.re_match_lines(r"""
        .*::test_a PASSED
        .*::test_b SKIPPED(?:\s+\(.*\))?
        .*::test_c SKIPPED(?:\s+\(.*\))?
        .*::test_d SKIPPED(?:\s+\(.*\))?
    """)


def test_fail_depend(ctestdir):
    """One test fails, other dependent tests are skipped.
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
    result.stdout.re_match_lines(r"""
        .*::test_a PASSED
        .*::test_b FAILED
        .*::test_c SKIPPED(?:\s+\(.*\))?
        .*::test_d SKIPPED(?:\s+\(.*\))?
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
    result.stdout.re_match_lines(r"""
        .*::test_a PASSED
        .*::test_b FAILED
        .*::test_c SKIPPED(?:\s+\(.*\))?
        .*::test_d SKIPPED(?:\s+\(.*\))?
    """)


def test_explicit_select(ctestdir):
    """Explicitly select only a single test that depends on another one.

    Since the other test has not been run at all, the selected test
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
    result = ctestdir.runpytest("--verbose", "test_explicit_select.py::test_d")
    result.assert_outcomes(passed=0, skipped=1, failed=0)
    result.stdout.re_match_lines(r"""
        .*::test_d SKIPPED(?:\s+\(.*\))?
    """)


def test_depend_unknown(ctestdir):
    """Depend on an unknown test that is not even defined in the test set.

    Note that is not an error to depend on an undefined test, but the
    dependent test will be skipped since the non-existent dependency
    has not been run successfully.
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

        @pytest.mark.dependency(depends=["test_x"])
        def test_d():
            pass
    """)
    result = ctestdir.runpytest("--verbose")
    result.assert_outcomes(passed=3, skipped=1, failed=0)
    result.stdout.re_match_lines(r"""
        .*::test_a PASSED
        .*::test_b PASSED
        .*::test_c PASSED
        .*::test_d SKIPPED(?:\s+\(.*\))?
    """)
