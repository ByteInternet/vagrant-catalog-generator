from copy import deepcopy
from hashlib import sha256
from json import dump
from logging import getLogger
from os import path, stat

from boxfile_manager.box_list import list_boxes
from boxfile_manager.settings import PROVIDER_AND_VERSION_PATTERN, BASE_URL, BOX_METADATA

logger = getLogger(__name__)


def compose_box_version(version, provider, url, checksum, checksum_type='sha256'):
    return {
        'version': version,
        'providers': [
            {
                'name': provider,
                'url': BASE_URL + url,
                'checksum_type': checksum_type,
                'checksum': checksum
            }
        ]
    }


def calculate_box_hash(boxfile, blocksize=65536):
    with open(boxfile, 'rb') as fh:
        hasher = sha256()
        buf = fh.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = fh.read(blocksize)
        return hasher.digest()


def generate_checksum(shafile, boxfile):
    with open(shafile, 'w') as checksum_file:
        checksum = calculate_box_hash(boxfile)
        checksum_file.write(checksum)
        return checksum


def retrieve_checksum(shafile):
    with open(shafile, 'r') as checksum_file:
        return checksum_file.read().strip()


def generate_box_metadata(box, version, provider):
    boxfile = path.abspath(box)
    shafile = boxfile + '.sha256'
    if not path.isfile(shafile) or stat(shafile).st_size == 0:
        logger.info('Calculating SHA256 sum for {}'.format(box))
        checksum = generate_checksum(shafile, boxfile)
    else:
        logger.info('Retrieving SHA256 for {} from cache'.format(box))
        checksum = retrieve_checksum(shafile)
    return compose_box_version(version, provider, box, checksum)


def parse_boxes(boxes):
    metadata = deepcopy(BOX_METADATA)
    for box in boxes:
        match = PROVIDER_AND_VERSION_PATTERN.search(box)
        if match:
            provider, version = match.groups()
            if version == 'latest':
                continue
            metadata['versions'].append(
                generate_box_metadata(box, version, provider)
            )
        else:
            logger.info('Could not parse version of {}, skipping!'.format(box))
            continue
    return metadata


def write_catalog(metadata):
    with open('catalog.json', 'w') as f:
        dump(metadata, f, indent=2)


def create_catalog():
    boxes = list_boxes()
    metadata = parse_boxes(boxes)
    write_catalog(metadata)
    logger.info("Done creating catalog.json!")
