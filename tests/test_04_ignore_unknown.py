"""Test the ignore-unknown-dependency command line option.
"""

import pytest


def test_no_ignore(ctestdir):
    """No command line option, e.g. ignore-unknown-dependency is not set.

    Explicitly select only a single test that depends on another one.
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
    result = ctestdir.runpytest("--verbose", "test_no_ignore.py::test_d")
    result.assert_outcomes(passed=0, skipped=1, failed=0)
    result.stdout.re_match_lines(r"""
        .*::test_d SKIPPED(?:\s+\(.*\))?
    """)


def test_ignore(ctestdir):
    """Set the ignore-unknown-dependency command line option.

    Explicitly select only a single test that depends on another one.
    The other test has not been run at all, but since unknown
    dependencies will be ignored, the selected test will be run
    nevertheless.
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
    result = ctestdir.runpytest("--verbose", "--ignore-unknown-dependency", 
                                "test_ignore.py::test_d")
    result.assert_outcomes(passed=1, skipped=0, failed=0)
    result.stdout.re_match_lines(r"""
        .*::test_d PASSED
    """)
