"""Test the accept_xfail option.
"""

import pytest


def test_accept_xfail_not_set(ctestdir):
    """No pytest.ini file, therefore accept_xfail is not set.

    Since accept_xfail defaults to False and test_a is marked as xfail, 
    the xfailed outcome of test_a will be considered as skipped. As a result,
    test_b will be skipped since its dependency was not successful.
    """
    ctestdir.makepyfile("""
        import pytest

        @pytest.mark.dependency()
        @pytest.mark.xfail()
        def test_a():
            assert False

        @pytest.mark.dependency(depends=["test_a"])
        def test_b():
            pass
    """)
    result = ctestdir.runpytest("--verbose", "-rs")
    result.assert_outcomes(xfailed=1, skipped=1)
    result.stdout.re_match_lines(r"""
        .*::test_a XFAIL
        .*::test_b SKIPPED(?:\s+\(.*\))?
    """)


@pytest.mark.parametrize(
    "false_value", ["0", "no", "n", "False", "false", "f", "off"]
)
def test_accept_xfail_set_false(ctestdir, false_value):
    """A pytest.ini is present, accept_xfail is set to False.

    Since accept_xfail is set to False and test_a is marked as xfail, 
    the xfailed outcome of test_a will be considered as skipped. As a result,
    test_b will be skipped since its dependency was not successful.
    """
    ctestdir.makefile('.ini', pytest="""
        [pytest]
        accept_xfail = %s
        console_output_style = classic
    """ % false_value)
    ctestdir.makepyfile("""
        import pytest

        @pytest.mark.dependency()
        @pytest.mark.xfail()
        def test_a():
            assert False

        @pytest.mark.dependency(depends=["test_a"])
        def test_b():
            pass
    """)
    result = ctestdir.runpytest("--verbose", "-rs")
    result.assert_outcomes(xfailed=1, skipped=1)
    result.stdout.re_match_lines(r"""
        .*::test_a XFAIL
        .*::test_b SKIPPED(?:\s+\(.*\))?
    """)


@pytest.mark.parametrize(
    "true_value", ["1", "yes", "y", "True", "true", "t", "on"]
)
def test_accept_xfail_set_true(ctestdir, true_value):
    """A pytest.ini is present, accept_xfail is set to True.

    Since accept_xfail is set to True and test_a is marked as xfail, 
    the xfailed outcome of test_a will be considered as passing. As a result,
    test_b will be executed since its dependency was successful.
    """
    ctestdir.makefile('.ini', pytest="""
        [pytest]
        accept_xfail = %s
        console_output_style = classic
    """ % true_value)
    ctestdir.makepyfile("""
        import pytest

        @pytest.mark.dependency()
        @pytest.mark.xfail()
        def test_a():
            assert False

        @pytest.mark.dependency(depends=["test_a"])
        def test_b():
            pass
    """)
    result = ctestdir.runpytest("--verbose", "-rs")
    result.assert_outcomes(xfailed=1, passed=1, skipped=0)
    result.stdout.re_match_lines(r"""
        .*::test_a XFAIL
        .*::test_b PASSED
    """)
