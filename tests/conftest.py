import pytest

pytest_plugins = "pytester"


@pytest.fixture
def ctestdir(testdir):
    testdir.makeconftest("""
        pytest_plugins = "pytest_dependency"
    """)
    return testdir
