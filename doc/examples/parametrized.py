import pytest

@pytest.mark.parametrize("x,y", [
    pytest.mark.dependency(name="a1")((0,0)),
    pytest.mark.dependency(name="a2")(pytest.mark.xfail((0,1))),
    pytest.mark.dependency(name="a3")((1,0)),
    pytest.mark.dependency(name="a4")((1,1))
])
def test_a(x,y):
    assert y <= x

@pytest.mark.parametrize("u,v", [
    pytest.mark.dependency(name="b1", depends=["a1", "a2"])((1,2)),
    pytest.mark.dependency(name="b2", depends=["a1", "a3"])((1,3)),
    pytest.mark.dependency(name="b3", depends=["a1", "a4"])((1,4)),
    pytest.mark.dependency(name="b4", depends=["a2", "a3"])((2,3)),
    pytest.mark.dependency(name="b5", depends=["a2", "a4"])((2,4)),
    pytest.mark.dependency(name="b6", depends=["a3", "a4"])((3,4))
])
def test_b(u,v):
    pass

@pytest.mark.parametrize("w", [
    pytest.mark.dependency(name="c1", depends=["b1", "b2", "b6"])(1),
    pytest.mark.dependency(name="c2", depends=["b2", "b3", "b6"])(2),
    pytest.mark.dependency(name="c3", depends=["b2", "b4", "b6"])(3)
])
def test_c(w):
    pass
