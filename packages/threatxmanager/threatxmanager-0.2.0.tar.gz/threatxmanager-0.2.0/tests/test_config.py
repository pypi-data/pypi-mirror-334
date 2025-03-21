import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import toml

from threatxmanager.config.manager_config import Config


class TestConfig(unittest.TestCase):
    """
    Test suite for the Config class.


    This suite verifies:
        - The proper loading of configuration from a file.
        - Handling of missing or erroneous configuration files.
        - The functionality of getter, setter, and section retrieval methods.
        - The obfuscation of sensitive configuration values.
        - The singleton behavior and initialization of the Config instance.
    """

    def setUp(self):
        """
        Reset the singleton instance before each test.
        """
        Config._instance = None

    def tearDown(self):
        """
        Ensure that the singleton instance is reset after each test.
        """
        Config._instance = None

    def create_temp_config_file(self, config_dict):
        """
        Create a temporary configuration file with the given dictionary content in TOML format.

        Parameters
        ----------
        config_dict : dict
            The configuration data to be dumped into the file.

        Returns
        -------
        str
            The absolute path of the temporary file.
        """
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".toml", mode="w", encoding="utf-8"
        ) as temp_file:
            toml.dump(config_dict, temp_file)
            temp_file_path = temp_file.name
        return temp_file_path

    def test_load_config_success(self):
        """
        Test that _load_config returns the configuration content from the file when it exists.
        """
        config_data = {"key": "value", "default_env": "prod", "section": {"prod": {"a": 1}}}
        temp_config_path = self.create_temp_config_file(config_data)
        try:
            cfg = Config(temp_config_path)
            assert cfg.config == config_data
        finally:
            Path(temp_config_path).unlink()

    def test_load_config_file_not_found(self):
        """
        Test that _load_config returns an empty dictionary when the configuration file does not exist.
        """
        fake_path = "nonexistent_config.toml"
        cfg = Config(fake_path)
        assert cfg.config == {}

    def test_load_config_exception(self):
        """
        Test that _load_config returns an empty dictionary if an exception occurs while reading the file.
        """
        config_data = {"key": "value"}
        temp_config_path = self.create_temp_config_file(config_data)
        try:
            cfg = Config(temp_config_path)
            # Force an exception in toml.load to simulate a read error.
            with patch(
                "threatxmanager.config.manager_config.toml.load",
                side_effect=Exception("read error"),
            ):
                result = cfg._load_config()
                assert result == {}
        finally:
            Path(temp_config_path).unlink()

    def test_get_method(self):
        """
        Test that the get method returns the associated value or the default if it does not exist.
        """
        cfg = Config()
        cfg.config = {"foo": "bar"}
        assert cfg.get("foo") == "bar"
        assert cfg.get("nonexistent", "default") == "default"

    def test_get_default_env(self):
        """
        Test that get_default_env returns 'dev' if not defined, or the defined value if it exists.
        """
        cfg = Config()
        cfg.config = {}
        assert cfg.get_default_env() == "dev"
        cfg.config["default_env"] = "testenv"
        assert cfg.get_default_env() == "testenv"

    def test_get_section_success(self):
        """
        Test that get_section returns the configuration for the specified environment or default.
        """
        cfg = Config()
        cfg.config = {"logs": {"prod": {"a": "b"}, "dev": {"c": "d"}}, "default_env": "dev"}
        assert cfg.get_section("logs", "prod") == {"a": "b"}
        assert cfg.get_section("logs") == {"c": "d"}

    def test_get_section_environment_not_found(self):
        """
        Test that get_section returns {} and logs a warning if the environment is not found.
        """
        cfg = Config()
        cfg.config = {"logs": {"prod": {"a": "b"}}}
        with self.assertLogs(level="WARNING") as log:
            result = cfg.get_section("logs")
        assert result == {}
        assert any("Environment 'dev' not found" in message for message in log.output)

    def test_get_section_not_dict(self):
        """
        Test that get_section returns {} and logs a warning if the section is not a dictionary.
        """
        cfg = Config()
        cfg.config = {"logs": "not a dict"}
        with self.assertLogs(level="WARNING") as log:
            result = cfg.get_section("logs")
        assert result == {}
        assert any(
            "Section 'logs' is not in the expected dictionary format." in message
            for message in log.output
        )

    def test_set_method(self):
        """
        Test that the set method updates or adds a key to the configuration.
        """
        cfg = Config()
        cfg.config = {}
        cfg.set("new_key", "new_value")
        assert cfg.config["new_key"] == "new_value"

    def test_reload(self):
        """
        Test that reload re-loads the configuration from the file.

        It verifies that changes in the configuration file are reflected after calling reload.
        """
        initial_data = {"key": "initial"}
        temp_config_path = self.create_temp_config_file(initial_data)
        try:
            cfg = Config(temp_config_path)
            assert cfg.get("key") == "initial"
            # Update the file content.
            updated_data = {"key": "updated"}
            with Path(temp_config_path).open("w", encoding="utf-8") as f:
                toml.dump(updated_data, f)
            cfg.reload()
            assert cfg.get("key") == "updated"
        finally:
            Path(temp_config_path).unlink()

    def test_obfuscate_config_default(self):
        """
        Test that obfuscate_config masks sensitive keys recursively.

        Sensitive keys (e.g., DATABASE_URL, SENTRY_DSN, TOKEN, PASSWORD) should be obfuscated while non-sensitive keys remain unchanged.
        Specific checks:
            - TOKEN of length 10 should be masked as "******2345"
            - PASSWORD of length 4 should be masked as "****"
        """
        config_dict = {
            "DATABASE_URL": "postgresql://user:password@localhost/db",
            "SENTRY_DSN": "dsn_value_1234",
            "TOKEN": "abcde12345",  # len=10 -> should be "******2345"
            "PASSWORD": "pass",  # len=4 -> should be "****"
            "NON_SENSITIVE": "value",
            "nested": {"DATABASE_URL": "secretdata1234", "info": "detail"},
        }
        cfg = Config()
        cfg.config = config_dict
        obfuscated = cfg.obfuscate_config()
        # Sensitive keys should be modified.
        assert obfuscated["DATABASE_URL"] != config_dict["DATABASE_URL"]
        assert obfuscated["SENTRY_DSN"] != config_dict["SENTRY_DSN"]
        assert obfuscated["TOKEN"] != config_dict["TOKEN"]
        assert obfuscated["PASSWORD"] != config_dict["PASSWORD"]
        # Non-sensitive keys remain the same.
        assert obfuscated["NON_SENSITIVE"] == "value"
        # Nested values.
        assert obfuscated["nested"]["DATABASE_URL"] != config_dict["nested"]["DATABASE_URL"]
        assert obfuscated["nested"]["info"] == "detail"
        # Specific checks:
        assert obfuscated["TOKEN"] == "******2345"
        assert obfuscated["PASSWORD"] == "****"

    def test_obfuscate_config_custom_sensitive_keys(self):
        """
        Test that obfuscate_config with custom sensitive_keys (an empty set) does not mask any key.
        """
        config_dict = {"KEY": "value", "SECRET": "mysecret"}
        cfg = Config()
        cfg.config = config_dict
        obfuscated = cfg.obfuscate_config(sensitive_keys=set())
        assert obfuscated == config_dict

    def test_obfuscate_config_with_none_config(self):
        """
        Test that if config is None, obfuscate_config uses self.config.
        """
        config_dict = {"TOKEN": "abcdef123456"}
        cfg = Config()
        cfg.config = config_dict
        obfuscated = cfg.obfuscate_config(config=None)
        assert "TOKEN" in obfuscated
        assert obfuscated["TOKEN"] != config_dict["TOKEN"]

    def test_obfuscate_config_non_string(self):
        """
        Test that obfuscate_config does not modify values that are not strings.
        """
        cfg = Config()
        cfg.config = {"INTEGER": 123, "LIST": [1, 2, 3]}
        obfuscated = cfg.obfuscate_config()
        assert obfuscated["INTEGER"] == 123
        assert obfuscated["LIST"] == [1, 2, 3]

    def test_init_already_initialized(self):
        """
        Test that __init__ does not reconfigure if _initialized is already True.
        """
        config_data = {"key": "value"}
        temp_config_path = self.create_temp_config_file(config_data)
        try:
            cfg = Config(temp_config_path)
            original_config = cfg.config
            # Calling __init__ again should not alter cfg.config.
            cfg.__init__(temp_config_path)
            assert cfg.config is original_config
        finally:
            Path(temp_config_path).unlink()

    def test_init_with_default_config_file_not_exists(self):
        """
        Test the case where config_file is None.

        Patches Path to simulate that the default configuration file does not exist.
        """
        with patch("threatxmanager.config.manager_config.Path") as mock_path_class:
            mock_path_instance = mock_path_class.return_value
            # Simulate the construction of the default path: __file__.parent / "config.toml"
            mock_path_instance.__truediv__.return_value = mock_path_instance
            mock_path_instance.exists.return_value = False
            cfg = Config()  # config_file is None
            assert cfg.config == {}


if __name__ == "__main__":
    unittest.main()
