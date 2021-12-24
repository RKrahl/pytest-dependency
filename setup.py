#! /usr/bin/python
"""pytest-dependency - Manage dependencies of tests

This pytest plugin manages dependencies of tests.  It allows to mark
some tests as dependent from other tests.  These tests will then be
skipped if any of the dependencies did fail or has been skipped.
"""

import os
import os.path
import re
import stat
import string
import setuptools
from distutils.cmd import Command as du_cmd
import distutils.command.sdist
import distutils.log
from setuptools import setup
import setuptools.command.build_py
try:
    import setuptools_scm
    version = setuptools_scm.get_version()
    with open(".version", "wt") as f:
        f.write(version)
except (ImportError, LookupError):
    try:
        with open(".version", "rt") as f:
            version = f.read()
    except (OSError, IOError):
        distutils.log.warn("warning: cannot determine version number")
        version = "UNKNOWN"

doc_string = __doc__

class copy_file_mixin:
    """Distutils copy_file() mixin.

    Inject a custom version version of the copy_file() method that
    does some substitutions on the fly into distutils command class
    hierarchy.
    """
    Subst_srcs = {"src/pytest_dependency.py"}
    Subst = {'DOC': doc_string, 'VERSION': version}
    def copy_file(self, infile, outfile, preserve_mode=1, preserve_times=1,
                  link=None, level=1):
        if infile in self.Subst_srcs:
            fstat = os.stat(infile)
            if os.path.basename(outfile) == os.path.basename(infile):
                distutils.log.info("copying (with substitutions) %s -> %s",
                                   infile, os.path.dirname(outfile))
            else:
                distutils.log.info("copying (with substitutions) %s -> %s",
                                   infile, outfile)
            if not self.dry_run:
                if os.path.exists(outfile):
                    os.unlink(outfile)
                with open(infile, "rt") as sf, open(outfile, "wt") as df:
                    df.write(string.Template(sf.read()).substitute(self.Subst))
                if preserve_mode:
                    os.chmod(outfile, stat.S_IMODE(fstat[stat.ST_MODE]))
            return (outfile, 1)
        else:
            # Note: can't use super() with Python 2.
            return du_cmd.copy_file(self, infile, outfile,
                                    preserve_mode=preserve_mode,
                                    preserve_times=preserve_times,
                                    link=link, level=level)

class build_py(copy_file_mixin, setuptools.command.build_py.build_py):
    pass

# Note: Do not use setuptools for making the source distribution,
# rather use the good old distutils instead.
# Rationale: https://rhodesmill.org/brandon/2009/eby-magic/
class sdist(copy_file_mixin, distutils.command.sdist.sdist):
    pass

setup(
    name='pytest-dependency',
    version=version,
    description='Manage dependencies of tests',
    author='Rolf Krahl',
    author_email='rolf@rotkraut.de',
    maintainer='Rolf Krahl',
    maintainer_email='rolf@rotkraut.de',
    url='https://github.com/RKrahl/pytest-dependency',
    license='Apache Software License 2.0',
    long_description=doc_string,
    project_urls={
        'Documentation': 'https://pytest-dependency.readthedocs.io/',
        'Source Code': 'https://github.com/RKrahl/pytest-dependency',
    },
    package_dir = {'': 'src'},
    py_modules=['pytest_dependency'],
    install_requires=['pytest >= 3.7.0'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
    ],
    entry_points={
        'pytest11': [
            'dependency = pytest_dependency',
        ],
    },
    cmdclass = {'build_py': build_py, 'sdist': sdist},
)
