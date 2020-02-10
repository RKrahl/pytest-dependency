# test_mod_01.py

import pytest

@pytest.mark.dependency()
def test_a():
    pass

@pytest.mark.dependency()
@pytest.mark.xfail(reason="deliberate fail")
def test_b():
    assert False

@pytest.mark.dependency(depends=["test_a"])
def test_c():
    pass


class TestClass(object):

    @pytest.mark.dependency()
    def test_b(self):
        pass
