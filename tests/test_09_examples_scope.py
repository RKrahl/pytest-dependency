"""Test the included examples.
"""

from pathlib import Path
import pytest
from conftest import get_example


def test_scope_module(ctestdir):
    """Explicitly specifying the scope
    """
    with get_example("scope_module.py").open("rt") as f:
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


def test_scope_session(ctestdir):
    """Dependencies in session scope
    """
    subdir = Path(str(ctestdir.tmpdir)) / "tests"
    subdir.mkdir()
    with get_example("scope_session_mod_01.py").open("rt") as sf:
        with (subdir / "test_mod_01.py").open("wt") as df:
            df.write(sf.read())
    with get_example("scope_session_mod_02.py").open("rt") as sf:
        with (subdir / "test_mod_02.py").open("wt") as df:
            df.write(sf.read())
    result = ctestdir.runpytest("--verbose")
    try:
        result.assert_outcomes(passed=5, skipped=1, failed=0, xfailed=2)
    except TypeError:
        result.assert_outcomes(passed=5, skipped=1, failed=0)
    result.stdout.re_match_lines(r"""
        tests/test_mod_01.py::test_a PASSED
        tests/test_mod_01.py::test_b (?:XFAIL(?:\s+\(.*\))?|xfail)
        tests/test_mod_01.py::test_c PASSED
        tests/test_mod_01.py::TestClass::test_b PASSED
        tests/test_mod_02.py::test_a (?:XFAIL(?:\s+\(.*\))?|xfail)
        tests/test_mod_02.py::test_e PASSED
        tests/test_mod_02.py::test_f SKIPPED(?:\s+\(.*\))?
        tests/test_mod_02.py::test_g PASSED
    """)


def test_scope_class(ctestdir):
    """The class scope
    """
    with get_example("scope_class.py").open("rt") as f:
        ctestdir.makepyfile(f.read())
    result = ctestdir.runpytest("--verbose")
    try:
        result.assert_outcomes(passed=3, skipped=2, failed=0, xfailed=1)
    except TypeError:
        result.assert_outcomes(passed=3, skipped=2, failed=0)
    result.stdout.re_match_lines(r"""
        .*::test_a (?:XFAIL(?:\s+\(.*\))?|xfail)
        .*::TestClass1::test_b PASSED
        .*::TestClass2::test_a PASSED
        .*::TestClass2::test_c SKIPPED(?:\s+\(.*\))?
        .*::TestClass2::test_d PASSED
        .*::TestClass2::test_e SKIPPED(?:\s+\(.*\))?
    """)
