"""Test the included examples.
"""

import pytest
from conftest import get_example


def test_basic(ctestdir):
    """Basic usage
    """
    with get_example("basic.py").open("rt") as f:
        ctestdir.makepyfile(f.read())
    result = ctestdir.runpytest("--verbose")
    try:
        result.assert_outcomes(passed=2, skipped=2, failed=0, xfailed=1)
    except TypeError:
        result.assert_outcomes(passed=2, skipped=2, failed=0)
    result.stdout.re_match_lines(r"""
        .*::test_a (?:XFAIL(?:\s+\(.*\))?|xfail)
        .*::test_b PASSED
        .*::test_c SKIPPED(?:\s+\(.*\))?
        .*::test_d PASSED
        .*::test_e SKIPPED(?:\s+\(.*\))?
    """)


def test_named(ctestdir):
    """Naming tests
    """
    with get_example("named.py").open("rt") as f:
        ctestdir.makepyfile(f.read())
    result = ctestdir.runpytest("--verbose")
    try:
        result.assert_outcomes(passed=2, skipped=2, failed=0, xfailed=1)
    except TypeError:
        result.assert_outcomes(passed=2, skipped=2, failed=0)
    result.stdout.re_match_lines(r"""
        .*::test_a (?:XFAIL(?:\s+\(.*\))?|xfail)
        .*::test_b PASSED
        .*::test_c SKIPPED(?:\s+\(.*\))?
        .*::test_d PASSED
        .*::test_e SKIPPED(?:\s+\(.*\))?
    """)


def test_testclass(ctestdir):
    """Using test classes
    """
    with get_example("testclass.py").open("rt") as f:
        ctestdir.makepyfile(f.read())
    result = ctestdir.runpytest("--verbose")
    try:
        result.assert_outcomes(passed=4, skipped=4, failed=0, xfailed=2)
    except TypeError:
        result.assert_outcomes(passed=4, skipped=4, failed=0)
    result.stdout.re_match_lines(r"""
        .*::TestClass::test_a (?:XFAIL(?:\s+\(.*\))?|xfail)
        .*::TestClass::test_b PASSED
        .*::TestClass::test_c SKIPPED(?:\s+\(.*\))?
        .*::TestClass::test_d PASSED
        .*::TestClass::test_e SKIPPED(?:\s+\(.*\))?
        .*::TestClassNamed::test_a (?:XFAIL(?:\s+\(.*\))?|xfail)
        .*::TestClassNamed::test_b PASSED
        .*::TestClassNamed::test_c SKIPPED(?:\s+\(.*\))?
        .*::TestClassNamed::test_d PASSED
        .*::TestClassNamed::test_e SKIPPED(?:\s+\(.*\))?
    """)


def test_mark_class(ctestdir):
    """Applying the dependency marker to a class as a whole
    """
    with get_example("mark-class.py").open("rt") as f:
        ctestdir.makepyfile(f.read())
    result = ctestdir.runpytest("--verbose")
    try:
        result.assert_outcomes(passed=1, skipped=2, failed=0, xfailed=1)
    except TypeError:
        result.assert_outcomes(passed=1, skipped=2, failed=0)
    result.stdout.re_match_lines(r"""
        .*::test_f (?:XFAIL(?:\s+\(.*\))?|xfail)
        .*::TestClass::test_a SKIPPED(?:\s+\(.*\))?
        .*::TestClass::test_b PASSED
        .*::TestClass::test_c SKIPPED(?:\s+\(.*\))?
    """)


def test_parametrized(ctestdir):
    """Parametrized tests
    """
    with get_example("parametrized.py").open("rt") as f:
        ctestdir.makepyfile(f.read())
    result = ctestdir.runpytest("--verbose")
    try:
        result.assert_outcomes(passed=7, skipped=5, failed=0, xfailed=1)
    except TypeError:
        result.assert_outcomes(passed=7, skipped=5, failed=0)
    result.stdout.re_match_lines(r"""
        .*::test_a\[0-0\] PASSED
        .*::test_a\[0-1\] (?:XFAIL(?:\s+\(.*\))?|xfail)
        .*::test_a\[1-0\] PASSED
        .*::test_a\[1-1\] PASSED
        .*::test_b\[1-2\] SKIPPED(?:\s+\(.*\))?
        .*::test_b\[1-3\] PASSED
        .*::test_b\[1-4\] PASSED
        .*::test_b\[2-3\] SKIPPED(?:\s+\(.*\))?
        .*::test_b\[2-4\] SKIPPED(?:\s+\(.*\))?
        .*::test_b\[3-4\] PASSED
        .*::test_c\[1\] SKIPPED(?:\s+\(.*\))?
        .*::test_c\[2\] PASSED
        .*::test_c\[3\] SKIPPED(?:\s+\(.*\))?
    """)


def test_runtime(ctestdir):
    """Marking dependencies at runtime
    """
    with get_example("runtime.py").open("rt") as f:
        ctestdir.makepyfile(f.read())
    result = ctestdir.runpytest("--verbose")
    try:
        result.assert_outcomes(passed=1, skipped=2, failed=0, xfailed=1)
    except TypeError:
        result.assert_outcomes(passed=1, skipped=2, failed=0)
    result.stdout.re_match_lines(r"""
        .*::test_a PASSED
        .*::test_b (?:XFAIL(?:\s+\(.*\))?|xfail)
        .*::test_c SKIPPED(?:\s+\(.*\))?
        .*::test_d SKIPPED(?:\s+\(.*\))?
    """)
