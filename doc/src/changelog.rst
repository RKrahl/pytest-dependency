History of changes to pytest-dependency
=======================================

dev (not yet released)
    Bug fixes and minor changes
      + Issue #34: failing test with pytest 4.2.0 and newer.

0.4 (2018-12-02)
    Incompatible changes
      + Require pytest version 3.6.0 or newer.  This implicitly drops
	support for Python 2.6 and for Python 3.3 and older.

    Bug fixes and minor changes
      + Issue #24: get_marker no longer available in pytest 4.0.0.
	(Thanks to Rogdham for the PR.)
      + Issue #28: Applying markers directly in parametrize is no
	longer available in 4.0.

0.3.2 (2018-01-17)
    Bug fixes and minor changes
      + Issue #5: properly register the dependency marker.
      + Do not add the documentation to the source distribution.

0.3.1 (2017-12-26)
    Bug fixes and minor changes
      + Issue #17: Move the online documentation to Read the Docs
      + Some improvements in the documentation.

0.3 (2017-12-26)
    New features
      + Issue #7: Add a configuration switch to implicitly mark all
	tests.
      + Issue #10: Add an option to ignore unknown dependencies.

    Incompatible changes
      + Prepend the class name to the default test name for test class
	methods.  This fixes a potential name conflict, see Issue #6.

        If your code uses test classes and you reference test methods
        by their default name, you must add the class name.  E.g. if
        you have something like:

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

        If you override the test name in the pytest.mark.dependency()
        marker, nothing need to be changed.

    Bug fixes and minor changes
      + PR #11: show the name of the skipped test (thanks
        asteriogonzalez).
      + Issue #13: Do not import pytest in setup.py to make it
        compatible with pipenv.
      + Issue #15: tests fail with pytest 3.3.0.
      + Issue #8: document incompatibility with parallelization in
        pytest-xdist.
      + Clarify in the documentation that Python 3.1 is not officially
	supported because pytest 2.8 does not support it.  There is no
	known issue with Python 3.1 though.

0.2 (2017-05-28)
    New features
      + Issue #2: Add documentation.
      + Issue #4: Add a depend() function to add a dependency to a
        test at runtime.

0.1 (2017-01-29)
    + Initial release as an independent Python module.

      This code was first developed as part of a larger package,
      python-icat, at Helmholtz-Zentrum Berlin für Materialien und
      Energie, see
      https://icatproject.org/user-documentation/python-icat/
