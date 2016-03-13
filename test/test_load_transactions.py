"""
Tests for apyori.load_transactions.
"""

# For Python 2 compatibility.
# pylint: disable=duplicate-code
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from nose.tools import eq_

from apyori import load_transactions


def test_empty():
    """
    Tests for empty data.
    """
    test_data = StringIO('')
    result = list(load_transactions(test_data))
    eq_(result, [])

def test_normal():
    """
    Tests for normal data.
    """
    test_data = StringIO(
        'A\tB\n' # Normal.
        '"C\t"\r\n' # Quote and Windows line feed code.
        'D\n' # Final line.
        '\n'  # Empty line.
    )
    result = list(load_transactions(test_data))
    eq_(result, [
        ['A', 'B'], # Normal.
        ['C\t'], # Contains tab.
        ['D'],
        # No records for empty lines.
    ])
