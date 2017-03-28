#!/usr/bin/env python

from argparse import ArgumentParser

from vagrant_catalog_generator.log import setup_logging
from vagrant_catalog_generator.manage_catalog import create_catalog
from vagrant_catalog_generator.settings import BASE_URL, BOX_NAME, BOX_DESCRIPTION


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--name', help="Name of the box. Default: {}".format(BOX_NAME),
                        default=BOX_NAME)
    parser.add_argument('--directory', help="Directory where the boxfiles are.")
    parser.add_argument('--base-url', help="Base url of where the boxfiles are hosted. Default: {}".format(BASE_URL),
                        default=BASE_URL)
    parser.add_argument('--description', help="Description of the box. Default: {}"
                        .format(BOX_DESCRIPTION),
                        default=BOX_DESCRIPTION)
    parser.add_argument('--forced_box',
                        help="Force generation of hash for this box. Default: None",
                        default=None)
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()

    setup_logging()

    create_catalog(args.base_url, args.directory, args.description, args.name, args.forced_box)
