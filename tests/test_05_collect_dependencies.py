"""Test the collect_dependencies option.
"""

import pytest


def test_no_set_collect_dependencies(ctestdir):
    """No pytest.ini file, e.g. collect_dependencies is not set.

    Explicitly select only a single test that depends on another one.
    Since collect_dependencies defaults to false, and the other test has not been run at all, the selected test
    will be skipped.

    """
    ctestdir.makepyfile("""
        import pytest

        @pytest.mark.dependency()
        def test_a():
            pass

        @pytest.mark.dependency()
        def test_b():
            pass

        @pytest.mark.dependency()
        def test_c():
            pass

        @pytest.mark.dependency(depends=["test_c"])
        def test_d():
            pass
    """)
    result = ctestdir.runpytest("--verbose", "test_no_set_collect_dependencies.py::test_d")
    result.assert_outcomes(passed=0, skipped=1, failed=0)
    result.stdout.re_match_lines(r"""
        .*::test_d SKIPPED(?:\s+\(.*\))?
    """)


def test_collect_dependencies_false(ctestdir):
    """A pytest.ini is present, collect_dependencies is set to false.

    Explicitly select only a single test that depends on another one.
    Since collect_dependencies is set to false, and the other test has not been run at all, the selected test
    will be skipped.

    """
    ctestdir.makefile('.ini', pytest="""
            [pytest]
            collect_dependencies = false
            console_output_style = classic
        """)

    ctestdir.makepyfile("""
        import pytest

        @pytest.mark.dependency()
        def test_a():
            pass

        @pytest.mark.dependency()
        def test_b():
            pass

        @pytest.mark.dependency()
        def test_c():
            pass

        @pytest.mark.dependency(depends=["test_c"])
        def test_d():
            pass
    """)
    result = ctestdir.runpytest("--verbose", "test_collect_dependencies_false.py::test_d")
    result.assert_outcomes(passed=0, skipped=1, failed=0)
    result.stdout.re_match_lines(r"""
        .*::test_d SKIPPED(?:\s+\(.*\))?
    """)




def test_collect_dependencies_true(ctestdir):
    """A pytest.ini is present, collect_dependencies is set to true.

    Explicitly select only a single test that depends on another one.
    Since collect_dependencies is set to true, the other test will be collected, and both tests will be run.
    """
    ctestdir.makefile('.ini', pytest="""
            [pytest]
            collect_dependencies = true
            console_output_style = classic
        """)

    ctestdir.makepyfile("""
        import pytest

        @pytest.mark.dependency()
        def test_a():
            pass

        @pytest.mark.dependency()
        def test_b():
            pass

        @pytest.mark.dependency()
        def test_c():
            pass

        @pytest.mark.dependency(depends=["test_c"])
        def test_d():
            pass
    """)
    result = ctestdir.runpytest("--verbose", "test_collect_dependencies_true.py::test_d")
    result.assert_outcomes(passed=2, skipped=0, failed=0)
    result.stdout.re_match_lines(r"""
            .*::test_c PASSED
            .*::test_d PASSED
        """)


def test_collect_dependencies_true_recursive(ctestdir):
    """A pytest.ini is present, collect_dependencies is set to true.

    Explicitly select only a single test that depends on another one, that depends from others two.
    Since collect_dependencies is set to true, the dependent tests will be recursively collected, and four tests will be run.
    """
    ctestdir.makefile('.ini', pytest="""
            [pytest]
            collect_dependencies = true
            console_output_style = classic
        """)

    ctestdir.makepyfile("""
        import pytest

        @pytest.mark.dependency()
        def test_a():
            pass

        @pytest.mark.dependency()
        def test_b():
            pass

        @pytest.mark.dependency(depends=["test_b", "test_a"])
        def test_c():
            pass

        @pytest.mark.dependency(depends=["test_c"])
        def test_d():
            pass
    """)
    result = ctestdir.runpytest("--verbose", "test_collect_dependencies_true_recursive.py::test_d")
    print(result)
    result.assert_outcomes(passed=4, skipped=0, failed=0)
    result.stdout.re_match_lines(r"""
            .*::test_a PASSED
            .*::test_b PASSED
            .*::test_c PASSED
            .*::test_d PASSED
        """)
