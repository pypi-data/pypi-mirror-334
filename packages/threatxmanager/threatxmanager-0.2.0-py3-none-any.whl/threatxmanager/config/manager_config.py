import builtins
import logging
from pathlib import Path
from typing import Any, Optional

import toml

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Config:
    """
    Singleton for centralized configuration management

    This class loads, accesses, updates, and obfuscates sensitive information
    contained in a configuration file.

    Attributes
    ----------
    config_file : Path
        The absolute path to the configuration file.
    config : Dict[str, Any]
        Dictionary containing the loaded configuration.
    _instance : Optional[Config]
        The singleton instance of the Config class.
    _initialized : bool
        Flag indicating whether the configuration has been initialized.
    """

    _instance: Optional["Config"] = None

    def __new__(cls, config_file: str | None = None) -> "Config":
        """
        Creates or returns the singleton instance of Config.

        Parameters
        ----------
        config_file : Optional[str], optional
            The path to the configuration file. If None, defaults to 'config.toml'
            in the same directory.

        Returns
        -------
        Config
            The singleton instance of the Config class.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, config_file: str | None = None) -> None:
        """
        Initializes the Config singleton by loading the configuration from a TOML file.

        Parameters
        ----------
        config_file : Optional[str], optional
            The path to the configuration file. If None, 'config.toml' in the same
            directory is used.
        """
        if self._initialized:
            return

        # Use 'config.toml' in the same directory if no file is provided.
        if config_file is None:
            config_path = Path(__file__).parent / "config.toml"
        else:
            config_path = Path(config_file)

        self.config_file: Path = config_path.resolve()
        self.config: dict[str, Any] = self._load_config()
        self._initialized = True

    def _load_config(self) -> dict[str, Any]:
        """
        Loads the configuration from a TOML file.

        If the file does not exist or an error occurs during reading, an empty
        dictionary is returned.

        Returns
        -------
        Dict[str, Any]
            The loaded configuration as a dictionary.
        """
        if self.config_file.exists():
            try:
                with self.config_file.open("r", encoding="utf-8") as f:
                    config_data = toml.load(f)
                    logger.info(f"Configurations loaded from file: {self.config_file}")
                    return config_data
            except Exception as e:
                logger.exception(f"Error loading configuration file '{self.config_file}': {e}")
        else:
            logger.warning(f"Configuration file '{self.config_file}' not found.")
        return {}

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieves the value associated with a key in the root of the configuration.

        Parameters
        ----------
        key : str
            The key to look up in the configuration.
        default : Any, optional
            The default value to return if the key is not found.

        Returns
        -------
        Any
            The value associated with the key, or the default if the key is absent.
        """
        return self.config.get(key, default)

    def get_default_env(self) -> str:
        """
        Returns the default environment defined in the configuration (key 'default_env').

        If not defined, 'dev' is returned.

        Returns
        -------
        str
            The default environment.
        """
        return self.get("default_env", "dev")

    def get_section(self, section: str, environment: str | None = None) -> dict[str, Any]:
        """
        Retrieves the configuration for a specific section and environment.

        If the 'environment' parameter is not provided, the default environment is used.

        Parameters
        ----------
        section : str
            The configuration section to retrieve.
        environment : Optional[str], optional
            The specific environment to retrieve the section for. Defaults to None.

        Returns
        -------
        Dict[str, Any]
            The configuration dictionary for the specified section and environment.
        """
        sec: Any = self.config.get(section, {})
        env: str = environment if environment else self.get_default_env()
        if isinstance(sec, dict):
            section_env: dict[str, Any] = sec.get(env, {})
            if not section_env:
                logger.warning(f"Environment '{env}' not found in section '{section}'.")
            return section_env
        logger.warning(f"Section '{section}' is not in the expected dictionary format.")
        return {}

    def set(self, key: str, value: Any) -> None:
        """
        Sets or updates the value of a key in the configuration.

        Parameters
        ----------
        key : str
            The key in the configuration.
        value : Any
            The value to set for the key.
        """
        self.config[key] = value

    def reload(self) -> None:
        """
        Reloads the configuration from the file.

        This method is useful when dynamic updates are made to the configuration file.
        """
        self.config = self._load_config()
        logger.info("Configurations reloaded successfully.")

    def obfuscate_config(
        self, config: dict[str, Any] | None = None, sensitive_keys: builtins.set[str] | None = None
    ) -> dict[str, Any]:
        """
        Returns a copy of the configuration with sensitive key values obfuscated.

        Parameters
        ----------
        config : Optional[Dict[str, Any]], optional
            The configuration dictionary to obfuscate. If None, uses self.config.
        sensitive_keys : Optional[Set[str]], optional
            A set of sensitive keys whose values should be masked.
            Defaults to {"DATABASE_URL", "SENTRY_DSN", "TOKEN", "PASSWORD"}.

        Returns
        -------
        Dict[str, Any]
            The configuration dictionary with sensitive data obfuscated.
        """
        if sensitive_keys is None:
            sensitive_keys = {"DATABASE_URL", "SENTRY_DSN", "TOKEN", "PASSWORD"}

        if config is None:
            config = self.config

        def mask(value: str) -> str:
            """
            Masks a string value by displaying only its last 4 characters.

            Parameters
            ----------
            value : str
                The string to mask.

            Returns
            -------
            str
                The masked string.
            """
            if isinstance(value, str) and len(value) > 4:
                return "*" * (len(value) - 4) + value[-4:]
            return "****"

        def _obfuscate(d: dict[str, Any]) -> dict[str, Any]:
            """
            Recursively obfuscates sensitive data in a dictionary.

            Parameters
            ----------
            d : Dict[str, Any]
                The dictionary to obfuscate.

            Returns
            -------
            Dict[str, Any]
                The obfuscated dictionary.
            """
            new_dict: dict[str, Any] = {}
            for key, value in d.items():
                if key.upper() in sensitive_keys and isinstance(value, str):
                    new_dict[key] = mask(value)
                elif isinstance(value, dict):
                    new_dict[key] = _obfuscate(value)
                else:
                    new_dict[key] = value
            return new_dict

        return _obfuscate(config)
