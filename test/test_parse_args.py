"""
Tests for apyori.parse_args.
"""

from apyori import parse_args


def test_normal():
    """
    Normal arguments.
    """
    argv = []
    parse_args(argv)
