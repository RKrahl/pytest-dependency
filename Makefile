PYTHON   = python
BUILDDIR = $(CURDIR)/build


build:
	$(PYTHON) setup.py build

test: build
	cd tests; env PYTHONPATH=$(BUILDDIR)/lib $(PYTHON) -m pytest

sdist: doc-html
	$(PYTHON) setup.py sdist

doc-html:
	$(MAKE) -C doc html

doc-pdf:
	$(MAKE) -C doc latexpdf

doc-dist: doc-html
	mkdir -p dist
	cd doc/html; zip -r ../../dist/doc.zip *


clean:
	rm -f *~ tests/*~
	rm -rf build
	$(MAKE) -C doc clean

distclean: clean
	rm -rf .cache
	rm -f MANIFEST
	rm -f *.pyc
	rm -rf __pycache__ tests/__pycache__
	rm -rf dist
	rm -rf pytest_dependency.egg-info
	$(MAKE) -C doc distclean


.PHONY: build test sdist doc-html doc-pdf clean distclean
