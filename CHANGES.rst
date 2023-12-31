Changelog
=========

0.6.0 (2023-12-31)
~~~~~~~~~~~~~~~~~~

Documentation
-------------

+ `#39`_, `#41`_, `#59`_: Review documentation

Incompatible changes
--------------------

+ Drop support for Python 2.

Bug fixes and minor changes
---------------------------

+ `#40`_: add logging.
+ `#50`_, `#51`_: test suite incompatibility with pytest 6.2.0.
+ `#58`_: declare the type of automark_dependency ini-option correctly
  as bool.

Internal
--------

+ `#75`_: review build tool chain.

.. _#39: https://github.com/RKrahl/pytest-dependency/issues/39
.. _#40: https://github.com/RKrahl/pytest-dependency/issues/40
.. _#41: https://github.com/RKrahl/pytest-dependency/issues/41
.. _#50: https://github.com/RKrahl/pytest-dependency/issues/50
.. _#51: https://github.com/RKrahl/pytest-dependency/pull/51
.. _#58: https://github.com/RKrahl/pytest-dependency/pull/58
.. _#59: https://github.com/RKrahl/pytest-dependency/pull/59
.. _#75: https://github.com/RKrahl/pytest-dependency/pull/75

0.5.1 (2020-02-14)
~~~~~~~~~~~~~~~~~~

Bug fixes and minor changes
---------------------------

+ Fix failing documentation build.

0.5.0 (2020-02-14)
~~~~~~~~~~~~~~~~~~

New features
------------

+ `#3`_, `#35`_: add a scope to dependencies.
  (Thanks to JoeSc and selenareneephillips!)

Incompatible changes
--------------------

+ Require pytest version 3.7.0 or newer.

Bug fixes and minor changes
---------------------------

+ `#34`_: failing test with pytest 4.2.0 and newer.

+ Use setuptools_scm to manage the version number.

.. _#35: https://github.com/RKrahl/pytest-dependency/pull/35
.. _#34: https://github.com/RKrahl/pytest-dependency/issues/34
.. _#3: https://github.com/RKrahl/pytest-dependency/issues/3

0.4.0 (2018-12-02)
~~~~~~~~~~~~~~~~~~

Incompatible changes
--------------------

+ Require pytest version 3.6.0 or newer.  This implicitly drops
  support for Python 2.6 and for Python 3.3 and older.

Bug fixes and minor changes
---------------------------

+ `#24`_, `#25`_: get_marker no longer available in pytest 4.0.0.
  (Thanks to Rogdham!)

+ `#28`_: Applying markers directly in parametrize is no longer
  available in 4.0.

.. _#28: https://github.com/RKrahl/pytest-dependency/issues/28
.. _#25: https://github.com/RKrahl/pytest-dependency/pull/25
.. _#24: https://github.com/RKrahl/pytest-dependency/issues/24

0.3.2 (2018-01-17)
~~~~~~~~~~~~~~~~~~

Bug fixes and minor changes
---------------------------

+ `#5`_: properly register the dependency marker.

+ Do not add the documentation to the source distribution.

.. _#5: https://github.com/RKrahl/pytest-dependency/issues/5

0.3.1 (2017-12-26)
~~~~~~~~~~~~~~~~~~

Bug fixes and minor changes
---------------------------

+ `#17`_: Move the online documentation to Read the Docs.

+ Some improvements in the documentation.

.. _#17: https://github.com/RKrahl/pytest-dependency/issues/17

0.3 (2017-12-26)
~~~~~~~~~~~~~~~~

New features
------------

+ `#7`_: Add a configuration switch to implicitly mark all tests.

+ `#10`_: Add an option to ignore unknown dependencies.

Incompatible changes
--------------------

+ Prepend the class name to the default test name for test class
  methods.  This fixes a potential name conflict, see `#6`_.

  If your code uses test classes and you reference test methods by
  their default name, you must add the class name.  E.g. if you have
  something like:

  .. code-block:: python

    class TestClass(object):

        @pytest.mark.dependency()
        def test_a():
            pass

        @pytest.mark.dependency(depends=["test_a"])
        def test_b():
            pass

  you need to change this to:

  .. code-block:: python

    class TestClass(object):

        @pytest.mark.dependency()
        def test_a():
            pass

        @pytest.mark.dependency(depends=["TestClass::test_a"])
        def test_b():
            pass

  If you override the test name in the :func:`pytest.mark.dependency`
  marker, nothing need to be changed.

Bug fixes and minor changes
---------------------------

+ `#11`_: show the name of the skipped test.
  (Thanks asteriogonzalez!)

+ `#13`_: Do not import pytest in setup.py to make it compatible with
  pipenv.

+ `#15`_: tests fail with pytest 3.3.0.

+ `#8`_: document incompatibility with parallelization in
  pytest-xdist.

+ Clarify in the documentation that Python 3.1 is not officially
  supported because pytest 2.8 does not support it.  There is no known
  issue with Python 3.1 though.

.. _#15: https://github.com/RKrahl/pytest-dependency/issues/15
.. _#13: https://github.com/RKrahl/pytest-dependency/issues/13
.. _#11: https://github.com/RKrahl/pytest-dependency/pull/11
.. _#10: https://github.com/RKrahl/pytest-dependency/issues/10
.. _#8: https://github.com/RKrahl/pytest-dependency/issues/8
.. _#7: https://github.com/RKrahl/pytest-dependency/issues/7
.. _#6: https://github.com/RKrahl/pytest-dependency/issues/6

0.2 (2017-05-28)
~~~~~~~~~~~~~~~~

New features
------------

+ `#2`_: Add documentation.

+ `#4`_: Add a depend() function to add a dependency to a test at
  runtime.

.. _#4: https://github.com/RKrahl/pytest-dependency/issues/4
.. _#2: https://github.com/RKrahl/pytest-dependency/issues/2

0.1 (2017-01-29)
~~~~~~~~~~~~~~~~

+ Initial release as an independent Python module.

  This code was first developed as part of a larger package,
  `python-icat`_, at Helmholtz-Zentrum Berlin für Materialien und
  Energie.

.. _python-icat: https://github.com/icatproject/python-icat
