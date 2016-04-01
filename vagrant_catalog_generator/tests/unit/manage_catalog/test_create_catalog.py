from vagrant_catalog_generator.manage_catalog import create_catalog
from vagrant_catalog_generator.tests.testcase import TestCase


class TestCreateCatalog(TestCase):
    def setUp(self):
        self.list_boxes = self.set_up_patch('vagrant_catalog_generator.manage_catalog.list_boxes')
        self.parse_boxes = self.set_up_patch('vagrant_catalog_generator.manage_catalog.parse_boxes')
        self.generate_metadata = self.set_up_patch('vagrant_catalog_generator.manage_catalog.generate_metadata')
        self.write_catalog = self.set_up_patch('vagrant_catalog_generator.manage_catalog.write_catalog')

    def test_create_catalog_lists_boxes(self):
        create_catalog('https://example.com', '/some/dir', 'my vagrant box', 'hypernode')

        self.list_boxes.assert_called_once_with('hypernode', '/some/dir')

    def test_create_catalog_parses_boxes(self):
        create_catalog('https://example.com', '/some/dir', 'my vagrant box', 'hypernode')

        self.parse_boxes.assert_called_once_with(
            self.list_boxes.return_value,
            'https://example.com',
            '/some/dir',
            'hypernode'
        )

    def test_create_catalog_generates_metadata(self):
        create_catalog('https://example.com', '/some/dir', 'my vagrant box', 'hypernode')

        self.generate_metadata.assert_called_once_with(self.parse_boxes.return_value, 'hypernode', 'my vagrant box')

    def test_create_catalog_writes_catalog(self):
        create_catalog('https://example.com', '/some/dir', 'my vagrant box', 'hypernode')

        self.write_catalog.assert_called_once_with(
            '/some/dir',
            self.generate_metadata.return_value
        )
