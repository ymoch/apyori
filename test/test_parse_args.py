"""
Tests for apyori.parse_args.
"""

from nose.tools import raises

from apyori import parse_args


def test_normal():
    """
    Normal arguments.
    """
    argv = []
    args = parse_args(argv)


@raises(ValueError)
def test_invalid_support():
    """
    An invalid support.
    """
    argv = ['-s', '0']
    args = parse_args(argv)
