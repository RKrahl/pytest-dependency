"""Test the included examples.
"""

import pytest
from conftest import get_example


def test_nodeid(ctestdir):
    """Node ids
    """
    with get_example("nodeid.py").open("rt") as f:
        ctestdir.makepyfile(f.read())
    result = ctestdir.runpytest("--verbose")
    try:
        result.assert_outcomes(passed=6, skipped=0, failed=0, xfailed=1)
    except TypeError:
        result.assert_outcomes(passed=6, skipped=0, failed=0)
    result.stdout.re_match_lines(r"""
        .*::test_a PASSED
        .*::test_b\[7-True\] PASSED
        .*::test_b\[0-False\] PASSED
        .*::test_b\[-1-False\] (?:XFAIL(?:\s+\(.*\))?|xfail)
        .*::TestClass::test_c PASSED
        .*::TestClass::test_d\[order\] PASSED
        .*::TestClass::test_d\[disorder\] PASSED
    """)
