#! /usr/bin/python
"""pytest-dependency - Manage dependencies of tests

This pytest plugin manages dependencies of tests.  It allows to mark
some tests as dependent from other tests.  These tests will then be
skipped if any of the dependencies did fail or has been skipped.
"""

import sys
if sys.version_info < (2, 7):
    raise RuntimeError("You are using Python %s.\n"
                       "Please apply python2_6.patch first." 
                       % sys.version.split()[0])
from setuptools import setup


setup(
    name='pytest-dependency',
    version='0.2',
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
        'Programming Language :: Python :: 3.1',
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
)
