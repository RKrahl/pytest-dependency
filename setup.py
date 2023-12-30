"""pytest-dependency - Manage dependencies of tests

This pytest plugin manages dependencies of tests.  It allows to mark
some tests as dependent from other tests.  These tests will then be
skipped if any of the dependencies did fail or has been skipped.
"""

import setuptools
from setuptools import setup
import setuptools.command.build_py
import distutils.command.sdist
import distutils.file_util
from distutils import log
import os
from pathlib import Path
from stat import ST_ATIME, ST_MTIME, ST_MODE, S_IMODE
import string
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
        log.warn("warning: cannot determine version number")
        version = "UNKNOWN"

docstring = __doc__

class copy_file_mixin:
    """Distutils copy_file() mixin.

    Inject a custom version version of the copy_file() method that
    does some substitutions on the fly into distutils command class
    hierarchy.
    """
    Subst_srcs = {"src/pytest_dependency.py"}
    Subst = {'DOC': docstring, 'VERSION': version}
    def copy_file(self, infile, outfile,
                  preserve_mode=1, preserve_times=1, link=None, level=1):
        if infile in self.Subst_srcs:
            infile = Path(infile)
            outfile = Path(outfile)
            if outfile.name == infile.name:
                log.info("copying (with substitutions) %s -> %s",
                         infile, outfile.parent)
            else:
                log.info("copying (with substitutions) %s -> %s",
                         infile, outfile)
            if not self.dry_run:
                st = infile.stat()
                try:
                    outfile.unlink()
                except FileNotFoundError:
                    pass
                with infile.open("rt") as sf, outfile.open("wt") as df:
                    df.write(string.Template(sf.read()).substitute(self.Subst))
                if preserve_times:
                    os.utime(str(outfile), (st[ST_ATIME], st[ST_MTIME]))
                if preserve_mode:
                    outfile.chmod(S_IMODE(st[ST_MODE]))
            return (str(outfile), 1)
        else:
            return distutils.file_util.copy_file(infile, outfile,
                                                 preserve_mode, preserve_times,
                                                 not self.force, link,
                                                 dry_run=self.dry_run)

# Note: Do not use setuptools for making the source distribution,
# rather use the good old distutils instead.
# Rationale: https://rhodesmill.org/brandon/2009/eby-magic/
class sdist(copy_file_mixin, distutils.command.sdist.sdist):
    pass

class build_py(copy_file_mixin, setuptools.command.build_py.build_py):
    pass

with Path("README.rst").open("rt", encoding="utf8") as f:
    readme = f.read()

setup(
    name = "pytest-dependency",
    version = version,
    description = "Manage dependencies of tests",
    long_description = readme,
    long_description_content_type = "text/x-rst",
    url = "https://github.com/RKrahl/pytest-dependency",
    author = "Rolf Krahl",
    author_email = "rolf@rotkraut.de",
    license = "Apache-2.0",
    classifiers = [
        "Development Status :: 4 - Beta",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Testing",
    ],
    project_urls = dict(
        Documentation="https://pytest-dependency.readthedocs.io/",
        Source="https://github.com/RKrahl/pytest-dependency",
        Download="https://github.com/RKrahl/pytest-dependency/releases/latest",
    ),
    package_dir = {"": "src"},
    python_requires = ">=3.4",
    py_modules = ["pytest_dependency"],
    install_requires = ["setuptools", "pytest >= 3.7.0"],
    entry_points = {
        "pytest11": [
            "dependency = pytest_dependency",
        ],
    },
    cmdclass = {'build_py': build_py, 'sdist': sdist},
)
