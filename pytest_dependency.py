"""pytest-dependency - Manage dependencies of tests

This pytest plugin manages dependencies of tests.  It allows to mark
some tests as dependent from other tests.  These tests will then be
skipped if any of the dependencies did fail or has been skipped.
"""

import pytest

__version__   = "0.1"
