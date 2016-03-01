"""
Tests for apyori.create_next_candidates.
"""

from nose.tools import eq_

from apyori import create_next_candidates


def test_2elem():
    """
    Test for create_next_candidates with 2 elements.
    """
    test_data = [
        frozenset(['A']),
        frozenset(['B']),
        frozenset(['C'])
    ]

    # Convert into frozenset to ignore orders.
    result = frozenset(create_next_candidates(test_data, 2))
    eq_(result, frozenset([
        frozenset(['A', 'B']),
        frozenset(['A', 'C']),
        frozenset(['B', 'C']),
    ]))


def test_3elem():
    """
    Test for create_next_candidates with 3 elements.
    """
    test_data = [
        frozenset(['A', 'B']),
        frozenset(['B', 'C']),
        frozenset(['A', 'C']),
        frozenset(['D', 'E']),
        frozenset(['D', 'F']),
    ]

    # Convert into frozenset to ignore orders.
    result = frozenset(create_next_candidates(test_data, 3))
    eq_(result, frozenset([frozenset(['A', 'B', 'C'])]))
