from logging import INFO

from boxfile_manager.log import setup_logging
from boxfile_manager.tests.testcase import TestCase


class TestSetupLogging(TestCase):
    def setUp(self):
        self.logging = self.set_up_patch('boxfile_manager.log.logging')

    def test_setup_logging_gets_logger(self):
        setup_logging()

        self.logging.getLogger.assert_called_once_with('hypernode-boxfile-manager')

    def test_setup_logging_defines_basic_config(self):
        setup_logging()

        self.logging.basicConfig.assert_called_once_with(level=INFO, format='%(message)s')

    def test_setup_logging_returns_logger(self):
        ret = setup_logging()

        self.assertEqual(ret, self.logging.getLogger.return_value)

