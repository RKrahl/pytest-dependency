import pytest

@pytest.mark.dependency()
@pytest.mark.xfail(reason="deliberate fail")
def test_a():
    assert False


class TestClass1(object):

    @pytest.mark.dependency()
    def test_b(self):
        pass


class TestClass2(object):

    @pytest.mark.dependency()
    def test_a(self):
        pass

    @pytest.mark.dependency(depends=["test_a"])
    def test_c(self):
        pass

    @pytest.mark.dependency(depends=["test_a"], scope='class')
    def test_d(self):
        pass

    @pytest.mark.dependency(depends=["test_b"], scope='class')
    def test_e(self):
        pass
