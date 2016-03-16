from boxfile_manager.manage_boxfiles import remove_boxfile
from boxfile_manager.tests.testcase import TestCase


class TestRemoveBoxfile(TestCase):
    def setUp(self):
        self.path = self.set_up_patch('boxfile_manager.manage_boxfiles.path')
        self.path.join.return_value = '/some/dir/hypernode.vagrant.release-2638.box'
        self.remove = self.set_up_patch('boxfile_manager.manage_boxfiles.remove')

    def test_remove_boxfile_gets_box_join(self):
        remove_boxfile('/some/dir', 'hypernode.vagrant.release-2638.box')

        self.path.join.assert_called_once_with('/some/dir', 'hypernode.vagrant.release-2638.box')

    def test_remove_boxfile_removes_boxfile_path(self):
        remove_boxfile('/some/dir', 'hypernode.vagrant.release-2638.box')

        self.remove.assert_called_once_with(
            self.path.join.return_value
        )

    def test_remove_boxfile_catches_gone_files_and_other_oserrors(self):
        self.remove.side_effect = OSError

        remove_boxfile('/some/dir', 'hypernode.vagrant.release-2638.box')
