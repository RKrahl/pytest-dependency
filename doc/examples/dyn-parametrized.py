import pytest

# Test data
# Consider a bunch of Nodes, some of them are parents and some are children.

class Node(object):
    NodeMap = {}
    def __init__(self, name, parent=None):
        self.name = name
        self.children = []
        self.NodeMap[self.name] = self
        if parent:
            self.parent = self.NodeMap[parent]
            self.parent.children.append(self)
        else:
            self.parent = None
    def __str__(self):
        return self.name

parents = [ Node("a"),  Node("b"),  Node("c"),  Node("d"), ]
childs =  [ Node("e", "a"), Node("f", "a"), Node("g", "a"), 
            Node("h", "b"), Node("i", "c"), Node("j", "c"), 
            Node("k", "d"), Node("l", "d"), Node("m", "d"), ]

# The test for the parent shall depend on the test of all its children.
# Create enriched parameter lists, decorated with the dependency marker.

childparam = [ 
    pytest.param(c, marks=pytest.mark.dependency(name="test_child[%s]" % c)) 
    for c in childs
]
parentparam = [
    pytest.param(p, marks=pytest.mark.dependency(
        name="test_parent[%s]" % p, 
        depends=["test_child[%s]" % c for c in p.children]
    )) for p in parents
]

@pytest.mark.parametrize("c", childparam)
def test_child(c):
    if c.name == "l":
        pytest.xfail("deliberate fail")
        assert False

@pytest.mark.parametrize("p", parentparam)
def test_parent(p):
    pass

