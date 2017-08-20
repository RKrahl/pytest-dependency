# Makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
PAPER         = a4

# Internal variables.
PAPEROPT_a4     = -D latex_paper_size=a4
PAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS   = -d doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) src

# Subdirectories of src that are supposed to be there but that may be
# empty and may thus be missing after a git checkout.
SRCDIRS = src/_static src/_templates


html: $(SRCDIRS)
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) html

latex: $(SRCDIRS)
	$(SPHINXBUILD) -b latex $(ALLSPHINXOPTS) latex

latexpdf: latex
	$(MAKE) -C latex all-pdf

linkcheck: $(SRCDIRS)
	$(SPHINXBUILD) -b linkcheck $(ALLSPHINXOPTS) linkcheck

doctest: $(SRCDIRS)
	$(SPHINXBUILD) -b doctest $(ALLSPHINXOPTS) doctest

clean:
	rm -f *~ examples/*~ src/*~

distclean: clean
	rm -rf doctrees html latex linkcheck doctest
	rm -f examples/*.pyc
	rm -rf examples/__pycache__

src/_static:
	mkdir $@

src/_templates:
	mkdir $@

.PHONY: html latex latexpdf linkcheck doctest clean distclean
