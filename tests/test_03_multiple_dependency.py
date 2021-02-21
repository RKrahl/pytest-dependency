"""A complicated scenario with tests having multiple dependencies.
"""

import pytest


def test_multiple(ctestdir):
    ctestdir.makepyfile("""
        import pytest

        @pytest.mark.dependency(name="a")
        def test_a():
            pytest.skip("explicit skip")

        @pytest.mark.dependency(name="b")
        def test_b():
            assert False

        @pytest.mark.dependency(name="c")
        def test_c():
            pass

        @pytest.mark.dependency(name="d")
        def test_d():
            pass

        @pytest.mark.dependency(name="e")
        def test_e():
            pass

        @pytest.mark.dependency(name="f", depends=["a", "c"])
        def test_f():
            pass

        @pytest.mark.dependency(name="g", depends=["b", "d"])
        def test_g():
            pass

        @pytest.mark.dependency(name="h", depends=["c", "e"])
        def test_h():
            pass

        @pytest.mark.dependency(name="i", depends=["f", "h"])
        def test_i():
            pass

        @pytest.mark.dependency(name="j", depends=["d", "h"])
        def test_j():
            pass

        @pytest.mark.dependency(name="k", depends=["g", "i", "j"])
        def test_k():
            pass
    """)
    result = ctestdir.runpytest("--verbose")
    result.assert_outcomes(passed=5, skipped=5, failed=1)
    result.stdout.re_match_lines(r"""
        .*::test_a SKIPPED(?:\s+\(.*\))?
        .*::test_b FAILED
        .*::test_c PASSED
        .*::test_d PASSED
        .*::test_e PASSED
        .*::test_f SKIPPED(?:\s+\(.*\))?
        .*::test_g SKIPPED(?:\s+\(.*\))?
        .*::test_h PASSED
        .*::test_i SKIPPED(?:\s+\(.*\))?
        .*::test_j PASSED
        .*::test_k SKIPPED(?:\s+\(.*\))?
    """)
