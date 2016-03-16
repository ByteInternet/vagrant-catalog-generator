from mock import Mock

from vagrant_catalog_generator.manage_catalog import generate_checksum
from vagrant_catalog_generator.tests.testcase import TestCase


class TestGenerateChecksum(TestCase):
    def setUp(self):
        self.open = self.set_up_patch('vagrant_catalog_generator.manage_catalog.open')
        self.open.return_value.__exit__ = lambda a, b, c, d: None
        self.file_handle = Mock()
        self.open.return_value.__enter__ = lambda x: self.file_handle
        self.boxfile = 'hypernode.vagrant.release-2638.box'
        self.shafile = self.boxfile + '.sha256'
        self.calculate_box_hash = self.set_up_patch('vagrant_catalog_generator.manage_catalog.calculate_box_hash')

    def test_generate_checksum_opens_shafile(self):
        generate_checksum(self.shafile, self.boxfile)

        self.open.assert_called_once_with(self.shafile, 'w')

    def test_generate_checksum_calculates_box_hash(self):
        generate_checksum(self.shafile, self.boxfile)

        self.calculate_box_hash.assert_called_once_with(self.boxfile)

    def test_generate_checksum_writes_to_file(self):
        generate_checksum(self.shafile, self.boxfile)

        self.file_handle.write.assert_called_once_with(
            self.calculate_box_hash.return_value
        )

    def test_generate_checksum_returns_calculated_checksum(self):
        ret = generate_checksum(self.shafile, self.boxfile)

        self.assertEqual(ret, self.calculate_box_hash.return_value)
