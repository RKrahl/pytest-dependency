SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = pytest-dependency
SOURCEDIR     = src
BUILDDIR      = .
BUILDERS      = html dirhtml singlehtml htmlhelp qthelp devhelp epub	\
		latex latexpdf man texinfo text gettext linkcheck xml	\
		json pickle

# Subdirectories of the source directory that are supposed to be there
# but that may be empty and may thus be missing after a git checkout.
STATIC_SOURCEDIRS = $(SOURCEDIR)/_static $(SOURCEDIR)/_templates


help:
	$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

$(BUILDERS): $(STATIC_SOURCEDIRS)
	$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

distclean:
	rm -rf doctrees $(BUILDERS)

$(STATIC_SOURCEDIRS):
	mkdir $@

.PHONY: help distclean $(BUILDERS)
