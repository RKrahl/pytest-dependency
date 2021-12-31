from enum import Enum
import pytest


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

    def __str__(self):
        return self.name


def get_starship(name):
    fleet = pytest.importorskip("fleet")
    return fleet.get_ship(name)


@pytest.fixture(scope="module", params=range(2))
def prepenv(request):
    pass

@pytest.mark.dependency()
@pytest.mark.xfail(reason="deliberate fail")
def test_a():
    assert False

@pytest.mark.dependency()
def test_b():
    pass

@pytest.mark.dependency(depends=["test_a"])
def test_c():
    pass

@pytest.mark.dependency(depends=["test_b"])
def test_d():
    pass

@pytest.mark.dependency(depends=["test_b", "test_c"])
def test_e():
    pass


class TestClass(object):

    @pytest.mark.dependency()
    def test_a(self):
        pass

    @pytest.mark.dependency()
    @pytest.mark.xfail(reason="deliberate fail")
    def test_b(self):
        assert False

    @pytest.mark.dependency(depends=["test_b"])
    def test_c(self):
        pass


@pytest.mark.dependency()
@pytest.mark.parametrize("c", [ Color.RED, Color.GREEN, Color.BLUE, ])
def test_colors(c):
    pass

@pytest.mark.dependency(depends=["test_colors"])
def test_multicolored():
    pass

@pytest.mark.dependency(depends=["test_colors[Color.RED]"])
def test_alert():
    pass

@pytest.mark.dependency(depends=["test_f"])
def test_g():
    pass

@pytest.mark.dependency(name="h")
def test_h():
    pass

@pytest.mark.dependency(depends=["test_b"])
def test_k():
    s = get_starship("NCC-1701")

@pytest.mark.dependency()
def test_l(prepenv):
    pass

@pytest.mark.dependency(depends=["test_b"], scope='session')
def test_m():
    pass

@pytest.mark.dependency(depends=["test_h"])
def test_o():
    pass

@pytest.mark.dependency()
def test_p():
    pass

@pytest.mark.dependency(depends=["test_p"])
def test_q(prepenv):
    pass

@pytest.mark.dependency(depends=["test_a"])
@pytest.mark.dependency(name="r")
def test_r():
    pass

@pytest.mark.dependency(depends=["test_l"])
def test_s():
    pass
