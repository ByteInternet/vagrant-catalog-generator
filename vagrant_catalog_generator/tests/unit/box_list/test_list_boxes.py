from vagrant_catalog_generator.box_list import list_boxes
from vagrant_catalog_generator.tests.testcase import TestCase


class TestListBoxes(TestCase):
    def setUp(self):
        self.listdir = self.set_up_patch('vagrant_catalog_generator.box_list.listdir')
        self.listdir.return_value = [
            'hypernode.vagrant.release-latest.box',
            'hypernode.vagrant.release-latest.box.sha256',
            'hypernode.vagrant.release-1065.box',
            'hypernode.vagrant.release-1065.box.sha256',
            'hypernode.vagrant.release-1066.box',
            'hypernode.vagrant.release-1066.box.sha256',
            'not_a_boxfile',
        ]

    def test_list_boxes_lists_current_directory(self):
        list_boxes('hypernode', '/some/dir')

        self.listdir.assert_called_once_with('/some/dir')

    def test_list_boxes_returns_boxes(self):
        ret = list_boxes('hypernode', '/some/dir')

        expected_list = [
            'hypernode.vagrant.release-latest.box',
            'hypernode.vagrant.release-1065.box',
            'hypernode.vagrant.release-1066.box',
        ]

        self.assertEqual(list(ret), expected_list)
