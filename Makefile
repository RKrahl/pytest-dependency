PYTHON   = python
BUILDDIR = $(CURDIR)/build


build:
	$(PYTHON) setup.py build

test: build
	PYTHONPATH=$(BUILDDIR)/lib $(PYTHON) -m pytest tests

sdist:
	$(PYTHON) setup.py sdist

doc-html: .version
	$(MAKE) -C doc html

clean:
	rm -f *~ tests/*~
	rm -rf build
	$(MAKE) -C doc clean

distclean: clean
	rm -rf .cache tests/.cache .pytest_cache tests/.pytest_cache
	rm -f *.pyc tests/*.pyc
	rm -rf __pycache__ tests/__pycache__
	rm -f MANIFEST .version
	rm -rf dist
	rm -rf pytest_dependency.egg-info
	$(MAKE) -C doc distclean

.version:
	$(PYTHON) setup.py check

.PHONY: build test sdist doc-html clean distclean
