"""
Tests ordering.
"""


def test_order_standard(ctestdir):
    """
    One module and 7 tests designed to cover most cases the ordering can fail in.
    """
    ctestdir.makepyfile("""
        import pytest

        # this empty one should stay first
        @pytest.mark.dependency()
        def test_a():
            pass

        # misordered dependencies, this should end up near the bottom
        @pytest.mark.dependency(depends=["test_f", "test_d", "test_e"])
        def test_b():
            pass

        # this empty one should occur after 'test_a' but before 'test_d'
        @pytest.mark.dependency(depends=["test_a"])
        def test_c():
            pass

        # right after 'test_c'
        @pytest.mark.dependency()
        def test_d():
            pass

        # correct order already
        @pytest.mark.dependency(depends=["test_d"])
        def test_e():
            pass

        # same here
        @pytest.mark.dependency(depends=["test_c", "test_d"])
        def test_f():
            pass

        # and here - 'test_b' should land just before this test
        @pytest.mark.dependency(depends=["test_c"])
        def test_g():
            pass
    """)
    result = ctestdir.runpytest("--verbose")
    result.assert_outcomes(passed=7, skipped=0, failed=0)
    result.stdout.fnmatch_lines("""
        test_order_standard.py::test_a PASSED
        test_order_standard.py::test_c PASSED
        test_order_standard.py::test_d PASSED
        test_order_standard.py::test_e PASSED
        test_order_standard.py::test_f PASSED
        test_order_standard.py::test_b PASSED
        test_order_standard.py::test_g PASSED
    """)


def test_order_missing(ctestdir):
    """
    5 tests, with 2 of them having mislabeled (missing) dependencies.
    """
    ctestdir.makepyfile("""
        import pytest

        @pytest.mark.dependency()
        def test_a():
            pass

        # mislabeled 'test_c'
        @pytest.mark.dependency(depends=["tets_c"])
        def test_b():
            pass

        @pytest.mark.dependency()
        def test_c():
            pass

        # mislabeled 'test_a'
        @pytest.mark.dependency(depends=["tets_a"])
        def test_d():
            pass

        @pytest.mark.dependency()
        def test_e():
            pass
    """)
    result = ctestdir.runpytest("--verbose")
    result.assert_outcomes(passed=3, skipped=2, failed=0)
    result.stdout.fnmatch_lines("""
        test_order_missing.py::test_a PASSED
        test_order_missing.py::test_c PASSED
        test_order_missing.py::test_e PASSED
        test_order_missing.py::test_b SKIPPED
        test_order_missing.py::test_d SKIPPED
    """)


def test_order_cycles(ctestdir):
    """
    5 tests, with 2 of them creating an "accidental" cycle.
    """
    ctestdir.makepyfile("""
        import pytest

        @pytest.mark.dependency()
        def test_a():
            pass

        # depends on 'test_d' - cycle
        @pytest.mark.dependency(depends=["test_d"])
        def test_b():
            pass

        @pytest.mark.dependency()
        def test_c():
            pass

        # depends on 'test_b' - cycle
        @pytest.mark.dependency(depends=["test_b", "test_c"])
        def test_d():
            pass

        @pytest.mark.dependency()
        def test_e():
            pass
    """)
    result = ctestdir.runpytest("--verbose")
    result.assert_outcomes(passed=3, skipped=2, failed=0)
    result.stdout.fnmatch_lines("""
        test_order_cycles.py::test_a PASSED
        test_order_cycles.py::test_c PASSED
        test_order_cycles.py::test_e PASSED
        test_order_cycles.py::test_b SKIPPED
        test_order_cycles.py::test_d SKIPPED
    """)


def test_order_nesting(ctestdir):
    """
    8 tests, with tests depending on tests that depend on
    other tests that might be reordered later too.
    """
    ctestdir.makepyfile("""
        import pytest

        @pytest.mark.dependency()
        def test_a():
            pass

        @pytest.mark.dependency(depends=["test_d"])
        def test_b():
            pass

        @pytest.mark.dependency()
        def test_c():
            pass

        @pytest.mark.dependency(depends=["test_f"])
        def test_d():
            pass

        @pytest.mark.dependency()
        def test_e():
            pass

        @pytest.mark.dependency(depends=["test_g"])
        def test_f():
            pass

        @pytest.mark.dependency()
        def test_g():
            pass

        @pytest.mark.dependency()
        def test_h():
            pass
    """)
    result = ctestdir.runpytest("--verbose")
    result.assert_outcomes(passed=8, skipped=0, failed=0)
    result.stdout.fnmatch_lines("""
        test_order_nesting.py::test_a PASSED
        test_order_nesting.py::test_c PASSED
        test_order_nesting.py::test_e PASSED
        test_order_nesting.py::test_g PASSED
        test_order_nesting.py::test_f PASSED
        test_order_nesting.py::test_d PASSED
        test_order_nesting.py::test_b PASSED
        test_order_nesting.py::test_h PASSED
    """)


def test_order_scopes(ctestdir):
    """
    9 tests, with dependencies spread between 'module' and 'session' scopes.
    """
    ctestdir.makepyfile("""
        import pytest

        @pytest.mark.dependency()
        def test_a():
            pass

        @pytest.mark.dependency(depends=["test_c"])
        def test_b():
            pass

        @pytest.mark.dependency()
        def test_c():
            pass

        @pytest.mark.dependency(depends=["test_order_scopes.py::test_e"], scope="session")
        def test_d():
            pass

        @pytest.mark.dependency()
        @pytest.mark.dependency(scope="session")
        def test_e():
            pass

        @pytest.mark.dependency(depends=["test_g"])
        @pytest.mark.dependency(depends=["test_order_scopes.py::test_e"], scope="session")
        def test_f():
            pass

        @pytest.mark.dependency()
        def test_g():
            pass

        @pytest.mark.dependency(depends=["test_order_scopes.py::test_i"], scope="session")
        @pytest.mark.dependency(depends=["test_e"])
        def test_h():
            pass

        @pytest.mark.dependency(scope="session")
        def test_i():
            pass
    """)
    result = ctestdir.runpytest("--verbose")
    result.assert_outcomes(passed=9, skipped=0, failed=0)
    result.stdout.fnmatch_lines("""
        test_order_scopes.py::test_a PASSED
        test_order_scopes.py::test_c PASSED
        test_order_scopes.py::test_b PASSED
        test_order_scopes.py::test_e PASSED
        test_order_scopes.py::test_d PASSED
        test_order_scopes.py::test_g PASSED
        test_order_scopes.py::test_f PASSED
        test_order_scopes.py::test_i PASSED
        test_order_scopes.py::test_h PASSED
    """)
