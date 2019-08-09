"""$DOC"""

__version__ = "$VERSION"
__revision__ = "$REVISION"

import pytest

_automark = False
_ignore_unknown = False


def _get_bool(value):
    """Evaluate string representation of a boolean value.
    """
    if value:
        if value.lower() in ["0", "no", "n", "false", "f", "off"]:
            return False
        elif value.lower() in ["1", "yes", "y", "true", "t", "on"]:
            return True
        else:
            raise ValueError("Invalid truth value '%s'" % value)
    else:
        return False


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

    ScopeCls = {'class':pytest.Class, 'module':pytest.Module, 'session':pytest.Session}

    @classmethod
    def getManager(cls, item, scope='module'):
        """Get the DependencyManager object from the node at scope level.
        Create it, if not yet present.
        """
        node = item.getparent(cls.ScopeCls[scope])
        if not node:
            return None
        if not hasattr(node, 'dependencyManager'):
            node.dependencyManager = cls(scope)
        return node.dependencyManager

    def __init__(self, scope):
        self.results = {}
        self.scope = scope

    def addResult(self, item, name, rep):
        if not name:
            if self.scope == "session":
                name = item.nodeid.replace("::()::", "::")
            elif item.cls and self.scope == "module":
                name = "%s::%s" % (item.cls.__name__, item.name)
            else:
                name = item.name
        status = self.results.setdefault(name, DependencyItemStatus())
        status.addResult(rep)

    def checkDepend(self, depends, item):
        if depends == "all":
            for key in self.results:
                if not self.results[key].isSuccess():
                    pytest.skip("%s depends on all previous tests passing (%s failed)" % (item.name, key))
        else:
            for i in depends:
                if i in self.results:
                    if self.results[i].isSuccess():
                        continue
                else:
                    if _ignore_unknown:
                        continue
                pytest.skip("%s depends on %s" % (item.name, i))


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

    .. versionadded:: 0.2
    """
    item = request.node
    manager = DependencyManager.getManager(item)
    manager.checkDepend(other, item)


def pytest_addoption(parser):
    parser.addini("automark_dependency", 
                  "Add the dependency marker to all tests automatically", 
                  default=False)
    parser.addoption("--ignore-unknown-dependency", 
                     action="store_true", default=False, 
                     help="ignore dependencies whose outcome is not known")


def pytest_configure(config):
    global _automark, _ignore_unknown
    _automark = _get_bool(config.getini("automark_dependency"))
    _ignore_unknown = config.getoption("--ignore-unknown-dependency")
    config.addinivalue_line("markers", 
                            "dependency(name=None, depends=[]): "
                            "mark a test to be used as a dependency for "
                            "other tests or to depend on other tests.")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Store the test outcome if this item is marked "dependency".
    """
    outcome = yield
    marker = item.get_closest_marker("dependency")
    if marker is not None or _automark:
        rep = outcome.get_result()
        name = marker.kwargs.get('name') if marker is not None else None
        """ Store the test outcome for each scope if it exists"""
        for scope in DependencyManager.ScopeCls:
            manager = DependencyManager.getManager(item, scope=scope)
            if(manager):
                manager.addResult(item, name, rep)


def pytest_runtest_setup(item):
    """Check dependencies if this item is marked "dependency".
    Skip if any of the dependencies has not been run successfully.
    """
    marker = item.get_closest_marker("dependency")
    if marker is not None:
        depends = marker.kwargs.get('depends')
        if depends:
            scope = marker.kwargs.get('scope', 'module') if marker is not None else 'module'
            manager = DependencyManager.getManager(item, scope=scope)
            manager.checkDepend(depends, item)
