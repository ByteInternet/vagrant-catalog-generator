from boxfile_manager.manage_boxfiles import clean_up_old_boxes
from boxfile_manager.tests.testcase import TestCase


class TestCleanUpOldBoxes(TestCase):
    def setUp(self):
        self.list_boxes = self.set_up_patch('boxfile_manager.manage_boxfiles.list_boxes')
        self.only_keep_recent_boxes = self.set_up_patch('boxfile_manager.manage_boxfiles.only_keep_recent_boxes')

    def test_clean_up_old_boxes_lists_boxes(self):
        clean_up_old_boxes()

        self.list_boxes.assert_called_once_with()

    def test_clean_up_old_boxes_only_keeps_recent_boxes(self):
        clean_up_old_boxes()

        self.only_keep_recent_boxes.assert_called_once_with(
            self.list_boxes.return_value
        )
