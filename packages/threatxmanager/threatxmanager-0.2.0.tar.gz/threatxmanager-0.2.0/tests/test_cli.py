import json
import unittest
from unittest.mock import MagicMock, patch

from prompt_toolkit.completion import NestedCompleter
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Import functions, constants, and classes from the CLI module.
from threatxmanager.cli import (
    THREATMANAGER_VERSION,
    ThreatXCLI,
    get_version,
)


# --- Custom exception to simulate errors in modules ---
class FaultyModuleError(Exception):
    """Custom exception used to simulate module errors."""


# --- Dummy Modules to simulate external modules ---
class DummyMyModule:
    """
    Dummy module to simulate a module for testing purposes.

    Attributes
    ----------
    module_config : dict
        Module configuration dictionary.
    info : dict
        Module information.
    """

    def __init__(self):
        self.module_config = {"my_key": "my_value"}
        self.info = {"Description": "My module info"}

    def run(self):
        """Dummy run method."""

    def set_parameter(self, key, value):
        """
        Set a parameter in the module configuration.

        Parameters
        ----------
        key : str
            The parameter key.
        value : any
            The new value for the parameter.
        """
        self.module_config[key] = value


class DummySalesModule:
    """
    Dummy module to simulate a sales module for testing purposes.

    Attributes
    ----------
    module_config : dict
        Module configuration dictionary.
    info : dict
        Module information.
    """

    def __init__(self):
        self.module_config = {"sales_key": "sales_value"}
        self.info = {"Description": "Sales module info"}

    def run(self):
        """Dummy run method."""

    def set_parameter(self, key, value):
        """
        Set a parameter in the module configuration.

        Parameters
        ----------
        key : str
            The parameter key.
        value : any
            The new value for the parameter.
        """
        self.module_config[key] = value


# --- Tests for the get_version function ---
class TestGetVersion(unittest.TestCase):
    """
    Test suite for the get_version function.
    """

    @patch("threatxmanager.cli.Path")
    @patch("threatxmanager.cli.toml.load")
    def test_get_version_success(self, mock_toml_load, mock_path):
        """
        Test that get_version returns the correct version when the version file exists.

        Parameters
        ----------
        mock_toml_load : MagicMock
            Mock for toml.load.
        mock_path : MagicMock
            Mock for Path.
        """
        fake_path = MagicMock()
        fake_path.exists.return_value = True
        mock_path.return_value = fake_path
        mock_toml_load.return_value = {"project": {"version": "1.2.3"}}
        assert get_version() == "1.2.3"

    @patch("threatxmanager.cli.Path")
    def test_get_version_file_not_exist(self, mock_path):
        """
        Test that get_version returns 'Unknown' when the version file does not exist.

        Parameters
        ----------
        mock_path : MagicMock
            Mock for Path.
        """
        fake_path = MagicMock()
        fake_path.exists.return_value = False
        mock_path.return_value = fake_path
        assert get_version() == "Unknown"

    @patch("threatxmanager.cli.toml.load", side_effect=Exception("error"))
    @patch("threatxmanager.cli.Path")
    def test_get_version_exception(self, mock_path, mock_toml_load):
        """
        Test that get_version returns 'Unknown' when an exception occurs during file loading.

        Parameters
        ----------
        mock_path : MagicMock
            Mock for Path.
        mock_toml_load : MagicMock
            Mock for toml.load that raises an exception.
        """
        fake_path = MagicMock()
        fake_path.exists.return_value = True
        mock_path.return_value = fake_path
        assert get_version() == "Unknown"


# --- Tests for the ThreatXCLI class ---
class TestThreatXCLI(unittest.TestCase):
    """
    Test suite for the ThreatXCLI class.
    """

    def setUp(self):
        """
        Set up the test environment.

        Patches the PromptSession to avoid console errors (especially on Windows),
        creates dummy configuration, dummy console, and injects dummy modules.
        """
        # Patch PromptSession to avoid console issues
        patcher = patch("threatxmanager.cli.PromptSession")
        self.addCleanup(patcher.stop)
        self.mock_prompt_session = patcher.start()
        dummy_session = MagicMock()
        dummy_session.prompt = MagicMock()
        self.mock_prompt_session.return_value = dummy_session
        self.dummy_session = dummy_session

        # Dummy configuration: returns default environment and settings for "database" and "modules".
        self.dummy_config = MagicMock()
        self.dummy_config.get_default_env.return_value = "test"
        self.dummy_config.get.side_effect = lambda key, default=None: {
            "database": {
                "bancode_dados": {
                    "test": {
                        "DATABASE_URL": "sqlite:///test.db",
                        "POOL_SIZE": 5,
                        "MAX_OVERFLOW": 10,
                    }
                }
            },
            "modules": {
                "SalesModule": {"sales_param": "value1"},
                "MyModule": {"my_param": "value2"},
            },
        }.get(key, default)
        self.dummy_config.obfuscate_config.side_effect = lambda config: {k: "****" for k in config}

        # Create dummy console.
        self.dummy_console = MagicMock()

        # Instantiate the CLI by injecting the dummy configuration.
        self.cli = ThreatXCLI(config_instance=self.dummy_config)
        self.cli.console = self.dummy_console
        self.cli.session = self.dummy_session
        # Force the module mapping with our dummy modules.
        self.cli.modules = {"SalesModule": DummySalesModule, "MyModule": DummyMyModule}

    def test_print_startup_info(self):
        """
        Test that print_startup_info prints the correct startup messages.
        """
        with patch("secrets.choice", return_value="Test startup message"):
            self.cli.print_startup_info()
            printed_first = self.dummy_console.print.call_args_list[0][0][0]
            printed_second = self.dummy_console.print.call_args_list[1][0][0]
            assert "[bold green]Test startup message[/bold green]" in printed_first
            assert "[bold blue]Loaded 2 modules.[/bold blue]" in printed_second

    def test_get_rprompt_valid(self):
        """
        Test that get_rprompt returns a valid prompt string including the database info and version.
        """
        rprompt = self.cli.get_rprompt()
        assert "test.db" in rprompt
        assert "sqlite" in rprompt
        assert THREATMANAGER_VERSION in rprompt

    def test_get_rprompt_exception(self):
        """
        Test that get_rprompt returns an error message when there is an exception retrieving the database configuration.
        """
        self.dummy_config.get.side_effect = (
            lambda key, default=None: {} if key == "database" else default
        )
        rprompt = self.cli.get_rprompt()
        assert "DB: Error" in rprompt
        assert "Error" in rprompt

    def test_update_prompt(self):
        """
        Test that update_prompt updates the CLI prompt based on the current module.
        """
        self.cli.current_module_name = "SalesModule"
        self.cli.update_prompt()
        assert self.cli.prompt == "threatxmanager(SalesModule)> "
        self.cli.current_module_name = None
        self.cli.update_prompt()
        assert self.cli.prompt == "threatxmanager> "

    def test_update_completer(self):
        """
        Test that update_completer updates the command completer with module-specific parameters.
        """
        dummy_module = DummySalesModule()
        dummy_module.module_config = {"key1": "val1", "key2": "val2"}
        self.cli.current_module = dummy_module
        self.cli.update_completer()
        expected_dict = self.cli.base_completer_dict.copy()
        expected_dict["set"] = {"key1": None, "key2": None}
        new_completer = NestedCompleter.from_nested_dict(expected_dict)
        assert str(self.cli.session.completer) == str(new_completer)

    def test_print_help(self):
        """
        Test that print_help displays a help panel with available commands.
        """
        self.cli.print_help()
        self.dummy_console.print.assert_called()
        args, _ = self.dummy_console.print.call_args
        assert isinstance(args[0], Panel)
        assert "Available Commands" in args[0].renderable

    def test_list_modules_success(self):
        """
        Test that list_modules prints a table of modules.
        """
        self.cli.list_modules()
        self.dummy_console.print.assert_called()
        printed_arg = self.dummy_console.print.call_args[0][0]
        assert isinstance(printed_arg, Table)

    def test_list_modules_exception(self):
        """
        Test that list_modules handles exceptions during module instantiation and displays the error.
        """

        # Simulate a module that raises an exception during instantiation.
        class FaultyModule:
            def __init__(self):
                error_msg = "instantiation error"
                raise FaultyModuleError(error_msg)

        self.cli.modules["FaultyModule"] = FaultyModule
        self.cli.list_modules()
        printed_arg = self.dummy_console.print.call_args[0][0]
        temp_console = Console(record=True)
        temp_console.print(printed_arg)
        rendered = temp_console.export_text()
        assert "instantiation error" in rendered

    def test_complete_use(self):
        """
        Test that complete_use returns module suggestions based on user input.
        """
        suggestions_empty = self.cli.complete_use("", "", 0, 0)
        assert sorted(suggestions_empty) == sorted(self.cli.modules.keys())
        suggestions = self.cli.complete_use("my", "", 0, 0)
        assert suggestions == ["MyModule"]

    def test_use_module_no_name(self):
        """
        Test that use_module displays an error when no module name is provided.
        """
        self.cli.use_module("")
        printed_call = self.dummy_console.print.call_args[0][0]
        assert "[red]Please specify a module name. Usage: use <module_name>[/red]" in printed_call

    def test_use_module_success(self):
        """
        Test that use_module correctly selects an existing module.
        """
        self.cli.use_module("SalesModule")
        assert self.cli.current_module is not None
        assert self.cli.current_module_name == "SalesModule"
        printed_calls = [c[0][0] for c in self.dummy_console.print.call_args_list]
        assert any("[green]Module 'SalesModule' selected.[/green]" in s for s in printed_calls)
        assert "SalesModule" in self.cli.prompt

    def test_use_module_exception(self):
        """
        Test that use_module handles exceptions during module initialization.
        """

        class FaultyModule:
            def __init__(self):
                error_msg = "faulty"
                raise FaultyModuleError(error_msg)

        self.cli.modules["FaultyModule"] = FaultyModule
        self.cli.use_module("FaultyModule")
        printed_calls = [c[0][0] for c in self.dummy_console.print.call_args_list]
        assert any("Error initializing module 'FaultyModule': faulty" in s for s in printed_calls)

    def test_use_module_not_found(self):
        """
        Test that use_module displays an error if the specified module is not found.
        """
        self.cli.use_module("NonExistent")
        printed_call = self.dummy_console.print.call_args[0][0]
        assert "[red]Module 'NonExistent' not found.[/red]" in printed_call

    def test_complete_show(self):
        """
        Test that complete_show returns the correct suggestions.
        """
        suggestions_empty = self.cli.complete_show("", "", 0, 0)
        assert suggestions_empty == ["info", "config"]
        suggestions = self.cli.complete_show("in", "", 0, 0)
        assert suggestions == ["info"]

    def test_show_info_no_module(self):
        """
        Test that show_info displays an error when no module is selected.
        """
        self.cli.current_module = None
        self.cli.show_info()
        printed_call = self.dummy_console.print.call_args[0][0]
        assert "[red]No module selected. Use 'use <module_name>' first.[/red]" in printed_call

    def test_show_info_success(self):
        """
        Test that show_info displays the module information in a panel.
        """
        dummy_module = DummyMyModule()
        self.cli.current_module = dummy_module
        self.cli.show_info()
        self.dummy_console.print.assert_called()
        args, _ = self.dummy_console.print.call_args
        assert isinstance(args[0], Panel)
        info_json = json.dumps(
            {
                "Module": dummy_module.__class__.__name__,
                "Config": dummy_module.module_config,
                "Info": dummy_module.info,
            },
            indent=2,
            ensure_ascii=False,
        )
        assert info_json in args[0].renderable

    def test_show_config_no_module(self):
        """
        Test that show_config displays an error when no module is selected.
        """
        self.cli.current_module = None
        self.cli.show_config()
        printed_call = self.dummy_console.print.call_args[0][0]
        assert "[red]No module selected. Use 'use <module_name>' first.[/red]" in printed_call

    def test_show_config_success(self):
        """
        Test that show_config displays the module configuration in a panel.
        """
        dummy_module = DummySalesModule()
        self.cli.current_module = dummy_module
        self.cli.show_config()
        self.dummy_console.print.assert_called()
        args, _ = self.dummy_console.print.call_args
        assert isinstance(args[0], Panel)
        config_json = json.dumps(dummy_module.module_config, indent=2, ensure_ascii=False)
        assert config_json in args[0].renderable

    def test_complete_set_no_module(self):
        """
        Test that complete_set returns an empty list when no module is selected.
        """
        self.cli.current_module = None
        suggestions = self.cli.complete_set("", "", 0, 0)
        assert suggestions == []

    def test_complete_set_success(self):
        """
        Test that complete_set returns valid parameter suggestions for the current module.
        """
        dummy_module = DummyMyModule()
        dummy_module.module_config = {"key1": "val1", "key2": "val2"}
        self.cli.current_module = dummy_module
        suggestions = self.cli.complete_set("", "", 0, 0)
        assert sorted(suggestions) == sorted(["key1", "key2"])
        suggestions_prefix = self.cli.complete_set("key1", "", 0, 0)
        assert suggestions_prefix == ["key1"]

    def test_set_param_no_module(self):
        """
        Test that set_param displays an error when no module is selected.
        """
        self.cli.current_module = None
        self.cli.set_param("key", "value")
        printed_call = self.dummy_console.print.call_args[0][0]
        assert "[red]No module selected. Use 'use <module_name>' first.[/red]" in printed_call

    def test_set_param_success(self):
        """
        Test that set_param updates the module parameter correctly and logs the update.
        """
        dummy_module = DummyMyModule()
        dummy_module.set_parameter = MagicMock()
        self.cli.current_module = dummy_module
        self.cli.set_param("key", "value")
        dummy_module.set_parameter.assert_called_with("key", "value")
        printed_call = self.dummy_console.print.call_args[0][0]
        assert "[green]Parameter 'key' set to 'value' for module 'DummyMyModule'" in printed_call

    def test_run_module_no_module(self):
        """
        Test that run_module displays an error when no module is selected.
        """
        self.cli.current_module = None
        self.cli.run_module()
        printed_call = self.dummy_console.print.call_args[0][0]
        assert "[red]No module selected. Use 'use <module_name>' first." in printed_call

    def test_run_module_success(self):
        """
        Test that run_module executes the module's run method and prints the running message.
        """
        dummy_module = DummySalesModule()
        dummy_module.run = MagicMock()
        self.cli.current_module = dummy_module
        self.cli.run_module()
        printed_calls = [str(c[0][0]) for c in self.dummy_console.print.call_args_list]
        assert any("Running module 'DummySalesModule'" in s for s in printed_calls)
        dummy_module.run.assert_called_once()

    def test_run_module_exception(self):
        """
        Test that run_module handles exceptions raised by the module's run method and prints an error message.
        """
        dummy_module = DummySalesModule()
        dummy_module.run = MagicMock(side_effect=Exception("run error"))
        self.cli.current_module = dummy_module
        self.cli.run_module()
        printed_calls = [str(c[0][0]) for c in self.dummy_console.print.call_args_list]
        assert any("Error running module 'DummySalesModule': run error" in s for s in printed_calls)

    def test_run_loop(self):
        """
        Test the run loop of the CLI.

        Simulates a series of commands and verifies that the CLI loop processes them and exits properly.
        """
        commands = [
            "list",
            "use SalesModule",
            "show info",
            "show config",
            "set key new_value",
            "run",
            "help",
            "unknown",
            "",  # empty input
            "exit",
        ]
        self.dummy_session.prompt.side_effect = [*commands, EOFError()]
        with patch.object(self.cli, "update_completer") as mock_update_completer:
            self.cli.run()
            assert self.dummy_session.prompt.call_count >= len(commands)
            assert mock_update_completer.called
            printed_calls = [str(c[0][0]) for c in self.dummy_console.print.call_args_list]
            assert any(
                "[bold red]Exiting ThreatXManager CLI.[/bold red]" in s for s in printed_calls
            )

    def test_run_loop_keyboard_interrupt(self):
        """
        Test that the CLI run loop exits gracefully upon a KeyboardInterrupt.
        """
        self.dummy_session.prompt.side_effect = [KeyboardInterrupt(), "exit"]
        self.cli.run()
        printed_calls = [str(c[0][0]) for c in self.dummy_console.print.call_args_list]
        assert any("[bold red]Exiting ThreatXManager CLI.[/bold red]" in s for s in printed_calls)


if __name__ == "__main__":
    unittest.main()
