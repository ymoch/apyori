Apyori
======

[![Build Status](https://travis-ci.org/ymoch/apyori.svg?branch=master)](https://travis-ci.org/ymoch/apyori)
[![Coverage Status](https://coveralls.io/repos/github/ymoch/apyori/badge.svg?branch=master)](https://coveralls.io/github/ymoch/apyori?branch=master)

A simple implementation of *Apriori algorithm* by Python.


Features
--------

- Consisted of only one file and able to be used portably.
- Can be used as APIs.
- Supports a TSV output format for 2-items relations.


Installation
------------

- run ```python setup.py install```.


Execution
---------

- Run with ```python apyori.py``` command.
- If installed, you can also run with ```apyori-run``` command.


API Usage
---------

Here is a basic example.

```python
from apyori import apriori

transactions = [
    ['beer', 'nuts'],
    ['beer', 'cheese'],
]
results = list(apriori(transactions))
```

For more details, see *apyori.apriori* pydoc.
