


def test_session_scope(ctestdir):
    """ test_1 is marked dependent on test_a in the test_a.py file, that test
    failed and causes test_1 to be skipped.  Also test using session scope to
    select a test dependency within the same module"""
    test_file1 = """
        import pytest

        @pytest.mark.dependency()
        def test_a():
            assert False

        @pytest.mark.dependency(scope="session", depends=["test_a.py::test_a"])
        def test_b():
            pass
    """

    test_file2 = """
        import pytest

        @pytest.mark.dependency()
        def test_0():
            pass

        @pytest.mark.dependency(scope="session", depends=["test_a.py::test_a"])
        def test_1():
            pass
    """

    ctestdir.makepyfile(test_a=test_file1, test_b=test_file2)

    result = ctestdir.runpytest("--verbose", "test_a.py", "test_b.py")
    result.assert_outcomes(passed=1, skipped=2, failed=1)
    result.stdout.fnmatch_lines("""
        *::test_a FAILED
        *::test_b SKIPPED
        *::test_0 PASSED
        *::test_1 SKIPPED
    """)


def test_session_scope_three_files(ctestdir):
    """ Test using 3 files with the third file depending on functions from either
    the first or second file """
    test_file1 = """
        import pytest

        @pytest.mark.dependency()
        def test_fail():
            assert False

        @pytest.mark.dependency()
        def test_pass():
            pass
    """

    test_file2 = """
        import pytest

        @pytest.mark.dependency()
        def test_pass():
            pass

        @pytest.mark.dependency()
        def test_fail():
            assert False
    """

    test_file3 = """
        import pytest

        @pytest.mark.dependency()
        def test_0():
            pass

        @pytest.mark.dependency(scope="session", depends=["test_a.py::test_fail", "test_b.py::test_pass"])
        def test_1():
            pass

        @pytest.mark.dependency(scope="session", depends=["test_a.py::test_pass", "test_b.py::test_fail"])
        def test_2():
            pass

        @pytest.mark.dependency(scope="session", depends=["test_a.py::test_pass", "test_b.py::test_pass"])
        def test_3():
            pass
    """

    ctestdir.makepyfile(test_a=test_file1, test_b=test_file2, test_c=test_file3)

    result = ctestdir.runpytest("--verbose", "test_a.py", "test_b.py", "test_c.py")
    result.assert_outcomes(passed=4, skipped=2, failed=2)
    result.stdout.fnmatch_lines("""
        test_a.py::test_fail FAILED
        test_a.py::test_pass PASSED
        test_b.py::test_pass PASSED
        test_b.py::test_fail FAILED
        *::test_0 PASSED
        *::test_1 SKIPPED
        *::test_2 SKIPPED
        *::test_3 PASSED
    """)
