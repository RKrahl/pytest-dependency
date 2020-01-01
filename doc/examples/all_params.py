import pytest

def instances(name, params):
    def vstr(val):
        if isinstance(val, (list, tuple)):
            return "-".join([str(v) for v in val])
        else:
            return str(val)
    return ["%s[%s]" % (name, vstr(v)) for v in params]


params_a = range(17)

@pytest.mark.parametrize("x", params_a)
@pytest.mark.dependency()
def test_a(x):
    if x == 13:
        pytest.xfail("deliberate fail")
        assert False
    else:
        pass

@pytest.mark.dependency(depends=instances("test_a", params_a))
def test_b():
    pass

params_c = list(zip(range(0,8,2), range(2,6)))

@pytest.mark.parametrize("x,y", params_c)
@pytest.mark.dependency()
def test_c(x, y):
    if x > y:
        pytest.xfail("deliberate fail")
        assert False
    else:
        pass

@pytest.mark.dependency(depends=instances("test_c", params_c))
def test_d():
    pass

params_e = ['abc', 'def']

@pytest.mark.parametrize("s", params_e)
@pytest.mark.dependency()
def test_e(s):
    if 'e' in s:
        pytest.xfail("deliberate fail")
        assert False
    else:
        pass

@pytest.mark.dependency(depends=instances("test_e", params_e))
def test_f():
    pass
