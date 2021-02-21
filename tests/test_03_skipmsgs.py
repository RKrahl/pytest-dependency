"""Verify the messages issued when a dependent test is skipped.
"""

import pytest


def test_simple(ctestdir):
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
    result = ctestdir.runpytest("--verbose", "-rs")
    result.assert_outcomes(passed=1, skipped=2, failed=1)
    result.stdout.re_match_lines(r"""
        .*::test_a PASSED
        .*::test_b FAILED
        .*::test_c SKIPPED(?:\s+\(.*\))?
        .*::test_d SKIPPED(?:\s+\(.*\))?
    """)
    result.stdout.fnmatch_lines_random("""
        SKIP* test_c depends on test_b
        SKIP* test_d depends on test_c
    """)
