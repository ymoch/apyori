"""
Tests for apyori.apriori.
"""

from nose.tools import eq_
from nose.tools import raises

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
    dummy_return = OrderedStatistic(
        frozenset(['A']), frozenset(['B']), 0.1, 0.7)
    def gen_support_records(*args, **kwargs): # pylint: disable=unused-argument
        """ Mock for apyori.gen_support_records. """
        return iter([])

    def gen_ordered_statistics(*_):
        """ Mock for apyori.gen_ordered_statistics. """
        yield dummy_return

    def filter_ordered_statistics(*_):
        """ Mock for apyori.gen_ordered_statistics. """
        yield dummy_return

    result = list(apriori(
        transaction_manager,
        _gen_support_records=gen_support_records,
        _gen_ordered_statistics=gen_ordered_statistics,
        _filter_ordered_statistics=filter_ordered_statistics,
    ))
    eq_(result, [])


def test_filtered():
    """
    Test for filtered data.
    """
    transaction_manager = Mock(spec=TransactionManager)
    dummy_return = OrderedStatistic(
        frozenset(['A']), frozenset(['B']), 0.1, 0.7)
    def gen_support_records(*args, **kwargs): # pylint: disable=unused-argument
        """ Mock for apyori.gen_support_records. """
        yield dummy_return

    def gen_ordered_statistics(*_):
        """ Mock for apyori.gen_ordered_statistics. """
        yield dummy_return

    def filter_ordered_statistics(*args, **kwargs): # pylint: disable=unused-argument
        """ Mock for apyori.gen_ordered_statistics. """
        return iter([])

    result = list(apriori(
        transaction_manager,
        _gen_support_records=gen_support_records,
        _gen_ordered_statistics=gen_ordered_statistics,
        _filter_ordered_statistics=filter_ordered_statistics,
    ))
    eq_(result, [])


def test_normal():
    """
    Test for normal data.
    """
    transaction_manager = Mock(spec=TransactionManager)
    min_support = 0.1
    min_confidence = 0.1
    min_lift = 0.5
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

    def filter_ordered_statistics(*args, **kwargs):
        """ Mock for apyori.gen_ordered_statistics. """
        eq_(kwargs['min_confidence'], min_confidence)
        eq_(kwargs['min_lift'], min_lift)
        eq_(len(list(args[0])), 2)
        yield ordered_statistic1

    result = list(apriori(
        transaction_manager,
        min_support=min_support,
        min_confidence=min_confidence,
        min_lift=min_lift,
        max_length=max_length,
        _gen_support_records=gen_support_records,
        _gen_ordered_statistics=gen_ordered_statistics,
        _filter_ordered_statistics=filter_ordered_statistics,
    ))
    eq_(result, [RelationRecord(
        support_record.items, support_record.support, [ordered_statistic1]
    )])


@raises(ValueError)
def test_invalid_support():
    """
    An invalid support.
    """
    transaction_manager = Mock(spec=TransactionManager)
    list(apriori(transaction_manager, min_support=0.0))
