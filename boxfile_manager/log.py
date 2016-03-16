import logging


def setup_logging(level=logging.INFO):
    logger = logging.getLogger('hypernode-boxfile-manager')
    formatter = '%(message)s'
    logging.basicConfig(level=level, format=formatter)
    return logger
