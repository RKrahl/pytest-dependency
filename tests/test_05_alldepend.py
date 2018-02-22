"""Test the "all" dependency.
"""

import pytest


def test_all(ctestdir):
    """ Show that depends="all" causes the test to be skipped if a
    previous test has failed """
    ctestdir.makepyfile("""
        import pytest

        @pytest.mark.dependency()
        def test_a():
            pass

        @pytest.mark.dependency(depends="all")
        def test_b():
            pass

        @pytest.mark.dependency()
        def test_c():
            assert False

        @pytest.mark.dependency(depends="all")
        def test_d():
            pass

        class TestClass(object):

            @pytest.mark.dependency()
            def test_a(self):
                pass

            @pytest.mark.dependency(depends="all")
            def test_b(self):
                pass
    """)
    result = ctestdir.runpytest("--verbose", "test_all.py")
    result.assert_outcomes(passed=3, skipped=2, failed=1)
    result.stdout.fnmatch_lines("""
        *::test_b PASSED
        *::test_c FAILED
        *::test_d SKIPPED
        *::TestClass::test_b SKIPPED
    """)
