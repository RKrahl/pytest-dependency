PYTHON   = python
BUILDDIR = $(CURDIR)/build


build:
	$(PYTHON) setup.py build

test: build
	PYTHONPATH=$(BUILDDIR)/lib $(PYTHON) -m pytest tests

sdist: .gitrevision
	$(PYTHON) setup.py sdist

doc-html:
	$(MAKE) -C doc html

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
	rm -rf .pytest_cache
	$(MAKE) -C doc distclean

.gitrevision:
	git describe --always --dirty > .gitrevision


.PHONY: build test sdist doc-html clean distclean .gitrevision
