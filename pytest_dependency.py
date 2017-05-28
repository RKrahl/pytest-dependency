"""pytest-dependency - Manage dependencies of tests

This pytest plugin manages dependencies of tests.  It allows to mark
some tests as dependent from other tests.  These tests will then be
skipped if any of the dependencies did fail or has been skipped.
"""

import pytest

__version__   = "0.2"


class DependencyItemStatus(object):
    """Status of a test item in a dependency manager.
    """

    Phases = ('setup', 'call', 'teardown')

    def __init__(self):
        self.results = { w:None for w in self.Phases }

    def __str__(self):
        l = ["%s: %s" % (w, self.results[w]) for w in self.Phases]
        return "Status(%s)" % ", ".join(l)

    def addResult(self, rep):
        self.results[rep.when] = rep.outcome

    def isSuccess(self):
        return list(self.results.values()) == ['passed', 'passed', 'passed']


class DependencyManager(object):
    """Dependency manager, stores the results of tests.
    """

    ScopeCls = {'module':pytest.Module, 'session':pytest.Session}

    @classmethod
    def getManager(cls, item, scope='module'):
        """Get the DependencyManager object from the node at scope level.
        Create it, if not yet present.
        """
        node = item.getparent(cls.ScopeCls[scope])
        if not hasattr(node, 'dependencyManager'):
            node.dependencyManager = cls()
        return node.dependencyManager

    def __init__(self):
        self.results = {}

    def addResult(self, item, marker, rep):
        name = marker.kwargs.get('name')
        if not name:
            name = item.name
        status = self.results.setdefault(name, DependencyItemStatus())
        status.addResult(rep)

    def checkDepend(self, depends):
        for i in depends:
            if not(i in self.results and self.results[i].isSuccess()):
                pytest.skip("depends on %s" % i)


def depends(request, other):
    """Add dependency on other test.

    Call pytest.skip() unless a successful outcome of all of the tests in
    other has been registered previously.  This has the same effect as
    the `depends` keyword argument to the :func:`pytest.mark.dependency`
    marker.  In contrast to the marker, this function may be called at
    runtime during a test.

    :param request: the value of the `request` pytest fixture related
        to the current test.
    :param other: dependencies, a list of names of tests that this
        test depends on.
    :type other: iterable of :class:`str`
    """
    item = request.node
    manager = DependencyManager.getManager(item)
    manager.checkDepend(other)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Store the test outcome if this item is marked "dependency".
    """
    outcome = yield
    marker = item.get_marker("dependency")
    if marker is not None:
        rep = outcome.get_result()
        manager = DependencyManager.getManager(item)
        manager.addResult(item, marker, rep)


def pytest_runtest_setup(item):
    """Check dependencies if this item is marked "dependency".
    Skip if any of the dependencies has not been run successfully.
    """
    marker = item.get_marker("dependency")
    if marker is not None:
        depends = marker.kwargs.get('depends')
        if depends:
            manager = DependencyManager.getManager(item)
            manager.checkDepend(depends)
