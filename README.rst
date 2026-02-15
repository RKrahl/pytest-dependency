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

This module is a plugin for the popular Python testing framework
`pytest`_.  It manages dependencies of tests: you may mark some tests
as dependent from other tests.  These tests will then be skipped if
any of the dependencies did fail or has been skipped.

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
- Copyright 2016–2026 Rolf Krahl

Licensed under the `Apache License`_, Version 2.0 (the "License"); you
may not use this package except in compliance with the License.

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied.  See the License for the specific language governing
permissions and limitations under the License.


.. _pytest: https://pytest.org/
.. _Read the Docs site: https://pytest-dependency.readthedocs.io/
.. _Apache License: https://www.apache.org/licenses/LICENSE-2.0
