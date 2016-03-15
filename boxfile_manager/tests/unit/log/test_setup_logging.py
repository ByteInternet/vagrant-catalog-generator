from logging import INFO, DEBUG
from sys import stdout

from boxfile_manager.log import setup_logging
from boxfile_manager.tests.testcase import TestCase


class TestSetupLogging(TestCase):
    def setUp(self):
        self.getlogger = self.set_up_patch('boxfile_manager.log.getLogger')
        self.streamhandler = self.set_up_patch('boxfile_manager.log.StreamHandler')

    def test_setup_logging_gets_logger(self):
        setup_logging()

        self.getlogger.assert_called_once_with('hypernode-boxfile-manager')

    def test_setup_logging_sets_default_logging_level(self):
        setup_logging()

        self.getlogger.return_value.setLevel.assert_called_once_with(
            INFO
        )

    def test_setup_logging_sets_logging_level(self):
        setup_logging(level=DEBUG)

        self.getlogger.return_value.setLevel.assert_called_once_with(
            DEBUG
        )

    def test_setup_logging_configures_streamhandler(self):
        setup_logging()

        self.streamhandler.assert_called_once_with(stdout)

    def test_setup_logging_adds_console_handler_to_logger(self):
        setup_logging()

        self.getlogger.return_value.addHandler.assert_called_once_with(
            self.streamhandler.return_value
        )

    def test_setup_logging_returns_logger(self):
        ret = setup_logging()

        self.assertEqual(ret, self.getlogger.return_value, ret)

