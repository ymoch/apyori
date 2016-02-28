#!/usr/bin/env python

import setuptools

setuptools.setup(
    name='apyori',
    version='0.1.0',
    description='Simple Apriori algorithm Implementation.',
    author='ymoch',
    author_email='ymoch@github.com',
    py_modules=['apyori'],
    test_suite='nose.collector',
    tests_require=['nose', 'mock'],
    entry_points={
        'console_scripts': [
            'apyori-run = apyori:main',
        ],
    },
)
