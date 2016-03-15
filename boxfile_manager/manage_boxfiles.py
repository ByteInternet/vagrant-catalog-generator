from logging import getLogger
from os import remove, path

from boxfile_manager.box_list import list_boxes
from boxfile_manager.settings import RECENT_BOX_AMOUNT

logger = getLogger(__name__)


def remove_boxfile(box):
    box_path = path.abspath(box)
    try:
        logger.info('Cleaning up old box {}'.format(box))
        remove(box_path)
    except OSError:
        logger.info('Could not remove old box {}, probably already gone. Skipping'.format(box))


def remove_checksum(box):
    checksum_path = path.abspath(box) + '.sha256'
    try:
        logger.info('Cleaning up old checksum for {}'.format(box))
        remove(checksum_path)
    except OSError:
        logger.info('Could not remove old checksum for {}, probably already gone. Skipping'.format(box))


def only_keep_recent_boxes(boxes, amount=RECENT_BOX_AMOUNT):
    sorted_boxes = filter(lambda name: 'latest' not in name, sorted(boxes))
    old_boxes = list(sorted_boxes)[:-amount]
    for old_box in old_boxes:
        remove_boxfile(old_box)
        remove_checksum(old_box)


def clean_up_old_boxes():
    boxes = list_boxes()
    only_keep_recent_boxes(boxes)
