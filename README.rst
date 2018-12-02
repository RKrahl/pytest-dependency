.. image:: https://travis-ci.org/RKrahl/pytest-dependency.svg?branch=master
   :target: https://travis-ci.org/RKrahl/pytest-dependency

pytest-dependency - Manage dependencies of tests
================================================

This pytest plugin manages dependencies of tests.  It allows to mark
some tests as dependent from other tests.  These tests will then be
skipped if any of the dependencies did fail or has been skipped.


Download
--------

The latest release version can be found at PyPI, see

    https://pypi.python.org/pypi/pytest_dependency


System requirements
-------------------

+ Python 2.7 or 3.4 and newer.
+ `setuptools`_.
+ `pytest`_ 3.6.0 or newer.


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


Documentation
-------------

The documentation can be found at

    https://pytest-dependency.readthedocs.io/

The example test modules used in the documentation can be found in
doc/examples in the source distribution.


Copyright and License
---------------------

- Copyright 2013-2015
  Helmholtz-Zentrum Berlin für Materialien und Energie GmbH
- Copyright 2016-2018 Rolf Krahl

Licensed under the Apache License, Version 2.0 (the "License"); you
may not use this file except in compliance with the License.  You may
obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied.  See the License for the specific language governing
permissions and limitations under the License.


.. _setuptools: http://pypi.python.org/pypi/setuptools/
.. _pytest: http://pytest.org/
