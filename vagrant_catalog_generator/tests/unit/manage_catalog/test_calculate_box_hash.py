from mock import call, Mock

from vagrant_catalog_generator.manage_catalog import calculate_box_hash
from vagrant_catalog_generator.tests.testcase import TestCase


class TestCalculateBoxHash(TestCase):
    def setUp(self):
        self.open = self.set_up_patch('vagrant_catalog_generator.manage_catalog.open')
        self.open.return_value.__exit__ = lambda a, b, c, d: None
        self.file_handle = Mock()
        self.buffer = list()
        self.file_handle.read.return_value = self.buffer
        self.open.return_value.__enter__ = lambda x: self.file_handle
        self.boxfile = 'hypernode.vagrant.release-2638.box'
        self.sha256 = self.set_up_patch('vagrant_catalog_generator.manage_catalog.sha256')
        self.hasher = self.sha256.return_value

    def test_calculate_box_hash_opens_boxfile(self):
        calculate_box_hash(self.boxfile)

        self.open.assert_called_once_with(self.boxfile, 'rb')

    def test_calculate_box_hash_instantiates_hasher(self):
        calculate_box_hash(self.boxfile)

        self.sha256.assert_called_once_with()

    def test_calculate_box_hash_reads_default_block_size_from_file_handle(self):
        calculate_box_hash(self.boxfile)

        self.file_handle.read.assert_called_once_with(65536)

    def test_calculate_box_hash_reads_defined_block_size_from_file_handle(self):
        calculate_box_hash(self.boxfile, blocksize=1234)

        self.file_handle.read.assert_called_once_with(1234)

    def test_calculate_box_hash_updates_hasher_until_blocks_run_out(self):
        self.file_handle.read.side_effect = [
            [1, 2, 3],
            [1, 2, 3],
            [1, 2],
            []
        ]

        calculate_box_hash(self.boxfile, blocksize=1234)

        expected_calls = [
            call([1, 2, 3]),
            call([1, 2, 3]),
            call([1, 2])
        ]
        self.assertEqual(expected_calls, self.hasher.update.mock_calls)

    def test_calculate_box_hash_reads_blocks_from_file_handle_until_they_run_out(self):
        self.file_handle.read.side_effect = [
            [1, 2, 3],
            [1, 2, 3],
            [1, 2],
            []
        ]

        calculate_box_hash(self.boxfile, blocksize=3)

        expected_calls = [call(3)] * 4
        self.assertEqual(expected_calls, self.file_handle.read.mock_calls)

    def test_calculate_box_hash_returns_hasher_hexdigest(self):
        ret = calculate_box_hash(self.boxfile, blocksize=1234)

        self.assertEqual(ret, self.hasher.hexdigest.return_value)
