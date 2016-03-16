import logging
from hashlib import sha256
from json import dump
from os import path, stat
from re import escape, compile

from vagrant_catalog_generator.box_list import list_boxes


logger = logging.getLogger(__name__)


def compose_box_version(version, provider, base_url, box, checksum, checksum_type='sha256'):
    return {
        'version': version,
        'providers': [
            {
                'name': provider,
                'url': path.join(base_url, box),
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
        return hasher.hexdigest()


def generate_checksum(shafile, boxfile):
    with open(shafile, 'w') as checksum_file:
        checksum = calculate_box_hash(boxfile)
        checksum_file.write(checksum)
        return checksum


def retrieve_checksum(shafile):
    with open(shafile, 'r') as checksum_file:
        return checksum_file.read().strip()


def generate_box_metadata(boxfiles_directory, box, version, provider, base_url):
    boxfile = path.join(boxfiles_directory, box)
    shafile = boxfile + '.sha256'
    if not path.isfile(shafile) or stat(shafile).st_size == 0:
        logger.info('Calculating SHA256 sum for {}'.format(box))
        checksum = generate_checksum(shafile, boxfile)
    else:
        logger.info('Retrieving SHA256 for {} from cache'.format(box))
        checksum = retrieve_checksum(shafile)
    return compose_box_version(version, provider, base_url, box, checksum)


def parse_boxes(boxes, base_url, boxfiles_directory, description, box_name):
    logger.info("Generating metadata")
    metadata = {'versions': [], 'description': description, 'name': box_name}
    provider_and_version_pattern = compile(r'^{}\.([^.]*)\.release-(.*)\.box$'.format(escape(box_name)))
    for box in boxes:
        match = provider_and_version_pattern.search(box)
        if match:
            provider, version = match.groups()
            if version == 'latest':
                continue
            metadata['versions'].append(
                generate_box_metadata(boxfiles_directory, box, version, provider, base_url)
            )
        else:
            logger.info('Could not parse version of {}, skipping!'.format(box))
            continue
    return metadata


def write_catalog(boxfiles_directory, metadata):
    catalog_path = path.join(boxfiles_directory, 'catalog.json')
    with open(catalog_path, 'w') as f:
        dump(metadata, f, indent=2)
    logger.info("Done creating catalog! Wrote to: {}".format(catalog_path))


def create_catalog(base_url, boxfiles_directory, description, box_name):
    logger.info("Generating catalog for box {}".format(box_name))
    boxes = list_boxes(box_name, boxfiles_directory)
    metadata = parse_boxes(boxes, base_url, boxfiles_directory, description, box_name)
    write_catalog(boxfiles_directory, metadata)
