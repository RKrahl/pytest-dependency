import pytest

def pytest_dependency_override_skip(item: pytest.Item, dependency: str, scope: str) -> bool:
    """
    Possibly override decision to skip a test item with a dependency.

    If any implementation of this hook returns a true value `dependency`
    being unknown or skipped will not cause `item` to be skipped.
    """
