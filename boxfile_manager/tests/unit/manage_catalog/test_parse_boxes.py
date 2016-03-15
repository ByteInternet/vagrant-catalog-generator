from mock import call

from boxfile_manager.manage_catalog import parse_boxes
from boxfile_manager.settings import BOX_METADATA
from boxfile_manager.tests.testcase import TestCase


class TestParseBoxes(TestCase):
    def setUp(self):
        self.boxes = [
            'hypernode.vagrant.release-latest.box',
            'hypernode.vagrant.release-1065.box',
            'hypernode.vagrant.release-1066.box',
        ]

        self.deepcopy = self.set_up_patch('boxfile_manager.manage_catalog.deepcopy')
        self.deepcopy.return_value = {
            'name': 'hypernode',
            'versions': []
        }
        self.generate_box_metadata = self.set_up_patch('boxfile_manager.manage_catalog.generate_box_metadata')
        self.box1_metadata = {
            "version": "2647",
            "providers": [
                {
                    "url": "http://vagrant.example.com/hypernode.vagrant.release-2647.box",
                    "checksum_type": "sha256",
                    "name": "virtualbox",
                    "checksum": "527d7e25b96cbceaacd7819edbb34c9750dca355fd2d4cb288df9a89ee5fdf2a"
                }
            ]
        }
        self.box2_metadata = {
            "version": "2659",
            "providers": [
                {
                    "url": "http://vagrant.example.com/hypernode.vagrant.release-2659.box",
                    "checksum_type": "sha256",
                    "name": "virtualbox",
                    "checksum": "5dcb7a16edea25ae32fdef015ae96e95f94b16e4b2e886b3f19f7bb8463c5d7e"
                }
            ]
        }

        self.generate_box_metadata.side_effect = [self.box1_metadata, self.box2_metadata]

    def test_parse_boxes_deepcopies_metadata_from_settings(self):
        parse_boxes(self.boxes)

        self.deepcopy.assert_called_once_with(BOX_METADATA)

    def test_parse_boxes_generates_box_metadata_for_all_boxes(self):
        parse_boxes(self.boxes)

        expected_calls = [
            call('hypernode.vagrant.release-1065.box', '1065', 'vagrant'),
            call('hypernode.vagrant.release-1066.box', '1066', 'vagrant'),
        ]
        self.assertEqual(expected_calls, self.generate_box_metadata.mock_calls)

    def test_parse_boxes_returns_box_metadata(self):
        ret = parse_boxes(self.boxes)

        expected_metadata = self.deepcopy.return_value
        expected_metadata['versions'] = [
            self.box1_metadata,
            self.box2_metadata
        ]

        self.assertEqual(expected_metadata, ret)
