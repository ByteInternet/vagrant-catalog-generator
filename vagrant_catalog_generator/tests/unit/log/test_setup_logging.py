from logging import INFO

from vagrant_catalog_generator.log import setup_logging
from vagrant_catalog_generator.tests.testcase import TestCase


class TestSetupLogging(TestCase):
    def setUp(self):
        self.logging = self.set_up_patch('vagrant_catalog_generator.log.logging')

    def test_setup_logging_gets_logger(self):
        setup_logging()

        self.logging.getLogger.assert_called_once_with('vagrant-catalog-generator')

    def test_setup_logging_defines_basic_config(self):
        setup_logging()

        self.logging.basicConfig.assert_called_once_with(level=INFO, format='%(message)s')

    def test_setup_logging_returns_logger(self):
        ret = setup_logging()

        self.assertEqual(ret, self.logging.getLogger.return_value)

