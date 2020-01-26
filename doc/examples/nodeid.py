import random
import pytest

def test_a():
    pass

@pytest.mark.parametrize("i,b", [
    (7, True),
    (0, False),
    pytest.param(-1, False, marks=pytest.mark.xfail(reason="nonsense"))
])
def test_b(i, b):
    assert bool(i) == b

ordered = list(range(10))
unordered = random.sample(ordered, k=len(ordered))

class TestClass:

    def test_c(self):
        pass

    @pytest.mark.parametrize("l,ll", [(ordered, 10), (unordered, 10)],
                             ids=["order", "disorder"])
    def test_d(self, l, ll):
        assert len(l) == ll
