from boxfile_manager.manage_catalog import generate_box_metadata
from boxfile_manager.tests.testcase import TestCase


class TestGenerateBoxMetaData(TestCase):
    def setUp(self):
        self.path = self.set_up_patch('boxfile_manager.manage_catalog.path')
        self.path.abspath.return_value = '/some/dir/hypernode.vagrant.release-2638.box'
        self.boxfile = self.path.abspath.return_value
        self.shafile = self.boxfile + '.sha256'
        self.stat = self.set_up_patch('boxfile_manager.manage_catalog.stat')
        self.stat.return_value.st_size = 1
        self.generate_checksum = self.set_up_patch('boxfile_manager.manage_catalog.generate_checksum')
        self.retrieve_checksum = self.set_up_patch('boxfile_manager.manage_catalog.retrieve_checksum')
        self.compose_box_version = self.set_up_patch('boxfile_manager.manage_catalog.compose_box_version')

    def test_generate_box_metadata_gets_absolute_box_path(self):
        generate_box_metadata('hypernode.vagrant.release-2638.box', '2638', 'vagrant')

        self.path.abspath.assert_called_once_with('hypernode.vagrant.release-2638.box')

    def test_generate_box_metadata_checks_if_shafile_is_a_file(self):
        generate_box_metadata('hypernode.vagrant.release-2638.box', '2638', 'vagrant')

        self.path.isfile.assert_called_once_with(self.shafile)

    def test_generate_box_metadata_stats_shafile(self):
        generate_box_metadata('hypernode.vagrant.release-2638.box', '2638', 'vagrant')

        self.stat.assert_called_once_with(self.shafile)

    def test_generate_box_metadata_generates_checksum_if_shafile_doesnt_exist(self):
        self.path.isfile.return_value = False

        generate_box_metadata('hypernode.vagrant.release-2638.box', '2638', 'vagrant')

        self.generate_checksum.assert_called_once_with(self.shafile, self.boxfile)

    def test_generate_box_metadata_generates_checksum_if_shafile_is_empty(self):
        self.stat.return_value.st_size = 0

        generate_box_metadata('hypernode.vagrant.release-2638.box', '2638', 'vagrant')

        self.generate_checksum.assert_called_once_with(self.shafile, self.boxfile)

    def test_generate_box_metadata_doesnt_generate_checksum_if_shafile_exists(self):
        generate_box_metadata('hypernode.vagrant.release-2638.box', '2638', 'vagrant')

        self.assertEqual(0, self.generate_checksum.call_count)

    def test_generate_box_metadata_doesnt_retrieve_checksum_if_shafile_doesnt_exist(self):
        self.path.isfile.return_value = False

        generate_box_metadata('hypernode.vagrant.release-2638.box', '2638', 'vagrant')

        self.assertEqual(0, self.retrieve_checksum.call_count)

    def test_generate_box_metadata_doesnt_retrieve_checksum_ifs_shafile_is_empty(self):
        self.stat.return_value.st_size = 0

        generate_box_metadata('hypernode.vagrant.release-2638.box', '2638', 'vagrant')

        self.assertEqual(0, self.retrieve_checksum.call_count)

    def test_generate_box_metadata_retrieves_checksum_if_shafile_exists(self):
        generate_box_metadata('hypernode.vagrant.release-2638.box', '2638', 'vagrant')

        self.retrieve_checksum.assert_called_once_with(self.shafile)

    def test_generate_box_metadata_composes_box_version_with_shafile_from_file_if_it_exists(self):
        generate_box_metadata('hypernode.vagrant.release-2638.box', '2638', 'vagrant')

        self.compose_box_version.assert_called_once_with(
            '2638',
            'vagrant',
            'hypernode.vagrant.release-2638.box',
            self.retrieve_checksum.return_value
        )

    def test_generate_box_metadata_composes_box_version_with_generated_shafile_if_file_doesnt_exist(self):
        self.path.isfile.return_value = False

        generate_box_metadata('hypernode.vagrant.release-2638.box', '2638', 'vagrant')

        self.compose_box_version.assert_called_once_with(
            '2638',
            'vagrant',
            'hypernode.vagrant.release-2638.box',
            self.generate_checksum.return_value
        )

    def test_generate_box_metadata_composes_box_version_with_generated_shafile_if_file_is_empty(self):
        self.stat.return_value.st_size = 0

        generate_box_metadata('hypernode.vagrant.release-2638.box', '2638', 'vagrant')

        self.compose_box_version.assert_called_once_with(
            '2638',
            'vagrant',
            'hypernode.vagrant.release-2638.box',
            self.generate_checksum.return_value
        )
