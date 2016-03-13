"""
Tests for apyori.main.
"""

# For Python 2 compatibility.
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from collections import namedtuple
from nose.tools import eq_

from apyori import main


def test_normal():
    """
    Test for normal data.
    """
    delimiter = 'x'
    inputs = ['AxB', 'AxC']
    input_files = [StringIO(inputs[0]), StringIO(inputs[1])]
    input_transactions = [['A', 'B'], ['A', 'C']]
    def load_transactions_mock(input_file, **kwargs):
        """ Mock for apyori.load_transactions. """
        eq_(kwargs['delimiter'], delimiter)
        eq_(next(input_file), inputs[0])
        yield iter(input_transactions[0])
        eq_(next(input_file), inputs[1])
        yield iter(input_transactions[1])

    max_length = 2
    min_support = 0.5
    min_confidence = 0.2
    apriori_results = ['123', '456']
    def apriori_mock(transactions, **kwargs):
        """ Mock for apyori.apriori. """
        eq_(list(next(transactions)), input_transactions[0])
        eq_(list(next(transactions)), input_transactions[1])
        eq_(kwargs['max_length'], max_length)
        eq_(kwargs['min_support'], min_support)
        eq_(kwargs['min_confidence'], min_confidence)
        for result in apriori_results:
            yield result

    def output_func_mock(record, output_file):
        """ Mock for apyori.output_func. """
        output_file.write(record)

    args = namedtuple(
        'ArgumentMock', [
            'input',
            'delimiter',
            'max_length',
            'min_support',
            'min_confidence',
            'output',
            'output_func'
        ]
    )(
        input=input_files, delimiter=delimiter,
        max_length=max_length, min_support=min_support,
        min_confidence=min_confidence, output=StringIO(),
        output_func=output_func_mock
    )
    main(
        _parse_args=lambda _: args,
        _load_transactions=load_transactions_mock,
        _apriori=apriori_mock)
    args.output.seek(0)
    eq_(args.output.read(), ''.join(apriori_results))
