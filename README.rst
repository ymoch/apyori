Apyori
======

*Apyori* is a simple implementation of
Apriori algorithm with Python 2.7 and 3.3 - 3.5,
provided as APIs and as commandline interfaces.

.. image:: https://travis-ci.org/ymoch/apyori.svg?branch=master
    :target: https://travis-ci.org/ymoch/apyori
.. image:: https://coveralls.io/repos/github/ymoch/apyori/badge.svg?branch=master
    :target: https://coveralls.io/github/ymoch/apyori?branch=master


Module Features
---------------

- Consisted of only one file and depends on no other libraries,
  which enable you to use it portably.
- Able to used as APIs.

Application Features
--------------------

- Supports a JSON output format.
- Supports a TSV output format for 2-items relations.


Installation
------------

Choose one from the following.

- Put *apyori.py* into your project.
- Run :code:`python setup.py install`.


API Usage
---------

Here is a basic example:

.. code-block:: python

    from apyori import apriori

    transactions = [
        ['beer', 'nuts'],
        ['beer', 'cheese'],
    ]
    results = list(apriori(transactions))

For more details, see *apyori.apriori* pydoc.


CLI Usage
---------

First, prepare input data as tab-separated transactions.

- Each item is separated with a tab.
- Each transactions is separated with a line feed code.

Second, run the application.
Input data is given as a standard input or file paths.

- Run with :code:`python apyori.py` command.
- If installed, you can also run with :code:`apyori-run` command.

For more details, use '-h' option.


-------
Samples
-------

Basic usage
***********

.. code-block:: shell

    apyori-run < data/integration_test_input_1.tsv


Use TSV output
**************

.. code-block:: shell

    apyori-run -f tsv < data/integration_test_input_1.tsv

Fields of output mean:

- Base item.
- Appended item.
- Support.
- Confidence.
- Lift.


Specify the minimum support
***************************

.. code-block:: shell

    apyori-run -s 0.5 < data/integration_test_input_1.tsv


Specify the minimum confidence
******************************

.. code-block:: shell

    apyori-run -c 0.5 < data/integration_test_input_1.tsv
