import logging
import tempfile
import unittest
import warnings
from pathlib import Path
from unittest.mock import patch

from threatxmanager.logmanager.logmanager import LogManager


class DummyConfig:
    """
    Dummy configuration class for testing purposes.

    Parameters
    ----------
    logs_config : dict
        A dictionary with logging configuration.
    """

    def __init__(self, logs_config):
        self._logs_config = logs_config

    def get_section(self, section, env=None):
        """
        Retrieve a section of the configuration.

        Parameters
        ----------
        section : str
            The section key to retrieve.
        env : str, optional
            The environment key (default is None).

        Returns
        -------
        dict
            The configuration dictionary for the specified section.
        """
        if section == "logs":
            return self._logs_config
        return {}


class TestLogManager(unittest.TestCase):
    """
    Test suite for the LogManager class.

    This suite verifies:
        - Logger initialization with Sentry configuration.
        - Logger initialization without Sentry.
        - Correct forwarding of logging methods.
    """

    def setUp(self):
        """
        Reset the singleton instance before each test.
        """
        # Reset the singleton instance of LogManager.
        LogManager._instance = None  # pylint: disable=protected-access

        # Cria um arquivo temporário para log e armazena seu caminho.
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            self.temp_log_path = temp_file.name

    def tearDown(self):
        """
        Remove o arquivo de log temporário após cada teste.
        """
        log_file = Path(self.temp_log_path)
        if log_file.exists():
            log_file.unlink()

    @patch("threatxmanager.logmanager.logmanager.sentry_sdk.init")
    def test_logger_initialization_with_sentry(self, mock_sentry_init):
        """
        Test logger initialization when Sentry DSN is provided.

        It verifies that:
            - The logger level is set as expected.
            - sentry_sdk.init is called with correct parameters.
            - Logging handlers are configured.
        """
        logs_config = {
            "LOG_FILE": self.temp_log_path,
            "LOG_LEVEL": "WARNING",
            "SENTRY_DSN": "http://exampledsn",
        }
        dummy_config = DummyConfig(logs_config)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning)
            log_manager = LogManager(config_instance=dummy_config, env="test")
        logger = log_manager.get_logger()

        # Check that the logger level is set to WARNING.
        assert logger.level == logging.WARNING

        # Check that sentry_sdk.init was called with the correct parameters.
        mock_sentry_init.assert_called_once()
        call_args = mock_sentry_init.call_args[1]  # kwargs of the call
        assert call_args["dsn"] == "http://exampledsn"
        assert "integrations" in call_args

        # Verify that handlers are configured.
        assert len(logger.handlers) > 0

        # --- CLEANUP: Close and remove handlers ---
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)

    def test_logger_initialization_without_sentry(self):
        """
        Test logger initialization when Sentry DSN is not provided.

        It verifies that:
            - The logger level is set to DEBUG.
            - Logging handlers are configured.
        """
        logs_config = {"LOG_FILE": self.temp_log_path, "LOG_LEVEL": "DEBUG", "SENTRY_DSN": None}
        dummy_config = DummyConfig(logs_config)
        log_manager = LogManager(config_instance=dummy_config, env="test")
        logger = log_manager.get_logger()

        # Check that the logger level is set to DEBUG.
        assert logger.level == logging.DEBUG

        # Verify that handlers are configured.
        assert len(logger.handlers) > 0

        # --- CLEANUP: Close and remove handlers ---
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)

    def test_logging_methods(self):
        """
        Test that the LogManager logging methods forward messages to the underlying logger.

        It verifies that debug, info, warning, error, and critical methods are correctly invoked.
        """
        logs_config = {"LOG_FILE": self.temp_log_path, "LOG_LEVEL": "INFO", "SENTRY_DSN": None}
        dummy_config = DummyConfig(logs_config)
        log_manager = LogManager(config_instance=dummy_config, env="test")
        logger = log_manager.get_logger()

        # Patch the logger methods to verify that each method is called.
        with (
            unittest.mock.patch.object(logger, "debug") as mock_debug,
            unittest.mock.patch.object(logger, "info") as mock_info,
            unittest.mock.patch.object(logger, "warning") as mock_warning,
            unittest.mock.patch.object(logger, "error") as mock_error,
            unittest.mock.patch.object(logger, "critical") as mock_critical,
        ):
            log_manager.debug("debug message")
            log_manager.info("info message")
            log_manager.warning("warning message")
            log_manager.error("error message")
            log_manager.critical("critical message")

            mock_debug.assert_called_once_with("debug message")
            mock_info.assert_called_once_with("info message")
            mock_warning.assert_called_once_with("warning message")
            mock_error.assert_called_once_with("error message")
            mock_critical.assert_called_once_with("critical message")

        # --- CLEANUP: Close and remove handlers ---
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)


if __name__ == "__main__":
    unittest.main()
