from boxfile_manager.manage_catalog import create_catalog
from boxfile_manager.tests.testcase import TestCase


class TestCreateCatalog(TestCase):
    def setUp(self):
        self.list_boxes = self.set_up_patch('boxfile_manager.manage_catalog.list_boxes')
        self.parse_boxes = self.set_up_patch('boxfile_manager.manage_catalog.parse_boxes')
        self.write_catalog = self.set_up_patch('boxfile_manager.manage_catalog.write_catalog')

    def test_create_catalog_lists_boxes(self):
        create_catalog()

        self.list_boxes.assert_called_once_with()

    def test_create_catalog_parsers_boxes(self):
        create_catalog()

        self.parse_boxes.assert_called_once_with(
            self.list_boxes.return_value
        )

    def test_create_catalog_writes_catalog(self):
        create_catalog()

        self.write_catalog.assert_called_once_with(
            self.parse_boxes.return_value
        )
