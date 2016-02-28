#!/usr/bin/env python

"""
Setting up program for Apyori.
"""

import apyori
import setuptools

setuptools.setup(
    name='apyori',
    description='Simple Apriori algorithm Implementation.',
    version=apyori.__version__,
    author=apyori.__author__,
    author_email=apyori.__author__,
    py_modules=['apyori'],
    test_suite='nose.collector',
    tests_require=['nose', 'mock'],
    entry_points={
        'console_scripts': [
            'apyori-run = apyori:main',
        ],
    },
)
