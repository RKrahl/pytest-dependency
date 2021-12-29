from pathlib import Path
import pytest

pytest_plugins = "pytester"

example_dir = (Path(__file__).parent / "../doc/examples").resolve()

def get_example(fname):
    path = example_dir / fname
    assert path.is_file()
    return path


@pytest.fixture
def ctestdir(testdir):
    testdir.makefile('.ini', pytest="""
        [pytest]
        console_output_style = classic
    """)
    testdir.makeconftest("""
        import sys
        if "pytest_dependency" not in sys.modules:
            pytest_plugins = "pytest_dependency"
    """)
    return testdir
