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


def generate_box_metadata(boxfiles_directory, box, version, provider, base_url, force_generate=False):
    boxfile = path.join(boxfiles_directory, box)
    shafile = boxfile + '.sha256'
    if not path.isfile(shafile) or stat(shafile).st_size == 0 or force_generate:
        logger.info('Calculating SHA256 sum for {}'.format(box))
        checksum = generate_checksum(shafile, boxfile)
    else:
        logger.info('Retrieving SHA256 for {} from cache'.format(box))
        checksum = retrieve_checksum(shafile)
    return compose_box_version(version, provider, base_url, box, checksum)


def combine_provider_versions(box_metadata):
    versions = dict()
    for box in box_metadata:
        version = box['version']
        if version not in versions:
            versions[version] = list()
        versions[version].extend(box['providers'])

    metadata = list()
    for version in sorted(versions.keys()):
        metadata.append({
            'version': version,
            'providers': versions[version]
        })
    return metadata


def parse_boxes(boxes, base_url, boxfiles_directory, box_name, forced_box=None):
    logger.info("Generating metadata")
    provider_and_version_pattern = compile(r'^{}\.([^.]*)\.release-(.*)\.box$'.format(escape(box_name)))
    boxes_metadata = list()
    for box in boxes:
        match = provider_and_version_pattern.search(box)
        if match:
            provider, version = match.groups()
            if version == 'latest':
                continue
            if forced_box is not None and version == forced_box:
                force_generate = True
            else:
                force_generate = False
            boxes_metadata.append(
                generate_box_metadata(boxfiles_directory, box, version, provider, base_url, force_generate)
            )
        else:
            logger.info('Could not parse version of {}, skipping!'.format(box))
            continue
    return boxes_metadata


def generate_metadata(boxes_metadata, box_name, description):
    return {
        'description': description,
        'name': box_name,
        'versions': combine_provider_versions(boxes_metadata)
    }


def write_catalog(boxfiles_directory, metadata):
    catalog_path = path.join(boxfiles_directory, 'catalog.json')
    with open(catalog_path, 'w') as f:
        dump(metadata, f, indent=2)
    logger.info("Done creating catalog! Wrote to: {}".format(catalog_path))


def create_catalog(base_url, boxfiles_directory, description, box_name, forced_box=None):
    logger.info("Generating catalog for box {}".format(box_name))
    boxes = list_boxes(box_name, boxfiles_directory)
    boxes_metadata = parse_boxes(boxes, base_url, boxfiles_directory, box_name, forced_box)
    metadata = generate_metadata(boxes_metadata, box_name, description)
    write_catalog(boxfiles_directory, metadata)
