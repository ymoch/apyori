#!/usr/bin/env python

"""
Implementation of Apriori algorithm.
"""

import sys
import argparse
import functools
from collections import namedtuple
from itertools import combinations


__version__ = '0.1.0'
__author__ = 'ymoch'
__author_email__ = 'ymoch@githib.com'


# Ignore name errors because these names are namedtuples.
SupportRecord = namedtuple( # pylint: disable=C0103
    'SupportRecord', ('items', 'support'))
RelationRecord = namedtuple( # pylint: disable=C0103
    'RelationRecord', SupportRecord._fields + ('ordered_statistics',))
OrderedStatistic = namedtuple( # pylint: disable=C0103
    'OrderedStatistic', ('items_base', 'items_add', 'confidence', 'lift',))


class TransactionManager(object):
    """
    Transaction manager class.
    """

    def __init__(self, transactions):
        """
        Initialize.

        @param  transactions    A transaction list.
        """
        self.__num_transaction = 0
        self.__items = []
        self.__transaction_index_map = {}
        self.add_transactions(transactions)

    def add_transactions(self, transactions):
        """
        Add transactions.

        @param  transactions    A transaction list.
        """
        for transaction in transactions:
            for item in transaction:
                if item not in self.__transaction_index_map:
                    self.__items.append(item)
                    self.__transaction_index_map[item] = set()
                self.__transaction_index_map[item].add(self.__num_transaction)
            self.__num_transaction += 1

    def calc_support(self, items):
        """
        Returns a support for items.
        """
        # Empty items is supported by all transactions.
        if not items:
            return 1.0

        # Create the transaction index intersection.
        sum_indexes = None
        for item in items:
            indexes = self.__transaction_index_map.get(item)
            if indexes is None:
                # No support for any set that contains a not existing item.
                return 0.0

            if sum_indexes is None:
                sum_indexes = indexes
            else:
                sum_indexes = sum_indexes.intersection(indexes)

        # Calculate the support.
        return float(len(sum_indexes)) / self.__num_transaction

    def initial_candidates(self):
        """
        Returns the initial candidates.
        """
        return [frozenset([item]) for item in self.__items]

    @property
    def num_transaction(self):
        """
        Returns the number of transactions.
        """
        return self.__num_transaction

    @property
    def items(self):
        """
        Returns the item list that the transaction is consisted of.
        """
        return self.__items

    @staticmethod
    def create(transactions):
        """
        Create the TransactionManager with a transaction instance.
        If the given instance is a TransactionManager, this returns itself.
        """
        if isinstance(transactions, TransactionManager):
            return transactions
        return TransactionManager(transactions)


def create_next_candidates(prev_candidates, length):
    """
    Returns the apriori candidates.
    """
    # Solve the items.
    items = set()
    for candidate in prev_candidates:
        for item in candidate:
            items.add(item)

    # Create candidates.
    next_candidates = []
    for candidate in [frozenset(x) for x in combinations(items, length)]:
        if length > 2:
            candidate_subsets = [
                frozenset(x) for x in combinations(candidate, length - 1)]
            is_valid = functools.reduce(
                lambda a, b: a and b in prev_candidates, candidate_subsets)
            if not is_valid:
                continue
        next_candidates.append(candidate)
    return next_candidates


def gen_support_records(
        transaction_manager,
        min_support,
        max_length=None,
        _generate_candidates_func=create_next_candidates):
    """
    Returns the supported relations.
    """
    candidates = transaction_manager.initial_candidates()
    length = 1
    while candidates:
        relations = set()
        for relation_candidate in candidates:
            support = transaction_manager.calc_support(relation_candidate)
            if support < min_support:
                continue
            candidate_set = frozenset(relation_candidate)
            relations.add(candidate_set)
            yield SupportRecord(candidate_set, support)
        length += 1
        if max_length and length > max_length:
            break
        candidates = _generate_candidates_func(relations, length)


def gen_ordered_statistics(transaction_manager, record):
    """
    Returns the relation stats.
    """
    items = record.items
    combination_sets = [
        frozenset(x) for x in combinations(items, len(items) - 1)]
    for items_base in combination_sets:
        items_add = frozenset(items.difference(items_base))
        confidence = (
            record.support / transaction_manager.calc_support(items_base))
        lift = confidence / transaction_manager.calc_support(items_add)
        yield OrderedStatistic(
            frozenset(items_base), frozenset(items_add), confidence, lift)


def apriori(transactions, **kwargs):
    """
    Run Apriori algorithm.

    @param  transactions    A list of transactions.
    @param  min_support     The minimum support of the relation (float).
    @param  max_length      The maximum length of the relation (integer).
    """
    min_support = kwargs.get('min_support', 0.1)
    max_length = kwargs.get('max_length', None)
    min_confidence = kwargs.get('min_confidence', 0.0)

    # Calculate supports.
    transaction_manager = TransactionManager.create(transactions)
    support_records = gen_support_records(
        transaction_manager, min_support, max_length)

    # Calculate stats.
    for support_record in support_records:
        ordered_statistics = gen_ordered_statistics(
            transaction_manager, support_record)
        filtered_ordered_statistics = [
            x for x in ordered_statistics if x.confidence >= min_confidence]
        if not filtered_ordered_statistics:
            continue
        yield RelationRecord(
            support_record.items, support_record.support,
            filtered_ordered_statistics)


def print_record_default(record, output_file):
    """
    Print an Apriori algorithm result.

    @param  record      A record.
    @param  output_file An output file.
    """
    for ordered_stats in record.ordered_statistics:
        output_file.write(
            '{{{0}}} => {{{1}}} {2:.8f} {3:.8f} {4:.8f}\n'.format(
                ','.join(ordered_stats.items_base),
                ','.join(ordered_stats.items_add),
                record.support, ordered_stats.confidence, ordered_stats.lift))


def print_record_as_two_item_tsv(record, output_file):
    """
    Print an Apriori algorithm result as two item TSV.

    @param  record      A record.
    @param  output_file An output file.
    """
    for ordered_stats in record.ordered_statistics:
        if len(ordered_stats.items_base) != 1:
            return
        if len(ordered_stats.items_add) != 1:
            return
        output_file.write(
            '{0}\t{1}\t{2:.8f}\t{3:.8f}\t{4:.8f}\n'.format(
                [x for x in ordered_stats.items_base][0],
                [x for x in ordered_stats.items_add][0],
                record.support, ordered_stats.confidence, ordered_stats.lift))


def main():
    """
    Main.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input-file', help='Input file.', metavar='path',
        type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument(
        '-o', '--output-file', help='Output file.', metavar='path',
        type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument(
        '-l', '--max-length', help='Max length.', metavar='int',
        type=int, default=None)
    parser.add_argument(
        '-s', '--min-support', help='Minimum support (0.0-1.0).',
        metavar='float', type=float, default=0.15)
    parser.add_argument(
        '-c', '--min-confidence', help='Minimum confidence (0.0-1.0).',
        metavar='float', type=float, default=0.6)
    parser.add_argument(
        '-d', '--delimiter', help='Delimiter for input.',
        metavar='str', type=str, default='\t')
    parser.add_argument(
        '-f', '--out-format', help='Output format (default or tsv).',
        metavar='str', type=str, choices=['default', 'tsv'],
        default='default')
    args = parser.parse_args()

    transactions = [
        line.strip().split(args.delimiter)
        for line in args.input_file]
    result = apriori(
        transactions,
        max_length=args.max_length,
        min_support=args.min_support,
        min_confidence=args.min_confidence)

    output_func = {
        'default': print_record_default,
        'tsv': print_record_as_two_item_tsv
    }.get(args.out_format)
    for record in result:
        output_func(record, args.output_file)


if __name__ == '__main__':
    main()
