import pytest
from pytest_dependency import depends

@pytest.fixture(scope="module", params=range(1,10))
def testcase(request):
    param = request.param
    return param

@pytest.fixture(scope="module")
def dep_testcase(request, testcase):
    depends(request, ["test_a[%d]" % testcase])
    return testcase

@pytest.mark.dependency()
def test_a(testcase):
    if testcase % 7 == 0:
        pytest.xfail("deliberate fail")
        assert False

@pytest.mark.dependency()
def test_b(dep_testcase):
    pass

@pytest.mark.dependency()
def test_c(dep_testcase):
    pass
