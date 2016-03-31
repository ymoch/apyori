"""
Tests for apyori.dump_as_two_item_tsv.
"""

# For Python 2 compatibility.
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from os import linesep
from nose.tools import eq_

from apyori import RelationRecord
from apyori import OrderedStatistic
from apyori import dump_as_two_item_tsv


def test_normal():
    """
    Test for normal data.
    """
    test_data = RelationRecord(
        frozenset(['A', 'B']), 0.5, [
            OrderedStatistic(frozenset(), frozenset(['B']), 0.8, 1.2),
            OrderedStatistic(frozenset(['A']), frozenset(), 0.8, 1.2),
            OrderedStatistic(frozenset(['A']), frozenset(['B']), 0.8, 1.2),
        ]
    )
    output_file = StringIO()
    dump_as_two_item_tsv(test_data, output_file)

    output_file.seek(0)
    result = output_file.read()
    eq_(result, 'A\tB\t0.50000000\t0.80000000\t1.20000000' + linesep)
