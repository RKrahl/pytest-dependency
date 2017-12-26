#! /usr/bin/python
"""pytest-dependency - Manage dependencies of tests

This pytest plugin manages dependencies of tests.  It allows to mark
some tests as dependent from other tests.  These tests will then be
skipped if any of the dependencies did fail or has been skipped.
"""

__version__ = "0.3"

import sys
if sys.version_info < (2, 7):
    raise RuntimeError("You are using Python %s.\n"
                       "Please apply python2_6.patch first." 
                       % sys.version.split()[0])
import os
import os.path
import re
from setuptools import setup
import setuptools.command.sdist as st_sdist


def _filter_file(src, dest, subst):
    """Copy src to dest doing substitutions on the fly.
    """
    substre = re.compile(r'\$(%s)' % '|'.join(subst.keys()))
    def repl(m):
        return subst[m.group(1)]
    with open(src, "rt") as sf, open(dest, "wt") as df:
        while True:
            l = sf.readline()
            if not l:
                break
            df.write(re.sub(substre, repl, l))

class sdist(st_sdist.sdist):
    def make_release_tree(self, base_dir, files):
        st_sdist.sdist.make_release_tree(self, base_dir, files)
        if not self.dry_run:
            src = "pytest_dependency.py"
            dest = os.path.join(base_dir, src)
            gitrevfile = ".gitrevision"
            if hasattr(os, 'link') and os.path.exists(dest):
                os.unlink(dest)
            subst = {'DOC': __doc__, 'VERSION': __version__}
            if os.path.exists(gitrevfile):
                with open(gitrevfile, "rt") as f:
                    subst['REVISION'] = f.readline().strip()
            _filter_file(src, dest, subst)


setup(
    name='pytest-dependency',
    version=__version__,
    description='Manage dependencies of tests',
    author='Rolf Krahl',
    author_email='rolf@rotkraut.de',
    maintainer='Rolf Krahl',
    maintainer_email='rolf@rotkraut.de',
    url='https://github.com/RKrahl/pytest-dependency',
    license='Apache Software License 2.0',
    long_description=__doc__,
    py_modules=['pytest_dependency'],
    install_requires=['pytest >= 2.8.0'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
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
