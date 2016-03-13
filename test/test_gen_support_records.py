"""
Tests for apyori.create_next_candidates.
"""

from nose.tools import eq_
from mock import Mock

from apyori import SupportRecord
from apyori import TransactionManager
from apyori import gen_support_records


def test_empty():
    """
    Test for gen_supports_record.
    """
    transaction_manager = Mock(spec=TransactionManager)
    transaction_manager.initial_candidates.return_value = []
    support_records_gen = gen_support_records(transaction_manager, 0.1)
    support_records = list(support_records_gen)
    eq_(support_records, [])


def test_infinite():
    """
    Test for gen_supports_record with no limits.
    """
    transaction_manager = Mock(spec=TransactionManager)
    transaction_manager.initial_candidates.return_value = [
        frozenset(['A']), frozenset(['B']), frozenset(['C'])]
    transaction_manager.calc_support.side_effect = lambda key: {
        frozenset(['A']): 0.8,
        frozenset(['B']): 0.6,
        frozenset(['C']): 0.3,
        frozenset(['A', 'B']): 0.3,
        frozenset(['A', 'C']): 0.2,
    }.get(key, 0.0)
    candidates = {
        2: [
            frozenset(['A', 'B']),
            frozenset(['A', 'C']),
            frozenset(['B', 'C'])
        ],
        3: [
            frozenset(['A', 'B', 'C']),
        ],
    }
    support_records_gen = gen_support_records(
        transaction_manager, 0.3,
        _create_next_candidates=lambda _, length: candidates.get(length))

    support_records = list(support_records_gen)
    eq_(support_records, [
        SupportRecord(frozenset(['A']), 0.8),
        SupportRecord(frozenset(['B']), 0.6),
        SupportRecord(frozenset(['C']), 0.3),
        SupportRecord(frozenset(['A', 'B']), 0.3),
    ])


def test_length():
    """
    Test for gen_supports_record that limits the length.
    """
    transaction_manager = Mock(spec=TransactionManager)
    transaction_manager.initial_candidates.return_value = [
        frozenset(['A']), frozenset(['B']), frozenset(['C'])]
    transaction_manager.calc_support.side_effect = lambda key: {
        frozenset(['A']): 0.7,
        frozenset(['B']): 0.5,
        frozenset(['C']): 0.2,
        frozenset(['A', 'B']): 0.2,
        frozenset(['A', 'C']): 0.1,
    }.get(key, 0.0)
    candidates = {
        2: [
            frozenset(['A', 'B']),
            frozenset(['A', 'C']),
            frozenset(['B', 'C'])
        ],
    }
    support_records_gen = gen_support_records(
        transaction_manager, 0.05, max_length=1,
        _create_next_candidates=lambda _, length: candidates.get(length))

    support_records = list(support_records_gen)
    eq_(support_records, [
        SupportRecord(frozenset(['A']), 0.7),
        SupportRecord(frozenset(['B']), 0.5),
        SupportRecord(frozenset(['C']), 0.2),
    ])
