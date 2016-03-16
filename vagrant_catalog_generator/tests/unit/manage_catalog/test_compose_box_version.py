from vagrant_catalog_generator.manage_catalog import compose_box_version
from vagrant_catalog_generator.tests.testcase import TestCase


class TestComposeBoxVersion(TestCase):
    def setUp(self):
        self.test_args = (
            '2638',
            'vagrant',
            'https://example.com',
            'boxfile.box',
            '527d7e25b96cbceaacd7819edbb34c9750dca355fd2d4cb288df9a89ee5fdf2a'
        )

    def test_compose_box_version_returns_composed_box_version(self):
        ret = compose_box_version(*self.test_args)

        expected_box_version = {
            'version': '2638',
            'providers': [
                {
                    'name': 'vagrant',
                    'url': 'https://example.com/boxfile.box',
                    'checksum_type': 'sha256',
                    'checksum': '527d7e25b96cbceaacd7819edbb34c9750dca355fd2d4cb288df9a89ee5fdf2a'
                }
            ]
        }
        self.assertEqual(ret, expected_box_version)

    def test_compose_box_version_returns_composed_box_version_with_specified_checksum_type(self):
        ret = compose_box_version(*self.test_args, checksum_type='sha512')

        expected_box_version = {
            'version': '2638',
            'providers': [
                {
                    'name': 'vagrant',
                    'url': 'https://example.com/boxfile.box',
                    'checksum_type': 'sha512',
                    'checksum': '527d7e25b96cbceaacd7819edbb34c9750dca355fd2d4cb288df9a89ee5fdf2a'
                }
            ]
        }
        self.assertEqual(ret, expected_box_version)
