Installation instructions
=========================

System requirements
-------------------

+ Python 2.6, 2.7, or 3.1 and newer.
  Python 2.6 requires patching the sources, see below.
+ `setuptools`_.
+ `pytest`_ 2.8.0 or newer.


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

     $ python -m pytest

4. Install::

     $ python setup.py install

The last step might require admin privileges in order to write into
the site-packages directory of your Python installation.

If you are using Python 2.6, apply python2_6.patch after the first
step:

1a. Patch::

     $ patch -p1 < python2_6.patch

It removes the use of certain language features (dict comprehensions)
that were introduced in Python 2.7.

For production use, it is always recommended to use the latest release
version from PyPI, see above.  If you build from the development
sources that can be found at GitHub, please note that python2_6.patch
is generated dynamically and not in the source repository.


.. _setuptools: http://pypi.python.org/pypi/setuptools/
.. _pytest: http://pytest.org/
