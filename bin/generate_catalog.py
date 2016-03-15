from boxfile_manager.log import setup_logging
from boxfile_manager.manage_catalog import create_catalog

if __name__ == '__main__':
    setup_logging()
    create_catalog()
