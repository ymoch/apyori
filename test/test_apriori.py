"""
Tests for apyori.apriori.
"""

from nose.tools import eq_
from mock import Mock

from apyori import TransactionManager
from apyori import SupportRecord
from apyori import RelationRecord
from apyori import OrderedStatistic
from apyori import apriori


def test_empty():
    """
    Test for empty data.
    """
    transaction_manager = Mock(spec=TransactionManager)
    def gen_support_records(*args, **kwargs): # pylint: disable=unused-argument
        """ Mock for apyori.gen_support_records. """
        return iter([])

    def gen_ordered_statistics(*_):
        """ Mock for apyori.gen_ordered_statistics. """
        yield OrderedStatistic(
            frozenset(['A']), frozenset(['B']), 0.1, 0.7)

    result = list(apriori(
        transaction_manager,
        _gen_support_records=gen_support_records,
        _gen_ordered_statistics=gen_ordered_statistics,
    ))
    eq_(result, [])


def test_normal():
    """
    Test for normal data.
    """
    transaction_manager = Mock(spec=TransactionManager)
    min_support = 0.1
    max_length = 2
    support_record = SupportRecord(frozenset(['A', 'B']), 0.5)
    ordered_statistic1 = OrderedStatistic(
        frozenset(['A']), frozenset(['B']), 0.1, 0.7)
    ordered_statistic2 = OrderedStatistic(
        frozenset(['A']), frozenset(['B']), 0.3, 0.5)

    def gen_support_records(*args, **kwargs):
        """ Mock for apyori.gen_support_records. """
        eq_(args[1], min_support)
        eq_(kwargs['max_length'], max_length)
        yield support_record

    def gen_ordered_statistics(*_):
        """ Mock for apyori.gen_ordered_statistics. """
        yield ordered_statistic1
        yield ordered_statistic2

    # Will not create any records because of confidence.
    result = list(apriori(
        transaction_manager,
        min_support=min_support,
        min_confidence=0.4,
        max_length=max_length,
        _gen_support_records=gen_support_records,
        _gen_ordered_statistics=gen_ordered_statistics,
    ))
    eq_(result, [])

    # Will create a record.
    result = list(apriori(
        transaction_manager,
        min_support=min_support,
        min_confidence=0.3,
        max_length=max_length,
        _gen_support_records=gen_support_records,
        _gen_ordered_statistics=gen_ordered_statistics,
    ))
    eq_(result, [RelationRecord(
        support_record.items, support_record.support, [ordered_statistic2]
    )])
