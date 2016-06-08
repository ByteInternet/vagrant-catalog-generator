#!/usr/bin/env python

from argparse import ArgumentParser
from os.path import curdir

from vagrant_catalog_generator.log import setup_logging
from vagrant_catalog_generator.manage_boxfiles import clean_up_old_boxes
from vagrant_catalog_generator.settings import RECENT_BOX_AMOUNT, BOX_NAME


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--name', help="Name of the box. Default: {}".format(BOX_NAME),
                        default=BOX_NAME)
    parser.add_argument('--directory', help="Directory where the boxfiles are. Default: current working dir",
                        default=curdir)
    parser.add_argument('--amount', help="Amount of releases to keep. Default: {}".format(RECENT_BOX_AMOUNT),
                        default=RECENT_BOX_AMOUNT)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    setup_logging()

    clean_up_old_boxes(args.name, args.directory, int(args.amount))
