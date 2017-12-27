"""The most basic test: check that the marker works.
"""

import pytest


def test_marker_registered(ctestdir):
    result = ctestdir.runpytest("--markers")
    result.stdout.fnmatch_lines("""
        @pytest.mark.dependency*
    """)


def test_marker(ctestdir):
    ctestdir.makepyfile("""
        import pytest
        from pytest_dependency import DependencyManager

        @pytest.mark.dependency()
        def test_marker(request):
            node = request.node.getparent(pytest.Module)
            assert hasattr(node, 'dependencyManager')
            assert isinstance(node.dependencyManager, DependencyManager)
            assert 'test_marker' in node.dependencyManager.results
    """)
    result = ctestdir.runpytest("--verbose")
    result.assert_outcomes(passed=1)
