"""
Tests for apyori.filter_ordered_statistics.
"""

from nose.tools import eq_

from apyori import OrderedStatistic
from apyori import filter_ordered_statistics


TEST_DATA = [
    OrderedStatistic(frozenset(['A']), frozenset(['B']), 0.1, 0.7),
    OrderedStatistic(frozenset(['A']), frozenset(['B']), 0.3, 0.5),
]


def test_normal():
    """
    Test for normal data.
    """
    result = list(filter_ordered_statistics(
        TEST_DATA, min_confidence=0.1, min_lift=0.5))
    eq_(result, TEST_DATA)


def test_min_confidence():
    """
    Filter by minimum confidence.
    """
    result = list(filter_ordered_statistics(
        TEST_DATA, min_confidence=0.2, min_lift=0.1))
    eq_(result, [TEST_DATA[1]])


def test_min_lift():
    """
    Filter by minimum lift.
    """
    result = list(filter_ordered_statistics(
        TEST_DATA, min_confidence=0.0, min_lift=0.6))
    eq_(result, [TEST_DATA[0]])
