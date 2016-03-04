"""
Tests for apyori.dump_as_json.
"""

import json

# For Python 2 compatibility.
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from nose.tools import raises
from nose.tools import eq_

from apyori import RelationRecord
from apyori import OrderedStatistic
from apyori import dump_as_json


def test_normal():
    """
    Test for normal data.
    """
    test_data = RelationRecord(
        frozenset(['A']), 0.5,
        [OrderedStatistic(frozenset([]), frozenset(['A']), 0.8, 1.2)]
    )
    output_file = StringIO()
    dump_as_json(test_data, output_file)

    output_file.seek(0)
    result = json.loads(output_file.read())
    eq_(result, {
        'items': ['A'],
        'support': 0.5,
        'ordered_statistics': [
            {
                'items_base': [],
                'items_add': ["A"],
                'confidence': 0.8,
                'lift': 1.2
            }
        ]
    })


@raises(TypeError)
def test_bad():
    """
    Test for bad data.
    """
    test_data = RelationRecord(
        set(['A']), 0.5,
        [OrderedStatistic(frozenset([]), frozenset(['A']), 0.8, 1.2)]
    )
    output_file = StringIO()
    dump_as_json(test_data, output_file)
