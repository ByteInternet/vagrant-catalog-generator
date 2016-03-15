from logging import INFO, getLogger, StreamHandler
from sys import stdout


def setup_logging(level=INFO):
    logger = getLogger('hypernode-boxfile-manager')
    logger.setLevel(level)
    console_handler = StreamHandler(stdout)
    logger.addHandler(console_handler)
    return logger
