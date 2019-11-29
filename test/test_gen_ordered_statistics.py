"""
Tests for apyori.gen_ordered_statistics.
"""

from mock import Mock
from nose.tools import eq_

from apyori import SupportRecord
from apyori import OrderedStatistic
from apyori import TransactionManager
from apyori import gen_ordered_statistics


def test_normal():
    """
    Test for normal data.
    """
    transaction_manager = Mock(spec=TransactionManager)
    transaction_manager.calc_support.side_effect = lambda key: {
        frozenset([]): 1.0,
        frozenset(['A']): 0.8,
        frozenset(['B']): 0.4,
        frozenset(['C']): 0.2,
        frozenset(['A', 'B']): 0.2,
        frozenset(['A', 'C']): 0.1,
        frozenset(['B', 'C']): 0.01,
        frozenset(['A', 'B', 'C']): 0.001,
    }.get(key, 0.0)

    test_data = SupportRecord(frozenset(['A', 'B', 'C']), 0.001)
    results = list(gen_ordered_statistics(transaction_manager, test_data))
    eq_(results, [
        OrderedStatistic(
            frozenset([]),
            frozenset(['A', 'B', 'C']),
            0.001 / 1.0,
            0.001 / 1.0 / 0.001,
        ),
        OrderedStatistic(
            frozenset(['A']),
            frozenset(['B', 'C']),
            0.001 / 0.8,
            0.001 / 0.8 / 0.01,
        ),
        OrderedStatistic(
            frozenset(['B']),
            frozenset(['A', 'C']),
            0.001 / 0.4,
            0.001 / 0.4 / 0.1,
        ),
        OrderedStatistic(
            frozenset(['C']),
            frozenset(['A', 'B']),
            0.001 / 0.2,
            0.001 / 0.2 / 0.2,
        ),
        OrderedStatistic(
            frozenset(['A', 'B']),
            frozenset(['C']),
            0.001 / 0.2,
            0.001 / 0.2 / 0.2,
        ),
        OrderedStatistic(
            frozenset(['A', 'C']),
            frozenset(['B']),
            0.001 / 0.1,
            0.001 / 0.1 / 0.4,
        ),
        OrderedStatistic(
            frozenset(['B', 'C']),
            frozenset(['A']),
            0.001 / 0.01,
            0.001 / 0.01 / 0.8,
        ),
    ])
