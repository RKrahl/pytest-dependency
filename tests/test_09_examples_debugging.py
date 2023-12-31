"""Test the included examples.
"""

import pytest
from conftest import get_example


def test_debugging(ctestdir):
    """Debugging example
    """
    # The debugging example requires the enum module which is has been
    # added to the standard library in Python 3.4.  Skip this test if
    # the module is not available.
    _ = pytest.importorskip("enum")
    with get_example("debugging.py").open("rt") as f:
        ctestdir.makepyfile(f.read())
    result = ctestdir.runpytest("--verbose")
    try:
        result.assert_outcomes(passed=12, skipped=11, failed=0, xfailed=2)
    except TypeError:
        result.assert_outcomes(passed=12, skipped=11, failed=0)
    result.stdout.re_match_lines(r"""
        .*::test_a (?:XFAIL(?:\s+\(.*\))?|xfail)
        .*::test_b PASSED
        .*::test_c SKIPPED(?:\s+\(.*\))?
        .*::test_d PASSED
        .*::test_e SKIPPED(?:\s+\(.*\))?
        .*::TestClass::test_a PASSED
        .*::TestClass::test_b (?:XFAIL(?:\s+\(.*\))?|xfail)
        .*::TestClass::test_c PASSED
        .*::test_colors\[RED\] PASSED
        .*::test_colors\[GREEN\] PASSED
        .*::test_colors\[BLUE\] PASSED
        .*::test_multicolored SKIPPED(?:\s+\(.*\))?
        .*::test_alert SKIPPED(?:\s+\(.*\))?
        .*::test_g SKIPPED(?:\s+\(.*\))?
        .*::test_h PASSED
        .*::test_k SKIPPED(?:\s+\(.*\))?
        .*::test_l\[0\] PASSED
        .*::test_q\[0\] SKIPPED(?:\s+\(.*\))?
        .*::test_l\[1\] PASSED
        .*::test_q\[1\] SKIPPED(?:\s+\(.*\))?
        .*::test_m SKIPPED(?:\s+\(.*\))?
        .*::test_o SKIPPED(?:\s+\(.*\))?
        .*::test_p PASSED
        .*::test_r PASSED
        .*::test_s SKIPPED(?:\s+\(.*\))?
    """)
