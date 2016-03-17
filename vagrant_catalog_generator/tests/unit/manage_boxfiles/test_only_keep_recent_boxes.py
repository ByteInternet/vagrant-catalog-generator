from mock import call

from vagrant_catalog_generator.manage_boxfiles import only_keep_recent_boxes
from vagrant_catalog_generator.tests.testcase import TestCase


class TestOnlyKeepRecentBoxes(TestCase):
    def setUp(self):
        self.remove_boxfile = self.set_up_patch('vagrant_catalog_generator.manage_boxfiles.remove_boxfile')
        self.remove_checksum = self.set_up_patch('vagrant_catalog_generator.manage_boxfiles.remove_checksum')
        self.recent_box_amount = self.set_up_patch('vagrant_catalog_generator.manage_boxfiles.RECENT_BOX_AMOUNT')

        self.boxes = [
            'hypernode.release-latest.box',
            'hypernode.vagrant.release-1.box',
            'hypernode.vagrant.release-2635.box',
            'hypernode.vagrant.release-2638.box',
            'hypernode.vagrant.release-2653.box',
            'hypernode.vagrant.release-2659.box',
            'hypernode.vagrant.release-2674.box'
        ]

    def test_only_keep_recent_boxes_removes_boxfiles(self):
        only_keep_recent_boxes('/some/dir', self.boxes, amount=3)

        expected_calls = [call('/some/dir', box) for box in [
            'hypernode.vagrant.release-2635.box',
            'hypernode.vagrant.release-2638.box',
        ]]

        self.assertEqual(expected_calls, self.remove_boxfile.mock_calls)

    def test_only_keep_recent_boxes_removes_checksum(self):
        only_keep_recent_boxes('/some/dir', self.boxes, amount=3)

        expected_calls = [call('/some/dir', box) for box in [
            'hypernode.vagrant.release-2635.box',
            'hypernode.vagrant.release-2638.box',
        ]]

        self.assertEqual(expected_calls, self.remove_checksum.mock_calls)

    def test_only_keep_recent_boxes_doesnt_remove_latest_link(self):
        only_keep_recent_boxes('/some/dir', self.boxes, amount=0)

        self.assertNotIn(call('/some/dir', 'hypernode.release-latest.box'), self.remove_boxfile.mock_calls)

    def test_only_keep_recent_boxes_doesnt_remove_latest_checksum(self):
        only_keep_recent_boxes('/some/dir', self.boxes, amount=0)

        self.assertNotIn(call('/some/dir', 'hypernode.release-latest.box'), self.remove_checksum.mock_calls)
