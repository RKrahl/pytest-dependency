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
	rm -rf .cache tests/.cache .pytest_cache tests/.pytest_cache
	rm -f *.pyc tests/*.pyc
	rm -rf __pycache__ tests/__pycache__
	rm -f MANIFEST .version
	rm -rf dist
	rm -rf pytest_dependency.egg-info
	$(MAKE) -C doc distclean

.PHONY: build test sdist doc-html clean distclean
