"""The most basic test: check that the marker works.
"""

import pytest

pytest_plugins = "pytester"


def test_marker(testdir):
    testdir.makepyfile("""
        import pytest
        from pytest_dependency import DependencyManager

        pytest_plugins = "pytest_dependency"

        @pytest.mark.dependency()
        def test_marker(request):
            node = request.node.getparent(pytest.Module)
            assert hasattr(node, 'dependencyManager')
            assert isinstance(node.dependencyManager, DependencyManager)
            assert 'test_marker' in node.dependencyManager.results
    """)
    result = testdir.runpytest("--verbose")
    result.assert_outcomes(passed=1)
