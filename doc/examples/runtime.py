import pytest
from pytest_dependency import depends

@pytest.mark.dependency()
def test_a():
    pass

@pytest.mark.dependency()
@pytest.mark.xfail(reason="deliberate fail")
def test_b():
    assert False

@pytest.mark.dependency()
def test_c(request):
    depends(request, ["test_b"])
    pass

@pytest.mark.dependency()
def test_d(request):
    depends(request, ["test_a", "test_c"])
    pass
