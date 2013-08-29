#!/usr/bin/env python


import os

from ner import __version__

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open(os.path.join(os.path.dirname(__file__), 'README.md')) as fp:
    description = fp.read()

specs = {
    'name' : 'ner',
    'version' : __version__,
    'description' : 'Python client for the Stanford Named Entity Recognizer',
    'long_description' : description,
    'url' : 'http://github.com/dat/pyner',
    'author' : 'Dat Hoang',
    'author_email' : 'dat.hoang@gmail.com',
    'keywords' : ['ner', 'stanford named entity recognizer', 'stanford named entity tagger'],
    'license' : 'BSD',
    'packages' : ['ner'],
    'test_suite' : 'tests.all_tests',
    'classifiers' : (
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ),
}

if __name__=='__main__':
    setup(**specs)

