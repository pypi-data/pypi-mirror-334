import logging
from typing import Optional

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

from threatxmanager.config.manager_config import Config


class LogManager:
    """
    Singleton class for centralized logging management.

    This class configures and manages the logging system, including Sentry integration
    for error tracking. It retrieves logging configurations from a Config instance
    and sets up log handlers for both file and console logging.

    Attributes
    ----------
    logger : logging.Logger
        The logger instance used for logging messages.
    log_file : str
        Path to the log file.
    level : int
        Logging level (e.g., logging.DEBUG, logging.INFO).
    sentry_dsn : Optional[str]
        Sentry DSN for error tracking, if provided in the configuration.
    _instance : Optional[LogManager]
        The singleton instance of LogManager.
    _initialized : bool
        Flag indicating whether the LogManager instance has been initialized.
    """

    _instance: Optional["LogManager"] = None

    def __new__(cls, config_instance: Config | None = None, env: str | None = None) -> "LogManager":
        """
        Creates or returns the singleton instance of LogManager.

        Parameters
        ----------
        config_instance : Optional[Config], optional
            An instance of the configuration manager. If None, a new instance of Config is created.
        env : Optional[str], optional
            The environment identifier to fetch environment-specific logging configuration.

        Returns
        -------
        LogManager
            The singleton instance of LogManager.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, config_instance: Config | None = None, env: str | None = None) -> None:
        """
        Initializes the LogManager by setting up logging configurations and handlers.

        Parameters
        ----------
        config_instance : Optional[Config], optional
            An instance of the configuration manager. If None, a new Config instance is used.
        env : Optional[str], optional
            The environment identifier to fetch environment-specific logging configuration.
        """
        if self._initialized:
            return

        config = config_instance if config_instance is not None else Config()
        # Get logging configuration for the desired environment.
        log_config = config.get_section("logs", env)
        self.log_file: str = log_config.get("LOG_FILE", "app.log")
        level_str: str = log_config.get("LOG_LEVEL", "DEBUG")
        self.level: int = getattr(logging, level_str.upper(), logging.DEBUG)
        self.sentry_dsn: str | None = log_config.get("SENTRY_DSN", None)

        if self.sentry_dsn:
            sentry_logging = LoggingIntegration(
                level=self.level,  # Capture debug-level logs as breadcrumbs.
                event_level=logging.ERROR,  # Send error-level logs as events.
            )
            sentry_sdk.init(dsn=self.sentry_dsn, integrations=[sentry_logging])

        self.logger: logging.Logger = logging.getLogger("AppLogger")
        self.logger.setLevel(self.level)
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(levelname)s - %(name)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )

        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(self.level)
        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(self.level)
        stream_handler.setFormatter(formatter)

        if not self.logger.handlers:
            self.logger.addHandler(file_handler)
            self.logger.addHandler(stream_handler)

        self._initialized = True

    def get_logger(self) -> logging.Logger:
        """
        Returns the logger instance.

        Returns
        -------
        logging.Logger
            The logger used for logging messages.
        """
        return self.logger

    def debug(self, msg: str, *args, **kwargs) -> None:
        """
        Logs a debug-level message.

        Parameters
        ----------
        msg : str
            The message to log.
        *args
            Variable length argument list.
        **kwargs
            Arbitrary keyword arguments.
        """
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg: str, *args, **kwargs) -> None:
        """
        Logs an info-level message.

        Parameters
        ----------
        msg : str
            The message to log.
        *args
            Variable length argument list.
        **kwargs
            Arbitrary keyword arguments.
        """
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs) -> None:
        """
        Logs a warning-level message.

        Parameters
        ----------
        msg : str
            The message to log.
        *args
            Variable length argument list.
        **kwargs
            Arbitrary keyword arguments.
        """
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs) -> None:
        """
        Logs an error-level message.

        Parameters
        ----------
        msg : str
            The message to log.
        *args
            Variable length argument list.
        **kwargs
            Arbitrary keyword arguments.
        """
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg: str, *args, **kwargs) -> None:
        """
        Logs a critical-level message.

        Parameters
        ----------
        msg : str
            The message to log.
        *args
            Variable length argument list.
        **kwargs
            Arbitrary keyword arguments.
        """
        self.logger.critical(msg, *args, **kwargs)
