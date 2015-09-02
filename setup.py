#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from harvest import __version__ as version

setup(
    name='harvest',
    version=version,
    description='Grow linguistic data on trees',
    author='Luke Maurits',
    author_email='luke@maurits.id.au',
    license="BSD (2 clause)",
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: BSD License',
    ],
    packages=['harvest', 'harvest/models'],
    scripts=['bin/harvest',],
    requires=['dendropy', 'scipy'],
    install_requires=['dendropy','scipy']
)
