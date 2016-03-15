from mock import Mock

from boxfile_manager.manage_catalog import write_catalog
from boxfile_manager.tests.testcase import TestCase


class TestWriteCatalog(TestCase):
    def setUp(self):
        self.open = self.set_up_patch('boxfile_manager.manage_catalog.open')
        self.open.return_value.__exit__ = lambda a, b, c, d: None
        self.file_handle = Mock()
        self.open.return_value.__enter__ = lambda x: self.file_handle
        self.dump = self.set_up_patch('boxfile_manager.manage_catalog.dump')
        self.metadata = {'name': 'hypernode'}

    def test_write_catalog_opens_catalog_json(self):
        write_catalog(self.metadata)

        self.open.assert_called_once_with('catalog.json', 'w')

    def test_write_catalog_dumps_metadata_to_disk(self):
        write_catalog(self.metadata)

        self.dump.assert_called_once_with(self.metadata, self.file_handle, indent=2)
