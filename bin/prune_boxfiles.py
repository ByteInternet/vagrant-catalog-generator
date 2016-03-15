from boxfile_manager.log import setup_logging
from boxfile_manager.manage_boxfiles import clean_up_old_boxes

if __name__ == '__main__':
    setup_logging()
    clean_up_old_boxes()
