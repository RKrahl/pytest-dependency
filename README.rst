pytest-dependency - Manage dependencies of tests
================================================

This pytest plugin manages dependencies of tests.  It allows to mark
some tests as dependent from other tests.  These tests will then be
skipped if any of the dependencies did fail or has been skipped.


System requirements
-------------------

+ Python 2.6, 2.7, or 3.1 and newer.
+ `setuptools`_.
+ `pytest`_ 2.8.0 or newer.


Copyright and License
---------------------

- Copyright 2013-2015
  Helmholtz-Zentrum Berlin für Materialien und Energie GmbH
- Copyright 2016 Rolf Krahl

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
