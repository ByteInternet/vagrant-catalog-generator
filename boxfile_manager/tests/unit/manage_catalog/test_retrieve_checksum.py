from mock import Mock

from boxfile_manager.manage_catalog import retrieve_checksum
from boxfile_manager.tests.testcase import TestCase


class TestRetrieveChecksum(TestCase):
    def setUp(self):
        self.open = self.set_up_patch('boxfile_manager.manage_catalog.open')
        self.open.return_value.__exit__ = lambda a, b, c, d: None
        self.file_handle = Mock()
        self.open.return_value.__enter__ = lambda x: self.file_handle
        self.shafile = 'hypernode.vagrant.release-2638.box.sha256'

    def test_retrieve_checksum_opens_shafile(self):
        retrieve_checksum(self.shafile)

        self.open.assert_called_once_with(self.shafile, 'r')

    def test_retrieve_checksum_reads_from_file(self):
        retrieve_checksum(self.shafile)

        self.file_handle.read.assert_called_once_with()

    def test_retrieve_checksum_strips_file_content(self):
        retrieve_checksum(self.shafile)

        self.file_handle.read.return_value.strip.assert_called_once_with()

    def test_retrieve_checksum_returns_checksum_from_file(self):
        ret = retrieve_checksum(self.shafile)

        self.assertEqual(ret, self.file_handle.read.return_value.strip.return_value)
