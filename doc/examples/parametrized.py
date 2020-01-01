import pytest

@pytest.mark.parametrize("x,y", [
    pytest.param(0, 0, marks=pytest.mark.dependency(name="a1")),
    pytest.param(0, 1, marks=[pytest.mark.dependency(name="a2"),
                              pytest.mark.xfail]),
    pytest.param(1, 0, marks=pytest.mark.dependency(name="a3")),
    pytest.param(1, 1, marks=pytest.mark.dependency(name="a4"))
])
def test_a(x,y):
    assert y <= x

@pytest.mark.parametrize("u,v", [
    pytest.param(1, 2, marks=pytest.mark.dependency(name="b1", 
                                                    depends=["a1", "a2"])),
    pytest.param(1, 3, marks=pytest.mark.dependency(name="b2", 
                                                    depends=["a1", "a3"])),
    pytest.param(1, 4, marks=pytest.mark.dependency(name="b3", 
                                                    depends=["a1", "a4"])),
    pytest.param(2, 3, marks=pytest.mark.dependency(name="b4", 
                                                    depends=["a2", "a3"])),
    pytest.param(2, 4, marks=pytest.mark.dependency(name="b5", 
                                                    depends=["a2", "a4"])),
    pytest.param(3, 4, marks=pytest.mark.dependency(name="b6", 
                                                    depends=["a3", "a4"]))
])
def test_b(u,v):
    pass

@pytest.mark.parametrize("w", [
    pytest.param(1, marks=pytest.mark.dependency(name="c1", 
                                                 depends=["b1", "b2", "b6"])),
    pytest.param(2, marks=pytest.mark.dependency(name="c2", 
                                                 depends=["b2", "b3", "b6"])),
    pytest.param(3, marks=pytest.mark.dependency(name="c3", 
                                                 depends=["b2", "b4", "b6"]))
])
def test_c(w):
    pass
