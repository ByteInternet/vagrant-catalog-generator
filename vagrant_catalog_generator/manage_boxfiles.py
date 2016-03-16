import logging
from os import remove, path

from vagrant_catalog_generator.box_list import list_boxes
from vagrant_catalog_generator.settings import RECENT_BOX_AMOUNT

logger = logging.getLogger('vagrant-catalog-generator')


def remove_boxfile(boxfiles_directory, box):
    box_path = path.join(boxfiles_directory, box)
    try:
        logger.info('Cleaning up old box {}'.format(box))
        remove(box_path)
    except OSError:
        logger.info('Could not remove old box {}, probably already gone. Skipping'.format(box))


def remove_checksum(boxfiles_directory, box):
    checksum_path = path.join(boxfiles_directory, box) + '.sha256'
    try:
        logger.info('Cleaning up old checksum for {}'.format(box))
        remove(checksum_path)
    except OSError:
        logger.info('Could not remove old checksum for {}, probably already gone. Skipping'.format(box))


def only_keep_recent_boxes(boxfiles_directory, boxes, amount=RECENT_BOX_AMOUNT):
    sorted_boxes = filter(lambda name: 'latest' not in name, sorted(boxes))
    old_boxes = list(sorted_boxes)[:-amount]
    for old_box in old_boxes:
        remove_boxfile(boxfiles_directory, old_box)
        remove_checksum(boxfiles_directory, old_box)


def clean_up_old_boxes(box_name, boxfiles_directory, amount):
    boxes = list_boxes(box_name, boxfiles_directory)
    only_keep_recent_boxes(boxfiles_directory, boxes, amount=amount)
