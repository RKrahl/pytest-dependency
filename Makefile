PYTHON   = python
BUILDDIR = $(CURDIR)/build


build:
	$(PYTHON) setup.py build

test: build
	PYTHONPATH=$(BUILDDIR)/lib $(PYTHON) -m pytest tests

sdist: python2_6.patch .gitrevision doc-html
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
	rm -rf .cache tests/.cache
	rm -f MANIFEST
	rm -f *.pyc tests/*.pyc
	rm -rf __pycache__ tests/__pycache__
	rm -rf dist
	rm -rf pytest_dependency.egg-info
	rm -f python2_6.patch
	$(MAKE) -C doc distclean

.gitrevision:
	git describe --always --dirty > .gitrevision

python2_6.patch:
	git diff `git merge-base master python2_6` python2_6 > $@


.PHONY: build test sdist doc-html doc-pdf doc-dist clean distclean .gitrevision
