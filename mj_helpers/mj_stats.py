#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
Command line argument to print stats to screen after profileit has been run.
"""
from pstats import Stats
import argparse
import sys
import os


SORTING = {
    'calls': 'Call count',
    'cumulative': 'Cumulative time',
    'file': 'File name',
    'module': 'File name',
    'pcalls': 'Primitive call count',
    'line': 'Line number',
    'name': 'Function name',
    'nfl': 'Name/File/Line',
    'stdname': 'Standard name',
    'time': 'Internal time',
}

def print_stats(filepaths, sorting='cumulative', limit=50):
    """
    Print the stats of a the given files.

    Loop through filepaths, if the file exists, attempt to parse the file with
    Stats the print the results.

    :param filepaths: List of strings that represents file paths
    :param sorting: A string representing which field to sort on
    :param limit: The number of lines to print
    """
    for file_ in filepaths:
        if os.path.isfile(file_):
            try:
                print('\n')
                stats = Stats(file_)

            except AttributeError:
                error_message = '{file_} does not appear to be a valid file'
                print(error_message.format(file_=file_))
                continue

            stats.sort_stats('cumulative').print_stats(limit)

def print_sorting_options():
    print('\nSorting option must be one of the following:\n')
    table_break = '+-----------+---------------------+'
    print(table_break)
    print('|{key:<11}|{value:<21}|'.format(key='Valid Arg', value='Meaning'))
    print(table_break.replace('-', '='))
    for key, value in SORTING.iteritems():
        print('|{key:<11}|{value:<21}|'.format(key=key, value=value))
        print(table_break)


def main():
    description = 'Print the top 50 stats from the @profileit decorator'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        'filepath',
        nargs='+',
        help='Location of /file/path/$FUNCTION_NAME.profile'
    )
    parser.add_argument(
        '--sorting',
        default='cumulative',
        help='Optional argument for sorting results'
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=50,
        help='Optional argument for sorting results'
    )

    args = parser.parse_args()

    if args.sorting not in SORTING:
        print_sorting_options()
        sys.exit(-1)

    if args.filepath:
        print_stats(args.filepath, args.sorting, args.limit)


if __name__ == '__main__':
    main()
