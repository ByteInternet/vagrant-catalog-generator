from vagrant_catalog_generator.manage_catalog import combine_provider_versions
from vagrant_catalog_generator.tests.testcase import TestCase


class TestCombineProviderVersions(TestCase):
    def setUp(self):
        self.input_fixture = [{
            "version": "2744",
            "providers": [{
                "url": "http://vagrant.example.com/php7/hypernode_php7.virtualbox.release-2744.box",
                "checksum_type": "sha256",
                "name": "virtualbox",
                "checksum": "8d94e34aa794122cbd2c92b11d5f31b3a2ca475af97a4ef588c3ea15c9106b44"
            }]
        }, {
            "version": "2743",
            "providers": [{
                "url": "http://vagrant.example.com/php7/hypernode_php7.virtualbox.release-2743.box",
                "checksum_type": "sha256",
                "name": "virtualbox",
                "checksum": "f44fe22de5ddfdadb4ac1c2c772098b81c92dc1914f83cbad2f9a47f91e2fe3a"
            }]
        }, {
            "version": "2743",
            "providers": [{
                "url": "http://vagrant.example.com/php7/hypernode_php7.lxc.release-2743.box",
                "checksum_type": "sha256",
                "name": "lxc",
                "checksum": "f9289bbcc11e9abecb67d3185c6831498806e12b08c6394473fc36f9ca2b5897"
            }]
        }]

        self.output_fixture = [{
            'providers': [{
                'checksum_type': 'sha256',
                'url': 'http://vagrant.example.com/php7/hypernode_php7.virtualbox.release-2743.box',
                'name': 'virtualbox',
                'checksum': 'f44fe22de5ddfdadb4ac1c2c772098b81c92dc1914f83cbad2f9a47f91e2fe3a'
            }, {
                'checksum_type': 'sha256',
                'url': 'http://vagrant.example.com/php7/hypernode_php7.lxc.release-2743.box',
                'name': 'lxc',
                'checksum': 'f9289bbcc11e9abecb67d3185c6831498806e12b08c6394473fc36f9ca2b5897'
            }],
            'version': '2743'
        }, {
            'providers': [{
                'checksum_type': 'sha256',
                'url': 'http://vagrant.example.com/php7/hypernode_php7.virtualbox.release-2744.box',
                'name': 'virtualbox',
                'checksum': '8d94e34aa794122cbd2c92b11d5f31b3a2ca475af97a4ef588c3ea15c9106b44'
            }],
            'version': '2744'
        }]

    def test_combine_provider_versions_combines_provider_versions(self):
        self.maxDiff = None
        ret = combine_provider_versions(self.input_fixture)

        self.assertEqual(ret, self.output_fixture)
