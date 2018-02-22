


def test_class_scope(ctestdir):
    """ test_a fails, however the scope of the dependency of TestClass::test_b
    causes it to only depend on other tests within its class.  test_d failing
    shows that the class scope is actually detecting failures within its own
    class.  test_f should skip since test_c within the depends on test_c
    within the class failed """
    ctestdir.makepyfile("""
        import pytest

        @pytest.mark.dependency()
        def test_a():
            assert False

        class TestClass(object):

            @pytest.mark.dependency()
            def test_a(self):
                pass

            @pytest.mark.dependency(scope="class", depends="all")
            def test_b(self):
                pass

            @pytest.mark.dependency()
            def test_c(self):
                assert False

            @pytest.mark.dependency(scope="class", depends="all")
            def test_d(self):
                pass

        @pytest.mark.dependency()
        def test_e():
            pass

        @pytest.mark.dependency(depends=["TestClass::test_c"])
        def test_f():
            pass

    """)

    result = ctestdir.runpytest("--verbose", "test_class_scope.py")
    result.assert_outcomes(passed=3, skipped=2, failed=2)
    result.stdout.fnmatch_lines("""
        *::test_a FAILED
        *::TestClass::test_a PASSED
        *::TestClass::test_b PASSED
        *::TestClass::test_c FAILED
        *::TestClass::test_d SKIPPED
        *::test_e PASSED
        *::test_f SKIPPED
    """)


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




def test_complex_scope(ctestdir):
    """ A complex test of scope utilizing module, class and session scopes.  Also utilizing the
    depends="all" modifier """
    test_file1 = """
        import pytest

        @pytest.mark.dependency()
        def test_a():
            assert False

        @pytest.mark.dependency()
        def test_b():
            pass

        @pytest.mark.dependency(depends="all")
        def test_c():
            pass

        @pytest.mark.dependency(depends=["test_c"])
        def test_d():
            pass

        class TestFile1():
            @pytest.mark.dependency()
            def test_0(self):
                pass
    """

    test_file2 = """
        import pytest

        def test_v():
            pass

        @pytest.mark.dependency(scope="session", depends="all")
        def test_w():
            pass

        @pytest.mark.dependency(scope="session", depends=["test_a.py::TestFile1::test_0"])
        def test_x():
            pass

        class TestFile2():
            def test_0(self):
                pass

            @pytest.mark.dependency(scope="class", depends="all")
            def test_1(self):
                pass

            @pytest.mark.dependency(scope="module", depends="all")
            def test_2(self):
                pass

            @pytest.mark.dependency(scope="session", depends="all")
            def test_3(self):
                pass

        @pytest.mark.dependency(scope="session", depends=["test_a.py::test_b"])
        def test_y():
            pass

        @pytest.mark.dependency(scope="session", depends=["test_a.py::test_a"])
        def test_z():
            pass
    """
    ctestdir.makepyfile(test_a=test_file1, test_b=test_file2)

    result = ctestdir.runpytest("--verbose", "test_a.py", "test_b.py")
    result.assert_outcomes(passed=7, skipped=6, failed=1)
    result.stdout.fnmatch_lines("""
        *::test_a FAILED
        *::test_b PASSED
        *::test_c SKIPPED
        *::test_d SKIPPED
        *::TestFile1::test_0 PASSED
        *::test_v PASSED
        *::test_w SKIPPED
        *::test_x PASSED
        *::TestFile2::test_0 PASSED
        *::TestFile2::test_1 PASSED
        *::TestFile2::test_2 SKIPPED
        *::TestFile2::test_3 SKIPPED
        *::test_y PASSED
        *::test_z SKIPPED
    """)
