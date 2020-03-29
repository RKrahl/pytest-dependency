About pytest-dependency
=======================

This module is a plugin for the popular Python testing framework
`pytest`_.  It manages dependencies of tests: you may mark some tests
as dependent from other tests.  These tests will then be skipped if
any of the dependencies did fail or has been skipped.


What is the purpose?
--------------------

In the theory of good test design, tests should be self-contained and
independent.  Each test should cover one single issue, either verify
that one single feature is working or that one single bug is fixed.
Tests should be designed to work in any order independent of each
other.

So far the theory.  The practice is often more complicated then that.
Sometimes, the principle of independency of tests is simply
unrealistic or impractical.  Program features often depend on each
other.  If some feature B depends on another feature A in such a way
that B cannot work without A, then it may simply be pointless to run
the test for B unless the test for A has succeeded.  Another case may
be if the subject of the tests has an internal state that unavoidably
is influenced by the tests.  In this situation it may happen that test
A, as a side effect, sets the system in some state that is the
precondition to be able to run test B.  Again, in this case it would
be pointless to try running test B unless test A has been run
successful.

It should be emphasized however that the principle of independency of
tests is still valid.  Before using pytest-dependency, it is still
advisable to reconsider your test design and to avoid dependencies of
tests whenever possible, rather then to manage these dependencies.


How does it work?
-----------------

The pytest-dependency module defines a marker that can be applied to
tests.  The marker accepts an argument that allows to list the
dependencies of the test.  Both tests, the dependency and the
dependent test should be decorated with the marker.  Behind the
scenes, the marker arranges for the result of the test to be recorded
internally.  If a list of dependencies has been given as argument, the
marker verifies that a successful outcome of all the dependencies has
been registered previously and causes a skip of the test if this was
not the case.


Why is this useful?
-------------------

The benefit of skipping dependent tests is the same as for skipping
tests in general: it avoids cluttering the test report with useless
and misleading failure reports from tests that have been known
beforehand not to work in this particular case.

If tests depend on each other in such a way that test B cannot work
unless test A has been run successfully, a failure of test A will
likely result in failure messages from both tests.  But the failure
message from test B will not be helpful in any way.  It will only
distract the user from the real issue that is the failure of test A.
Skipping test B in this case will help the user to concentrate on
those results that really matter.


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


.. _pytest: http://pytest.org/
