import pytest


@pytest.mark.dependency()
@pytest.mark.xfail(reason="deliberate fail")
def test_f():
    assert False


@pytest.mark.dependency(depends=["test_f"])
class TestClass(object):

    def test_a(self):
        pass

    @pytest.mark.dependency()
    def test_b(self):
        pass

    def test_c(self):
        pass
