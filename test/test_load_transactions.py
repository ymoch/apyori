"""
Tests for apyori.load_transactions.
"""

# For Python 2 compatibility.
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from nose.tools import eq_

from apyori import load_transactions


def test_empty_data():
    """
    Tests for empty data.
    """
    test_data = StringIO('')
    result = list(load_transactions(test_data))
    eq_(result, [])


def test_empty_string():
    """
    Tests for empty string.
    """
    test_data = StringIO(
        '\n'  # Empty line.
        'A\t\tB\n' # Empty string middle.
        'C\t\n' # Empty string last.
    )
    result = list(load_transactions(test_data))
    eq_(result, [
        [''],
        ['A', '', 'B'],
        ['C', ''],
    ])


def test_normal():
    """
    Tests for normal data.
    """
    test_data = StringIO(
        'A\tB\n' # Normal.
        '"C\t"\r\n' # Quote and Windows line feed code.
        'D' # Final line without line separator.
    )
    result = list(load_transactions(test_data))
    eq_(result, [
        ['A', 'B'], # Normal.
        ['C\t'], # Contains tab.
        ['D'],
    ])
