'''
Create an argument parser using argparse

Functions:
    get_parser() -> parser
'''

import argparse
from argparse import RawTextHelpFormatter

def get_parser():
    ''''Create a parser object specific to codoniser'''
    parser = argparse.ArgumentParser(
        "codoniser",
        description=
        "codoniser: a python package to visualise codon usage, and codon usage correlation.",
        epilog="Written by Dr. Thom Booth, 2022.",
        formatter_class=RawTextHelpFormatter
        )
    parser.add_argument(
        '-b',
        '--barchart',
        action='store_true',
        default=None,
        help=
            'provide a prefix for codon usage barchart'
            '(Default: FALSE)'
        )
    parser.add_argument(
        '-p',
        '--pearsons',
        action='store_true',
        default=None,
        help=
            'perform pearsons rank correlation analysis'
            '(Default: FALSE)'
        )
    parser.add_argument(
        '-s',
        '--spearmans',
        action='store_true',
        default=None,
        help=
            'perform spearmans rank correlation analysis'
            '(Default: FALSE)'
        )
    parser.add_argument(
        '-k',
        '--skip-malformed-cds',
        action='store_true',
        default=None,
        help=
            'perform spearmans rank correlation analysis'
            '(Default: FALSE)'
        )
    parser.add_argument(
        'files',
        type=str,
        nargs='+',
        default=None,
        help='path to a fasta file containing nucleotide sequences of each gene'
        )
    return parser

def parse_args():
    '''get the arguments from the console via the parser'''
    parser = get_parser()
    args = parser.parse_args()
    return args
