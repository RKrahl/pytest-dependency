import pytest

@pytest.mark.dependency()
@pytest.mark.xfail(reason="deliberate fail")
def test_a():
    assert False

@pytest.mark.dependency()
def test_b():
    pass

@pytest.mark.dependency(depends=["test_a"], scope='module')
def test_c():
    pass

@pytest.mark.dependency(depends=["test_b"], scope='module')
def test_d():
    pass

@pytest.mark.dependency(depends=["test_b", "test_c"], scope='module')
def test_e():
    pass
