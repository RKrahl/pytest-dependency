"""Test the automark_dependency option.
"""

import pytest


def test_not_set(ctestdir):
    """No pytest.ini file, e.g. automark_dependency is not set.

    Since automark_dependency defaults to false and test_a is not
    marked, the outcome of test_a will not be recorded.  As a result,
    test_b will be skipped due to a missing dependency.
    """
    ctestdir.makepyfile("""
        import pytest

        def test_a():
            pass

        @pytest.mark.dependency(depends=["test_a"])
        def test_b():
            pass
    """)
    result = ctestdir.runpytest("--verbose", "-rs")
    result.assert_outcomes(passed=1, skipped=1, failed=0)
    result.stdout.re_match_lines(r"""
        .*::test_a PASSED
        .*::test_b SKIPPED(?:\s+\(.*\))?
    """)


@pytest.mark.parametrize(
    "false_value", ["0", "no", "n", "False", "false", "f", "off"]
)
def test_set_false(ctestdir, false_value):
    """A pytest.ini is present, automark_dependency is set to false.

    Since automark_dependency is set to false and test_a is not
    marked, the outcome of test_a will not be recorded.  As a result,
    test_b will be skipped due to a missing dependency.
    """
    ctestdir.makefile('.ini', pytest="""
        [pytest]
        automark_dependency = %s
        console_output_style = classic
    """ % false_value)
    ctestdir.makepyfile("""
        import pytest

        def test_a():
            pass

        @pytest.mark.dependency(depends=["test_a"])
        def test_b():
            pass
    """)
    result = ctestdir.runpytest("--verbose", "-rs")
    result.assert_outcomes(passed=1, skipped=1, failed=0)
    result.stdout.re_match_lines(r"""
        .*::test_a PASSED
        .*::test_b SKIPPED(?:\s+\(.*\))?
    """)


@pytest.mark.parametrize(
    "true_value", ["1", "yes", "y", "True", "true", "t", "on"]
)
def test_set_true(ctestdir, true_value):
    """A pytest.ini is present, automark_dependency is set to false.

    Since automark_dependency is set to true, the outcome of test_a
    will be recorded, even though it is not marked.  As a result,
    test_b will be skipped due to a missing dependency.
    """
    ctestdir.makefile('.ini', pytest="""
        [pytest]
        automark_dependency = %s
        console_output_style = classic
    """ % true_value)
    ctestdir.makepyfile("""
        import pytest

        def test_a():
            pass

        @pytest.mark.dependency(depends=["test_a"])
        def test_b():
            pass
    """)
    result = ctestdir.runpytest("--verbose", "-rs")
    result.assert_outcomes(passed=2, skipped=0, failed=0)
    result.stdout.re_match_lines(r"""
        .*::test_a PASSED
        .*::test_b PASSED
    """)
