"""Test the included examples.
"""

import pytest
from conftest import get_example


def test_dyn_parametrized(ctestdir):
    """Dynamic compilation of marked parameters
    """
    with get_example("dyn-parametrized.py").open("rt") as f:
        ctestdir.makepyfile(f.read())
    result = ctestdir.runpytest("--verbose")
    try:
        result.assert_outcomes(passed=11, skipped=1, failed=0, xfailed=1)
    except TypeError:
        result.assert_outcomes(passed=11, skipped=1, failed=0)
    result.stdout.re_match_lines(r"""
        .*::test_child\[c0\] PASSED
        .*::test_child\[c1\] PASSED
        .*::test_child\[c2\] PASSED
        .*::test_child\[c3\] PASSED
        .*::test_child\[c4\] PASSED
        .*::test_child\[c5\] PASSED
        .*::test_child\[c6\] PASSED
        .*::test_child\[c7\] (?:XFAIL(?:\s+\(.*\))?|xfail)
        .*::test_child\[c8\] PASSED
        .*::test_parent\[p0\] PASSED
        .*::test_parent\[p1\] PASSED
        .*::test_parent\[p2\] PASSED
        .*::test_parent\[p3\] SKIPPED(?:\s+\(.*\))?
    """)


def test_group_fixture1(ctestdir):
    """Grouping tests using fixtures 1
    """
    with get_example("group-fixture.py").open("rt") as f:
        ctestdir.makepyfile(f.read())
    result = ctestdir.runpytest("--verbose")
    try:
        result.assert_outcomes(passed=16, skipped=1, failed=0, xfailed=1)
    except TypeError:
        result.assert_outcomes(passed=16, skipped=1, failed=0)
    result.stdout.re_match_lines(r"""
        .*::test_a\[1\] PASSED
        .*::test_b\[1\] PASSED
        .*::test_a\[2\] PASSED
        .*::test_b\[2\] PASSED
        .*::test_a\[3\] PASSED
        .*::test_b\[3\] PASSED
        .*::test_a\[4\] PASSED
        .*::test_b\[4\] PASSED
        .*::test_a\[5\] PASSED
        .*::test_b\[5\] PASSED
        .*::test_a\[6\] PASSED
        .*::test_b\[6\] PASSED
        .*::test_a\[7\] (?:XFAIL(?:\s+\(.*\))?|xfail)
        .*::test_b\[7\] SKIPPED(?:\s+\(.*\))?
        .*::test_a\[8\] PASSED
        .*::test_b\[8\] PASSED
        .*::test_a\[9\] PASSED
        .*::test_b\[9\] PASSED
    """)


def test_group_fixture2(ctestdir):
    """Grouping tests using fixtures 2
    """
    with get_example("group-fixture2.py").open("rt") as f:
        ctestdir.makepyfile(f.read())
    result = ctestdir.runpytest("--verbose")
    try:
        result.assert_outcomes(passed=24, skipped=2, failed=0, xfailed=1)
    except TypeError:
        result.assert_outcomes(passed=24, skipped=2, failed=0)
    result.stdout.re_match_lines(r"""
        .*::test_a\[1\] PASSED
        .*::test_b\[1\] PASSED
        .*::test_c\[1\] PASSED
        .*::test_a\[2\] PASSED
        .*::test_b\[2\] PASSED
        .*::test_c\[2\] PASSED
        .*::test_a\[3\] PASSED
        .*::test_b\[3\] PASSED
        .*::test_c\[3\] PASSED
        .*::test_a\[4\] PASSED
        .*::test_b\[4\] PASSED
        .*::test_c\[4\] PASSED
        .*::test_a\[5\] PASSED
        .*::test_b\[5\] PASSED
        .*::test_c\[5\] PASSED
        .*::test_a\[6\] PASSED
        .*::test_b\[6\] PASSED
        .*::test_c\[6\] PASSED
        .*::test_a\[7\] (?:XFAIL(?:\s+\(.*\))?|xfail)
        .*::test_b\[7\] SKIPPED(?:\s+\(.*\))?
        .*::test_c\[7\] SKIPPED(?:\s+\(.*\))?
        .*::test_a\[8\] PASSED
        .*::test_b\[8\] PASSED
        .*::test_c\[8\] PASSED
        .*::test_a\[9\] PASSED
        .*::test_b\[9\] PASSED
        .*::test_c\[9\] PASSED
    """)


def test_all_params(ctestdir):
    """Depend on all instances of a parametrized test at once
    """
    with get_example("all_params.py").open("rt") as f:
        ctestdir.makepyfile(f.read())
    result = ctestdir.runpytest("--verbose")
    try:
        result.assert_outcomes(passed=20, skipped=3, failed=0, xfailed=3)
    except TypeError:
        result.assert_outcomes(passed=20, skipped=3, failed=0)
    result.stdout.re_match_lines(r"""
        .*::test_a\[0\] PASSED
        .*::test_a\[1\] PASSED
        .*::test_a\[2\] PASSED
        .*::test_a\[3\] PASSED
        .*::test_a\[4\] PASSED
        .*::test_a\[5\] PASSED
        .*::test_a\[6\] PASSED
        .*::test_a\[7\] PASSED
        .*::test_a\[8\] PASSED
        .*::test_a\[9\] PASSED
        .*::test_a\[10\] PASSED
        .*::test_a\[11\] PASSED
        .*::test_a\[12\] PASSED
        .*::test_a\[13\] (?:XFAIL(?:\s+\(.*\))?|xfail)
        .*::test_a\[14\] PASSED
        .*::test_a\[15\] PASSED
        .*::test_a\[16\] PASSED
        .*::test_b SKIPPED(?:\s+\(.*\))?
        .*::test_c\[0-2\] PASSED
        .*::test_c\[2-3\] PASSED
        .*::test_c\[4-4\] PASSED
        .*::test_c\[6-5\] (?:XFAIL(?:\s+\(.*\))?|xfail)
        .*::test_d SKIPPED(?:\s+\(.*\))?
        .*::test_e\[abc\] PASSED
        .*::test_e\[def\] (?:XFAIL(?:\s+\(.*\))?|xfail)
        .*::test_f SKIPPED(?:\s+\(.*\))?
    """)


def test_or_dependency(ctestdir):
    """Logical combinations of dependencies
    """
    with get_example("or_dependency.py").open("rt") as f:
        ctestdir.makepyfile(f.read())
    result = ctestdir.runpytest("--verbose")
    try:
        result.assert_outcomes(passed=5, skipped=1, failed=0, xfailed=2)
    except TypeError:
        result.assert_outcomes(passed=5, skipped=1, failed=0)
    result.stdout.re_match_lines(r"""
        .*::test_ap PASSED
        .*::test_ax (?:XFAIL(?:\s+\(.*\))?|xfail)
        .*::test_bp PASSED
        .*::test_bx (?:XFAIL(?:\s+\(.*\))?|xfail)
        .*::test_c SKIPPED(?:\s+\(.*\))?
        .*::test_d PASSED
        .*::test_e PASSED
        .*::test_f PASSED
    """)
