import logging


def setup_logging(level=logging.INFO):
    logger = logging.getLogger('vagrant-catalog-generator')
    formatter = '%(message)s'
    logging.basicConfig(level=level, format=formatter)
    return logger
