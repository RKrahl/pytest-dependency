#! /usr/bin/python
"""pytest-dependency - Manage dependencies of tests

This pytest plugin manages dependencies of tests.  It allows to mark
some tests as dependent from other tests.  These tests will then be
skipped if any of the dependencies did fail or has been skipped.
"""

import distutils.log
import os
import os.path
import re
import string
from setuptools import setup
import setuptools.command.sdist as st_sdist
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


class sdist(st_sdist.sdist):
    def make_release_tree(self, base_dir, files):
        st_sdist.sdist.make_release_tree(self, base_dir, files)
        if not self.dry_run:
            src = "pytest_dependency.py"
            dest = os.path.join(base_dir, src)
            if hasattr(os, 'link') and os.path.exists(dest):
                os.unlink(dest)
            subst = {'DOC': __doc__, 'VERSION': version}
            with open(src, "rt") as sf, open(dest, "wt") as df:
                df.write(string.Template(sf.read()).substitute(subst))


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
    long_description=__doc__,
    project_urls={
        'Documentation': 'https://pytest-dependency.readthedocs.io/',
        'Source Code': 'https://github.com/RKrahl/pytest-dependency',
    },
    py_modules=['pytest_dependency'],
    install_requires=['pytest >= 3.6.0'],
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
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
    ],
    entry_points={
        'pytest11': [
            'dependency = pytest_dependency',
        ],
    },
    cmdclass = {'sdist': sdist},
)
