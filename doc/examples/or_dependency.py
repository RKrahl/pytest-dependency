import pytest
from pytest_dependency import depends

def depends_or(request, other, scope='module'):
    item = request.node
    for o in other:
        try:
            depends(request, [o], scope)
        except pytest.skip.Exception:
            continue
        else:
            return
    pytest.skip("%s depends on any of %s" % (item.name, ", ".join(other)))


@pytest.mark.dependency()
def test_ap():
    pass

@pytest.mark.dependency()
@pytest.mark.xfail(reason="deliberate fail")
def test_ax():
    assert False

@pytest.mark.dependency()
def test_bp():
    pass

@pytest.mark.dependency()
@pytest.mark.xfail(reason="deliberate fail")
def test_bx():
    assert False

@pytest.mark.dependency()
def test_c(request):
    depends_or(request, ["test_ax", "test_bx"])
    pass

@pytest.mark.dependency()
def test_d(request):
    depends_or(request, ["test_ax", "test_bp"])
    pass

@pytest.mark.dependency()
def test_e(request):
    depends_or(request, ["test_ap", "test_bx"])
    pass

@pytest.mark.dependency()
def test_f(request):
    depends_or(request, ["test_ap", "test_bp"])
    pass
