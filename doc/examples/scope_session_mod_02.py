# test_mod_02.py

import pytest

@pytest.mark.dependency()
@pytest.mark.xfail(reason="deliberate fail")
def test_a():
    assert False

@pytest.mark.dependency(
    depends=["tests/test_mod_01.py::test_a", "tests/test_mod_01.py::test_c"],
    scope='session'
)
def test_e():
    pass

@pytest.mark.dependency(
    depends=["tests/test_mod_01.py::test_b", "tests/test_mod_02.py::test_e"],
    scope='session'
)
def test_f():
    pass

@pytest.mark.dependency(
    depends=["tests/test_mod_01.py::TestClass::test_b"],
    scope='session'
)
def test_g():
    pass
