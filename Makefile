PYTHON   = python3
BUILDLIB = $(CURDIR)/build/lib


build:
	$(PYTHON) setup.py build

test: build
	PYTHONPATH=$(BUILDLIB) $(PYTHON) -m pytest tests

sdist:
	$(PYTHON) setup.py sdist

doc-html: build
	$(MAKE) -C doc html PYTHONPATH=$(BUILDLIB)

clean:
	rm -f *~ tests/*~
	rm -rf build

distclean: clean
	rm -f MANIFEST _meta.py
	rm -rf .cache tests/.cache .pytest_cache tests/.pytest_cache
	rm -f *.pyc tests/*.pyc
	rm -rf __pycache__ tests/__pycache__
	rm -rf dist
	rm -rf pytest_dependency.egg-info
	$(MAKE) -C doc distclean

meta:
	$(PYTHON) setup.py meta


.PHONY: build test sdist doc-html clean distclean meta
