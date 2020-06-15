"""$DOC"""

import logging

import pytest


__version__ = "$VERSION"

logger = logging.getLogger(__name__)

_automark = False
_ignore_unknown = False


def _get_bool(value):
    """
    Evaluate string representation of a boolean value.
    """
    if value:
        if value.lower() in ("0", "no", "n", "false", "f", "off"):
            return False
        elif value.lower() in ("1", "yes", "y", "true", "t", "on"):
            return True
        else:
            raise ValueError("Invalid truth value '%s'" % value)
    else:
        return False


def _remove_parametrization(item, scope):
    # Old versions of pytest used to add an extra "::()" to
    # the node ids of class methods to denote the class
    # instance.  This has been removed in pytest 4.0.0.
    nodeid = item.nodeid.replace("::()::", "::")
    if scope == "session" or scope == "package":
        name = nodeid
    elif scope == "module":
        name = nodeid.split("::", 1)[1]
    elif scope == "class":
        name = nodeid.split("::", 2)[2]
    else:
        raise RuntimeError(
            "Internal error: invalid scope '%s'" % scope
        )

    original = item.originalname if item.originalname is not None else item.name
    # remove the parametrization part at the end
    if not name.endswith(original):
        index = name.rindex(original) + len(original)
        name = name[:index]
    return name


class DependencyItemStatus(object):
    """
    Status of a test item in a dependency manager.
    """

    phases = ("setup", "call", "teardown")

    def __init__(self):
        self.results = {w: None for w in self.phases}

    def __str__(self):
        return "Status(%s)" % ", ".join(
            "%s: %s" % (w, self.results[w]) for w in self.phases
        )

    def add_result(self, rep):
        self.results[rep.when] = rep.outcome

    def is_success(self):
        return all(v == "passed" for v in self.results.values())

    def is_done(self):
        return None not in self.results.values()


class DependencyManager(object):
    """
    Dependency manager, stores the results of tests.
    """

    scope_cls = {
        "session": pytest.Session,
        "package": pytest.Package,
        "module": pytest.Module,
        "class": pytest.Class,
    }

    @classmethod
    def get_manager(cls, item, scope):
        """
        Get the DependencyManager object from the node at scope level.
        Create it, if not yet present.
        """
        node = item.getparent(cls.scope_cls[scope])
        if not node:
            return None
        if not hasattr(node, "dependency_manager"):
            node.dependency_manager = cls(scope)
        return node.dependency_manager

    def __init__(self, scope):
        self.scope = scope
        self.results = {}
        self.dependencies = {}

    def register_dependency(self, name, index):
        self.dependencies[name] = index

    def add_result(self, item, name, rep):
        if not name:
            name = _remove_parametrization(item, self.scope)

        # check if we failed - if so, return without adding the result
        if name not in self.results:
            self.results[name] = DependencyItemStatus()
        status = self.results[name]
        if status.is_done() and not status.is_success():
            return

        # add the result
        logger.debug(
            "register %s %s %s in %s scope",
            rep.when, name, rep.outcome, self.scope
        )
        status.add_result(rep)

    @classmethod
    def add_all_scopes(cls, item, name, rep):
        for scope in cls.scope_cls:
            manager = cls.get_manager(item, scope=scope)
            if manager is not None:
                manager.add_result(item, name, rep)

    def check_depends(self, depends, item):
        logger.debug(
            "check dependencies of %s in %s scope ...",
            item.name, self.scope
        )
        for i in depends:
            if i in self.results:
                if self.results[i].is_success():
                    logger.debug("... %s succeeded", i)
                    continue
                else:
                    logger.debug("... %s has not succeeded", i)
            else:
                logger.debug("... %s is unknown", i)
                if _ignore_unknown:
                    continue
            logger.info("skip %s because it depends on %s", item.name, i)
            pytest.skip("%s depends on %s" % (item.name, i))

    def reorder(self, depends, item, name, index):
        for dep in depends:
            di = self.dependencies.get(dep)
            if di is None:
                item.warn(pytest.PytestWarning(
                    "Dependency '%s' of '%s' doesn't exist, "
                    "or has incorrect scope!" % (dep, name)
                ))
                continue
            # change the index for the current item so that it'll execute
            # after the dependency
            if di > index:
                self.dependencies[name] = index = di + 1
        return self.dependencies[name]


def depends(request, other, scope="module"):
    """
    Add dependency on other test.

    Call pytest.skip() unless a successful outcome of all of the tests in
    other has been registered previously.  This has the same effect as
    the `depends` keyword argument to the :func:`pytest.mark.dependency`
    marker.  In contrast to the marker, this function may be called at
    runtime during a test.

    :param request: the value of the `request` pytest fixture related
        to the current test.
    :param other: dependencies, a list of names of tests that this
        test depends on.  The names of the dependencies must be
        adapted to the scope.
    :type other: iterable of :class:`str`
    :param scope: the scope to search for the dependencies.  Must be
        either `'session'`, `'package'`, `'module'`, or `'class'`.
    :type scope: :class:`str`

    .. versionadded:: 0.2

    .. versionchanged:: 0.5.0
        the scope parameter has been added.
    """
    item = request.node
    manager = DependencyManager.get_manager(item, scope=scope)
    manager.check_depends(other, item)


def pytest_addoption(parser):
    parser.addini(
        "automark_dependency",
        "Add the dependency marker to all tests automatically",
        default=False,
    )
    parser.addoption(
        "--ignore-unknown-dependency",
        action="store_true", default=False,
        help="ignore dependencies whose outcome is not known",
    )


def pytest_configure(config):
    global _automark, _ignore_unknown
    _automark = _get_bool(config.getini("automark_dependency"))
    _ignore_unknown = config.getoption("--ignore-unknown-dependency")
    config.addinivalue_line(
        "markers",
        "dependency(name=None, depends=[]): "
        "mark a test to be used as a dependency for "
        "other tests or to depend on other tests."
    )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Store the test outcome if this item is marked "dependency".
    """
    outcome = yield
    marker = item.get_closest_marker("dependency")
    if marker is not None or _automark:
        rep = outcome.get_result()
        name = marker.kwargs.get("name") if marker is not None else None
        DependencyManager.add_all_scopes(item, name, rep)


def pytest_runtest_setup(item):
    """
    Check dependencies if this item is marked "dependency".
    Skip if any of the dependencies has not been run successfully.
    """
    marker = item.get_closest_marker("dependency")
    if marker is not None:
        depends = marker.kwargs.get("depends")
        if depends:
            scope = marker.kwargs.get("scope", "module")
            manager = DependencyManager.get_manager(item, scope=scope)
            manager.check_depends(depends, item)


# special hook to make pytest-dependency support reordering based on deps
def pytest_collection_modifyitems(items):
    # register items and their names, according to scopes
    for i, item in enumerate(items):
        for marker in item.iter_markers("dependency"):
            depends = marker.kwargs.get("depends", [])
            scope = marker.kwargs.get("scope", "module")
            name = marker.kwargs.get("name")
            if not name:
                name = _remove_parametrization(item, scope)
            manager = DependencyManager.get_manager(item, scope)
            if manager is None:
                continue
            manager.register_dependency(name, i)
    # prepare a dictionary of final, highest indexes
    highest_indexes = {}
    # change stored indexes so that they point at
    # 'index + 1' of the furthest / latest dependency
    for i, item in enumerate(items):
        # this keeps track of the highest index between different markers
        highest_index = i
        for marker in item.iter_markers("dependency"):
            depends = marker.kwargs.get("depends", [])
            scope = marker.kwargs.get("scope", "module")
            name = marker.kwargs.get("name")
            if not name:
                name = _remove_parametrization(item, scope)
            manager = DependencyManager.get_manager(item, scope)
            if manager is None:
                continue
            highest_index = max(
                highest_index, manager.reorder(depends, item, name, i)
            )
        highest_indexes[item] = highest_index
    # sort the results - this ensures a stable sort too
    items.sort(key=lambda i: highest_indexes[i])
