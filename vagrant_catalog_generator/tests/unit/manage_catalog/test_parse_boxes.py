from mock import call

from vagrant_catalog_generator.manage_catalog import parse_boxes
from vagrant_catalog_generator.tests.testcase import TestCase


class TestParseBoxes(TestCase):
    def setUp(self):
        self.boxes = [
            'hypernode.vagrant.release-latest.box',
            'hypernode.vagrant.release-1065.box',
            'hypernode.vagrant.release-1066.box',
        ]

        self.generate_box_metadata = self.set_up_patch('vagrant_catalog_generator.manage_catalog.generate_box_metadata')
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

    def test_parse_boxes_generates_box_metadata_for_all_boxes(self):
        parse_boxes(self.boxes, 'https://example.com', '/some/dir', 'my vagrant box', 'hypernode')

        expected_calls = [
            call('/some/dir', 'hypernode.vagrant.release-1065.box', '1065',
                 'vagrant', 'https://example.com'),
            call('/some/dir', 'hypernode.vagrant.release-1066.box', '1066',
                 'vagrant', 'https://example.com'),
        ]

        self.assertEqual(expected_calls, self.generate_box_metadata.mock_calls)

    def test_parse_boxes_returns_box_metadata(self):
        ret = parse_boxes(self.boxes, 'https://example.com', '/some/dir', 'my vagrant box', 'hypernode')

        expected_metadata = {
            'description': 'my vagrant box',
            'name': 'hypernode',
            'versions': [
                self.box1_metadata,
                self.box2_metadata
            ]
        }

        self.assertEqual(expected_metadata, ret)
