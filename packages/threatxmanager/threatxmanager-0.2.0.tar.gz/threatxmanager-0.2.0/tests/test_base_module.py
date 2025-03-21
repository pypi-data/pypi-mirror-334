import sys
import types
import unittest
from unittest.mock import MagicMock, patch

from threatxmanager.base_module.base_module import BaseModule

# For testing the get_base method, we simulate the module threatxmanager.dbmanager.models
# with an attribute 'Base'. This dummy module will be used in place of the real one
dummy_models = types.ModuleType("threatxmanager.dbmanager.models")
dummy_models.Base = object  # can be any dummy object
sys.modules["threatxmanager.dbmanager.models"] = dummy_models


class DummyModule(BaseModule):
    """
    Dummy implementation of BaseModule to allow instantiation for tests.

    Methods
    -------
    run()
        Dummy run method implementation.
    """

    def run(self):
        pass


class TestBaseModule(unittest.TestCase):
    """
    Test suite for the BaseModule functionality.

    This suite verifies:
        - That the injected instances (config, logger, and DBManager) are correctly used.
        - That module configuration is loaded and updated correctly.
        - That warnings are issued for empty configuration fields.
        - That configuration obfuscation works as expected.
        - That the DBManager is properly initialized when not injected.
        - That the string representation and parameter setting work as intended.
    """

    def setUp(self):
        """
        Set up the test environment.

        Creates dummy instances for configuration, logging, and DBManager,
        and instantiates DummyModule with these dummy dependencies.
        """
        # Create dummy configuration
        self.mock_config = MagicMock()
        self.mock_config.get_default_env.return_value = "test_env"

        def get_side_effect(key, default):
            if key == "modules":
                return {"DummyModule": {"param1": "value1", "param2": "value2"}}
            return default

        self.mock_config.get.side_effect = get_side_effect

        # Simulate simple obfuscation: transforms all values to "****"
        self.mock_config.obfuscate_config.side_effect = lambda config: {k: "****" for k in config}

        # Create a dummy logger; getChild returns the same logger instance
        self.mock_logger = MagicMock()
        self.mock_logger.getChild.return_value = self.mock_logger

        # Dummy log manager that returns the dummy logger
        self.mock_log_manager = MagicMock()
        self.mock_log_manager.get_logger.return_value = self.mock_logger

        # Dummy DBManager (functionality is not needed for these tests)
        self.mock_db_manager = MagicMock()
        self.mock_db_manager.init_db = MagicMock()

        # Instantiate the DummyModule with the injected dummy dependencies
        self.module = DummyModule(
            config_instance=self.mock_config,
            log_manager_instance=self.mock_log_manager,
            db_instance=self.mock_db_manager,
            env="test_env",
        )

    def test_initialization_injected_instances(self):
        """
        Test that injected instances are correctly used.

        Ensures that the injected configuration, log manager, and DBManager are
        assigned properly and that a log message indicating instantiation is generated.
        """
        assert self.module.config == self.mock_config
        assert self.module.log_manager == self.mock_log_manager
        assert self.module.db_manager == self.mock_db_manager
        self.mock_logger.info.assert_called_with("[DummyModule] Base module instantiated.")

    def test_update_info(self):
        """
        Test update_info method.

        Verifies that update_info correctly updates the module's information dictionary.
        """
        initial_info = self.module.info.copy()
        new_info = {"key": "value"}
        updated_info = self.module.update_info(new_info)
        expected = {**initial_info, **new_info}
        assert updated_info == expected
        self.mock_logger.debug.assert_called_with(f"Module information updated: {expected}")

    def test_load_module_config(self):
        """
        Test load_module_config method.

        Checks that load_module_config returns the correct configuration for the module.
        """
        config_data = self.module.load_module_config()
        expected = {"param1": "value1", "param2": "value2"}
        assert config_data == expected

    def test_load_module_config_empty_fields(self):
        """
        Test load_module_config with empty configuration fields.

        Simulates the scenario where the module configuration exists but contains empty
        fields (None or empty string), which should trigger warnings.
        """
        # Simulate that the "modules" section has keys with empty values
        self.mock_config.get.side_effect = lambda key, default: (
            {"DummyModule": {"param1": "", "param2": None}} if key == "modules" else default
        )
        module_instance = DummyModule(
            config_instance=self.mock_config,
            log_manager_instance=self.mock_log_manager,
            db_instance=self.mock_db_manager,
            env="test_env",
        )
        config_data = module_instance.load_module_config()
        expected = {"param1": "", "param2": None}
        assert config_data == expected
        # Verify that warnings were issued for the empty fields
        warning_messages = [args[0] for args, _ in self.mock_logger.warning.call_args_list]
        assert any("param1" in msg for msg in warning_messages)
        assert any("param2" in msg for msg in warning_messages)

    def test_get_safe_module_config(self):
        """
        Test get_safe_module_config method.

        Verifies that get_safe_module_config correctly obfuscates the module configuration.
        """
        safe_config = self.module.get_safe_module_config()
        expected = {k: "****" for k in self.module.module_config}
        assert safe_config == expected
        self.mock_config.obfuscate_config.assert_called_once_with(self.module.module_config)

    def test_get_base(self):
        """
        Test get_base method.

        Checks that get_base returns the Base defined in the dummy module.
        """
        base = self.module.get_base()
        from threatxmanager.dbmanager.models import Base

        assert base == Base

    def test_str(self):
        """
        Test the string representation (__str__ method).

        Verifies that the string representation of the module includes the expected information.
        """
        self.module.module_config = {"param1": "value1"}
        self.module.info = {"info_key": "info_value"}
        s = str(self.module)
        assert "DummyModule" in s
        assert "param1" in s
        assert "info_key" in s

    def test_set_parameter_existing(self):
        """
        Test updating an existing parameter using set_parameter.

        Ensures that updating a parameter already in the configuration works and logs the update.
        """
        self.module.module_config = {"param1": "value1"}
        self.module.set_parameter("param1", "new_value")
        assert self.module.module_config["param1"] == "new_value"
        self.mock_logger.debug.assert_called_with(
            "Module configuration 'param1' updated to 'new_value'."
        )

    def test_set_parameter_new(self):
        """
        Test adding a new parameter using set_parameter.

        Checks that a new parameter can be added to the module configuration and that a log message is generated.
        """
        self.module.module_config = {}
        self.module.set_parameter("param_new", "value_new")
        assert self.module.module_config["param_new"] == "value_new"
        self.mock_logger.debug.assert_called_with(
            "Module configuration 'param_new' added with value 'value_new'."
        )

    def test_db_manager_initialization_when_not_injected(self):
        """
        Test DBManager initialization when no instance is injected.

        Verifies that if db_instance is None, a new DBManager is created and its init_db method is called
        with the Base returned by get_base.
        """
        dummy_db_manager = MagicMock()
        dummy_db_manager.init_db = MagicMock()
        # Patch the __new__ method of DBManager to return the dummy instance
        with patch(
            "threatxmanager.dbmanager.connection.DBManager.__new__",
            lambda cls, *args, **kwargs: dummy_db_manager,
        ):
            module_instance = DummyModule(
                config_instance=self.mock_config,
                log_manager_instance=self.mock_log_manager,
                db_instance=None,
                env="test_env",
            )
            dummy_db_manager.init_db.assert_called_once_with(module_instance.get_base())
            assert module_instance.db_manager == dummy_db_manager

    def test_run_method(self):
        """
        Test the run method of DummyModule.

        Ensures that the run method can be called without raising any exceptions.
        """
        try:
            self.module.run()
        except Exception as e:
            self.fail(f"run() raised an exception: {e}")


if __name__ == "__main__":
    unittest.main()
