"""Using depends() to mark dependencies at runtime.
"""

import pytest


def test_skip_depend_runtime(ctestdir):
    """One test is skipped, other dependent tests are skipped as well.
    This also includes indirect dependencies.
    """
    ctestdir.makepyfile("""
        import pytest
        from pytest_dependency import depends

        @pytest.mark.dependency()
        def test_a():
            pass

        @pytest.mark.dependency()
        def test_b():
            pytest.skip("explicit skip")

        @pytest.mark.dependency()
        def test_c(request):
            depends(request, ["test_b"])
            pass

        @pytest.mark.dependency()
        def test_d(request):
            depends(request, ["test_a", "test_c"])
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
