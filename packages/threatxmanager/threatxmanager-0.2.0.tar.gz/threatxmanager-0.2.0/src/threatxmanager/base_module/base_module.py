from abc import ABC, abstractmethod
from typing import Any

from threatxmanager.config.manager_config import Config
from threatxmanager.dbmanager.connection import DBManager
from threatxmanager.logmanager.logmanager import LogManager


class BaseModule(ABC):
    """
    Abstract base class for modules that use dependency injection for configuration,
    logging, and database management

    This class provides common functionalities for initializing and managing the essential
    components of a module. Derived classes must implement the `run` method to execute
    module-specific logic.

    Attributes
    ----------
    config : Config
        Instance of the configuration manager.
    log_manager : LogManager
        Instance of the log manager.
    logger : Any
        Logger specific to the module, used for logging messages and events.
    info : Dict[str, Any]
        Dictionary containing metadata and dynamic information about the module.
    module_config : Dict[str, Any]
        Dictionary with the module-specific configuration loaded from the 'modules' section
        of the configuration file.
    db_manager : DBManager
        Instance of the database manager.
    """

    def __init__(
        self,
        config_instance: Config | None = None,
        log_manager_instance: LogManager | None = None,
        db_instance: DBManager | None = None,
        env: str | None = None,
    ) -> None:
        """
        Initializes the base module with dependency injection for configuration, logging,
        and database management. If not provided, default singleton instances will be used.

        Parameters
        ----------
        config_instance : Optional[Config], optional
            Instance of the configuration manager. If None, a new instance of `Config` is created.
        log_manager_instance : Optional[LogManager], optional
            Instance of the log manager. If None, a new instance of `LogManager` is created using
            the configuration and environment.
        db_instance : Optional[DBManager], optional
            Instance of the database manager. If None, a new instance of `DBManager` is created
            and initialized.
        env : Optional[str], optional
            Environment identifier. If None, the default environment defined in the configuration is used.

        Returns
        -------
        None


        """
        self.config: Config = config_instance if config_instance is not None else Config()
        env = env if env is not None else self.config.get_default_env()

        # Create or use a log manager instance.
        self.log_manager: LogManager = (
            log_manager_instance
            if log_manager_instance is not None
            else LogManager(self.config, env)
        )
        self.logger = self.log_manager.get_logger().getChild(self.__class__.__name__)
        self.logger.info(f"[{self.__class__.__name__}] Base module instantiated.")
        self.info: dict[str, Any] = {}

        # Load module-specific configuration.
        self.module_config: dict[str, Any] = self.load_module_config()

        # Create or inject a database management instance.
        if db_instance is not None:
            self.db_manager: DBManager = db_instance
            self.logger.debug("Database instance injected.")
        else:
            self.db_manager = DBManager(self.config, env)
            self.db_manager.init_db(self.get_base())
            self.logger.debug("Database instance created and initialized.")

    def update_info(self, info: dict[str, Any]) -> dict[str, Any]:
        """
        Updates the module metadata with the provided dictionary.

        Parameters
        ----------
        info : Dict[str, Any]
            Dictionary containing metadata to update for the module.

        Returns
        -------
        Dict[str, Any]
            The updated module metadata dictionary.


        """
        self.info.update(info)
        self.logger.debug(f"Module information updated: {self.info}")
        return self.info

    def load_module_config(self) -> dict[str, Any]:
        """
        Loads and validates the module configuration from the global configuration's 'modules'
        section. The module's class name is used as the key. Warnings are logged if the configuration
        is missing or if expected fields are empty.

        Returns
        -------
        Dict[str, Any]
            A copy of the module-specific configuration dictionary.


        """
        modules_config: dict[str, Any] = self.config.get("modules", {})
        module_name: str = self.__class__.__name__
        config_data: dict[str, Any] = modules_config.get(module_name, {})
        if not config_data:
            self.logger.warning(f"No configuration found for module '{module_name}'.")
        else:
            for key, value in config_data.items():
                if value in [None, ""]:
                    self.logger.warning(
                        f"The configuration field '{key}' for module '{module_name}' is empty."
                    )
        return config_data.copy()  # Return a copy for dynamic modifications.

    def get_safe_module_config(self) -> dict[str, Any]:
        """
        Returns an obfuscated copy of the module configuration for logging purposes,
        preventing exposure of sensitive data.

        Returns
        -------
        Dict[str, Any]
            The module configuration with sensitive data obfuscated.


        """
        safe_config: dict[str, Any] = self.config.obfuscate_config(self.module_config)
        return safe_config

    def get_base(self) -> Any:
        """
        Returns the ORM declarative base used for database operations.

        Returns
        -------
        Any
            The declarative base class (usually named 'Base') used to define ORM models.


        """
        from threatxmanager.dbmanager.models import Base

        return Base

    def __str__(self) -> str:
        """
        Generates a string representation of the module, including its class name,
        loaded configuration, and metadata.

        Returns
        -------
        str
            String representation of the module.


        """
        return f"Module: {self.__class__.__name__}\nConfig: {self.module_config}\nInfo: {self.info}"

    @abstractmethod
    def run(self) -> None:
        """
        Abstract method that must be implemented by derived classes to execute
        module-specific logic.

        Returns
        -------
        None

        Raises
        ------
        NotImplementedError
            If the method is not implemented in the derived class.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def set_parameter(self, key: str, value: str) -> None:
        """
        Sets or updates a parameter in the module's configuration.
        If the key already exists in the loaded configuration, its value is updated;
        otherwise, the key is added.

        Parameters
        ----------
        key : str
            The key of the configuration parameter.
        value : str
            The new value for the parameter.

        Returns
        -------
        None

        """
        if key in self.module_config:
            self.module_config[key] = value
            self.logger.debug(f"Module configuration '{key}' updated to '{value}'.")
        else:
            self.module_config[key] = value
            self.logger.debug(f"Module configuration '{key}' added with value '{value}'.")
