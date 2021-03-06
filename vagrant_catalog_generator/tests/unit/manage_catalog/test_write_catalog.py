from mock import Mock

from vagrant_catalog_generator.manage_catalog import write_catalog
from vagrant_catalog_generator.tests.testcase import TestCase


class TestWriteCatalog(TestCase):
    def setUp(self):
        self.path = self.set_up_patch('vagrant_catalog_generator.manage_catalog.path')
        self.open = self.set_up_patch('vagrant_catalog_generator.manage_catalog.open')
        self.open.return_value.__exit__ = lambda a, b, c, d: None
        self.file_handle = Mock()
        self.open.return_value.__enter__ = lambda x: self.file_handle
        self.dump = self.set_up_patch('vagrant_catalog_generator.manage_catalog.dump')
        self.metadata = {'name': 'hypernode'}

    def test_write_catalog_joins_boxfiles_directory_with_catalog(self):
        write_catalog('/some/dir', self.metadata)

        self.path.join.assert_called_once_with('/some/dir', 'catalog.json')

    def test_write_catalog_opens_catalog_json(self):
        write_catalog('/some/dir', self.metadata)

        self.open.assert_called_once_with(self.path.join.return_value, 'w')

    def test_write_catalog_dumps_metadata_to_disk(self):
        write_catalog('/some/dir', self.metadata)

        self.dump.assert_called_once_with(self.metadata, self.file_handle, indent=2)
