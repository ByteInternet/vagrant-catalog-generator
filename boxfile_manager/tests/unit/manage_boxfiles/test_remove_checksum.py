from boxfile_manager.manage_boxfiles import remove_checksum
from boxfile_manager.tests.testcase import TestCase


class TestRemoveChecksum(TestCase):
    def setUp(self):
        self.path = self.set_up_patch('boxfile_manager.manage_boxfiles.path')
        self.path.join.return_value = '/some/dir/hypernode.vagrant.release-2638.box'
        self.remove = self.set_up_patch('boxfile_manager.manage_boxfiles.remove')

    def test_remove_checksum_gets_box_abspath(self):
        remove_checksum('/some/dir', 'hypernode.vagrant.release-2638.box')

        self.path.join.assert_called_once_with('/some/dir', 'hypernode.vagrant.release-2638.box')

    def test_remove_checksum_removes_checksum_path(self):
        remove_checksum('/some/dir', 'hypernode.vagrant.release-2638.box')

        self.remove.assert_called_once_with(
            self.path.join.return_value + '.sha256'
        )

    def test_remove_checksum_catches_gone_files_and_other_oserrors(self):
        self.remove.side_effect = OSError

        remove_checksum('/some/dir', 'hypernode.vagrant.release-2638.box')
