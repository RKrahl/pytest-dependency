PYTHON   = python3
BUILDLIB = $(CURDIR)/build/lib


build:
	$(PYTHON) -m build

test:
	$(PYTHON) -m pytest

sdist:
	$(PYTHON) -m build --sdist

doc-html: build
	$(MAKE) -C doc html PYTHONPATH=$(BUILDLIB)

clean:
	rm -rf build
	rm -rf __pycache__

distclean: clean
	rm -rf dist
	rm -rf tests/.pytest_cache
	$(MAKE) -C doc distclean


.PHONY: build test sdist doc-html clean distclean
