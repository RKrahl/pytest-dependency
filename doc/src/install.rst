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

pytest-xdist
   pytest-xdist features test run parallelization, e.g. distributing
   tests over separate processes that run in parallel.  This is based
   on the assumption that the tests can be run independent of each
   other.  Obviously, if you are using pytest-dependency, this
   assumption is not valid.  Thus, pytest-dependency will only work if
   you do not enable parallelization in pytest-xdist.


Download
--------

The latest release version of pytest-dependency source can be found at
PyPI, see

    https://pypi.python.org/pypi/pytest_dependency


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
