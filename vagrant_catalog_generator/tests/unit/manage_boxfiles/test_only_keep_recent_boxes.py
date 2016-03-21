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
            'hypernode.virtualbox.release-1.box',
            'hypernode.lxc.release-1.box',
            'hypernode.virtualbox.release-2635.box',
            'hypernode.lxc.release-2635.box',
            'hypernode.virtualbox.release-2638.box',
            'hypernode.lxc.release-2638.box',
            'hypernode.virtualbox.release-2653.box',
            'hypernode.lxc.release-2653.box',
            'hypernode.virtualbox.release-2659.box',
            'hypernode.lxc.release-2659.box',
            'hypernode.virtualbox.release-2674.box',
            'hypernode.lxc.release-2674.box'
        ]

    def test_only_keep_recent_boxes_removes_boxfiles(self):
        only_keep_recent_boxes('/some/dir', self.boxes, amount=6)

        expected_calls = [call('/some/dir', box) for box in [
            'hypernode.virtualbox.release-2635.box',
            'hypernode.lxc.release-2635.box',
            'hypernode.virtualbox.release-2638.box',
            'hypernode.lxc.release-2638.box',
        ]]

        self.assertEqual(expected_calls, self.remove_boxfile.mock_calls)

    def test_only_keep_recent_boxes_removes_checksum(self):
        only_keep_recent_boxes('/some/dir', self.boxes, amount=6)

        expected_calls = [call('/some/dir', box) for box in [
            'hypernode.virtualbox.release-2635.box',
            'hypernode.lxc.release-2635.box',
            'hypernode.virtualbox.release-2638.box',
            'hypernode.lxc.release-2638.box',
        ]]

        self.assertEqual(expected_calls, self.remove_checksum.mock_calls)

    def test_only_keep_recent_boxes_doesnt_remove_latest_link(self):
        only_keep_recent_boxes('/some/dir', self.boxes, amount=0)

        self.assertNotIn(call('/some/dir', 'hypernode.release-latest.box'), self.remove_boxfile.mock_calls)

    def test_only_keep_recent_boxes_doesnt_remove_latest_checksum(self):
        only_keep_recent_boxes('/some/dir', self.boxes, amount=0)

        self.assertNotIn(call('/some/dir', 'hypernode.release-latest.box'), self.remove_checksum.mock_calls)
