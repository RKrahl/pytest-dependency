"""A scenario featuring parametrized tests.
"""

import pytest


def test_multiple(ctestdir):
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
    result = ctestdir.runpytest("--verbose")
    result.assert_outcomes(passed=7, skipped=5, failed=1)
    result.stdout.re_match_lines(r"""
        .*::test_a\[0-0\] PASSED
        .*::test_a\[0-1\] PASSED
        .*::test_a\[1-0\] PASSED
        .*::test_a\[1-1\] FAILED
        .*::test_b\[1-2\] PASSED
        .*::test_b\[1-3\] PASSED
        .*::test_b\[1-4\] SKIPPED(?:\s+\(.*\))?
        .*::test_b\[2-3\] PASSED
        .*::test_b\[2-4\] SKIPPED(?:\s+\(.*\))?
        .*::test_b\[3-4\] SKIPPED(?:\s+\(.*\))?
        .*::test_c\[1\] SKIPPED(?:\s+\(.*\))?
        .*::test_c\[2\] SKIPPED(?:\s+\(.*\))?
        .*::test_c\[3\] PASSED
    """)
