"""
Tests for apyori.TransactionManager.
"""

from apyori import TransactionManager
from nose.tools import eq_


def test_empty():
    """
    Test for a empty transaction.
    """
    transactions = []
    manager = TransactionManager(transactions)

    eq_(manager.num_transaction, 0)
    eq_(manager.items, [])
    eq_(manager.initial_candidates(), [])
    eq_(manager.calc_support([]), 1.0)
    eq_(manager.calc_support(['hoge']), 0.0)


def test_normal():
    """
    Test for a normal transaction.
    """
    transactions = [
        ['beer', 'nuts'],
        ['beer', 'cheese'],
    ]
    manager = TransactionManager(transactions)

    eq_(manager.num_transaction, len(transactions))
    eq_(manager.calc_support(['beer']), 1.0)
    eq_(manager.calc_support(['nuts']), 0.5)
    eq_(manager.calc_support(['butter']), 0.0)
    eq_(manager.calc_support(['beer', 'nuts']), 0.5)
    eq_(manager.calc_support(['beer', 'nuts', 'cheese']), 0.0)

    # Convert into frozenset to ignore orders.
    eq_(frozenset(manager.items), frozenset(['beer', 'nuts', 'cheese']))
    eq_(
        frozenset(manager.initial_candidates()),
        frozenset([
            frozenset(['beer']), frozenset(['nuts']), frozenset(['cheese'])
        ])
    )

def test_create():
    """
    Test for the factory method.
    """
    transactions = []
    manager1 = TransactionManager.create(transactions)
    manager2 = TransactionManager.create(manager1)
    eq_(manager1, manager2)
