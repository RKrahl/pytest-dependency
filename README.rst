|gh-test| |rtd| |pypi|

.. |gh-test| image:: https://github.com/RKrahl/pytest-dependency/actions/workflows/run-tests.yaml/badge.svg
   :target: https://github.com/RKrahl/pytest-dependency/actions/workflows/run-tests.yaml
   :alt: GitHub Workflow Status
	 
.. |rtd| image:: https://img.shields.io/readthedocs/pytest-dependency/latest
   :target: https://pytest-dependency.readthedocs.io/en/latest/
   :alt: Documentation build status

.. |pypi| image:: https://img.shields.io/pypi/v/pytest-dependency
   :target: https://pypi.org/project/pytest-dependency/
   :alt: PyPI version

pytest-dependency – Manage dependencies of tests
================================================

This pytest plugin manages dependencies of tests.  It allows to mark
some tests as dependent from other tests.  These tests will then be
skipped if any of the dependencies did fail or has been skipped.


Download
--------

The latest release version can be found `at PyPI`__.

.. __: `PyPI site`_


System requirements
-------------------

+ Python 2.7 or 3.4 and newer.
+ `setuptools`_.
+ `pytest`_ 3.7.0 or newer.

Optional library packages:

+ `setuptools_scm`_

  The version number is managed using this package.  All source
  distributions add a static text file with the version number and
  fall back using that if `setuptools_scm` is not available.  So this
  package is only needed to build out of the plain development source
  tree as cloned from GitHub.


Installation
------------

1. Download the sources, unpack, and change into the source directory.

2. Build (optional)::

     $ python setup.py build

3. Test (optional)::

     $ PYTHONPATH=build/lib python -m pytest tests

4. Install::

     $ python setup.py install

The last step might require admin privileges in order to write into
the site-packages directory of your Python installation.


Documentation
-------------

See the `online documentation`__.

The example test modules used in the documentation can be found in
doc/examples in the source distribution.

.. __: `Read the Docs site`_


Copyright and License
---------------------

- Copyright 2013–2015
  Helmholtz-Zentrum Berlin für Materialien und Energie GmbH
- Copyright 2016–2020 Rolf Krahl

Licensed under the Apache License, Version 2.0 (the "License"); you
may not use this file except in compliance with the License.  You may
obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied.  See the License for the specific language governing
permissions and limitations under the License.


.. _PyPI site: https://pypi.org/project/pytest-dependency/
.. _setuptools: http://pypi.python.org/pypi/setuptools/
.. _pytest: http://pytest.org/
.. _setuptools_scm: https://github.com/pypa/setuptools_scm/
.. _Read the Docs site: https://pytest-dependency.readthedocs.io/
