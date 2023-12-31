Installation instructions
=========================

See :ref:`install-using-pip` for the short version of the install
instructions.


System requirements
-------------------

+ Python 3.4 or newer.
+ `setuptools`_.
+ `pytest`_ 3.7.0 or newer.

Optional library packages
.........................

These packages are not needed to install or use pytest-dependency.
They are mostly only needed by the maintainer.

+ `git-props`_

  This package is used to extract some metadata such as the version
  number out of git, the version control system.  All releases embed
  that metadata in the distribution.  So this package is only needed
  to build out of the plain development source tree as cloned from
  GitHub, but not to build a release distribution.

+ `distutils-pytest`_ >= 0.2

  Only needed to run the test suite.


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


Installation
------------

.. _install-using-pip:

Installation using pip
......................

You can install pytest-dependency from the `Python Package Index
(PyPI)`__ using pip::

  $ pip install pytest-dependency

Note that while installing from PyPI is convenient, there is no way to
verify the integrity of the source distribution, which may be
considered a security risk.

.. __: `PyPI site`_

Manual installation from the source distribution
................................................

Release distributions are published on the GitHub.  Steps to manually
build from the source distribution:

1. Download the sources.

   The `Release Page`__ offers download of the source distribution
   ``pytest-dependency-X.X.tar.gz`` and a detached signature file
   ``pytest-dependency-X.X.tar.gz.asc``, where the "X.X" is to be
   replaced by the version number.

2. Check the signature (optional).

   You may verify the integrity of the source distribution by checking
   the signature::

     $ gpg --verify pytest-dependency-0.5.1.tar.gz.asc 
     gpg: assuming signed data in 'pytest-dependency-0.5.1.tar.gz'
     gpg: Signature made Fri Feb 14 21:58:30 2020 CET
     gpg:                using RSA key B4EB920861DF33F31B55A07C08A1264175343E6E
     gpg: Good signature from "Rolf Krahl <rolf@rotkraut.de>" [ultimate]
     gpg:                 aka "Rolf Krahl <rolf@uni-bremen.de>" [ultimate]
     gpg:                 aka "Rolf Krahl <Rolf.Krahl@gmx.net>" [ultimate]

   The signature should be made by the key
   :download:`0xB4EB920861DF33F31B55A07C08A1264175343E6E
   <08A1264175343E6E.pub>`.  The fingerprint of that key is::

     B4EB 9208 61DF 33F3 1B55  A07C 08A1 2641 7534 3E6E

3. Unpack and change into the source directory.

4. Build (optional)::

     $ python setup.py build

5. Test (optional)::

     $ python setup.py test

6. Install::

     $ python setup.py install

.. __: `GitHub latest release`_


.. _setuptools: http://pypi.python.org/pypi/setuptools/
.. _pytest: http://pytest.org/
.. _git-props: https://github.com/RKrahl/git-props
.. _distutils-pytest: https://github.com/RKrahl/distutils-pytest
.. _pytest-order: https://github.com/pytest-dev/pytest-order
.. _pytest-xdist: https://github.com/pytest-dev/pytest-xdist
.. _PyPI site: https://pypi.python.org/pypi/pytest_dependency/
.. _GitHub latest release: https://github.com/RKrahl/pytest-dependency/releases/latest
