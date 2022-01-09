Installation instructions
=========================

System requirements
-------------------

+ Python 2.7 or 3.4 and newer.
+ `setuptools`_.
+ `pytest`_ 3.7.0 or newer.


.. _install-other-packages:

Interaction with other packages
-------------------------------

`pytest-order`_
   pytest-dependency is based on the assumption that dependencies are
   run before the test that depends on them.  If this assumption is
   not satisfied in the default execution order in pytest, you may
   want to have a look on pytest-order.  It implements reordering of
   tests and supports taking the dependencies into account.

`pytest-xdist`_
   pytest-xdist features test run parallelization, e.g. distributing
   tests over separate processes that run in parallel.  This is based
   on the assumption that the tests can be run independent of each
   other.  Obviously, if you are using pytest-dependency, this
   assumption is not valid.  Thus, pytest-dependency will only work if
   you do not enable parallelization in pytest-xdist.


Download
--------

The latest release version of pytest-dependency is available on the
`Python Package Index (PyPI)`__.

.. __: https://pypi.python.org/pypi/pytest_dependency/


Installation
------------

1. Download the sources, unpack, and change into the source directory.

2. Build (optional)::

     $ python setup.py build

3. Test (optional)::

     $ python -m pytest tests

4. Install::

     $ python setup.py install

The last step might require admin privileges in order to write into
the site-packages directory of your Python installation.

For production use, it is always recommended to use the latest release
version from PyPI, see above.


.. _setuptools: http://pypi.python.org/pypi/setuptools/
.. _pytest: http://pytest.org/
.. _pytest-order: https://github.com/pytest-dev/pytest-order
.. _pytest-xdist: https://github.com/pytest-dev/pytest-xdist
