from vagrant_catalog_generator.manage_catalog import generate_metadata
from vagrant_catalog_generator.tests.testcase import TestCase


class TestGenerateMetaData(TestCase):
    def setUp(self):
        self.combine_provider_version = self.set_up_patch('vagrant_catalog_generator.manage_catalog.combine_provider_versions')
        self.boxes_metadata = [{}, {}]

    def test_generate_metadata_combines_provider_versions(self):
        generate_metadata(self.boxes_metadata, 'my_vagrant_box', 'my vagrant box description')

        self.combine_provider_version.assert_called_once_with(self.boxes_metadata)

    def test_generate_metadata_returns_metadata(self):
        ret = generate_metadata(self.boxes_metadata, 'my_vagrant_box', 'my vagrant box description')

        self.assertEqual(ret, {
            'description': 'my vagrant box description',
            'name': 'my_vagrant_box',
            'versions': self.combine_provider_version.return_value
        })
