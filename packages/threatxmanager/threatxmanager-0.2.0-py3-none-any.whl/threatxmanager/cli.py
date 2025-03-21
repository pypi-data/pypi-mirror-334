#!/usr/bin/env python
import json
import secrets
from pathlib import Path

import toml
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.styles import Style
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from threatxmanager.config.manager_config import Config
from threatxmanager.modules.external.my_module import MyModule
from threatxmanager.modules.external.my_module_db import SalesModule


class DatabaseConfigError(Exception):
    """Custom exception for database configuration errors"""


def get_version() -> str:
    """

    Reads the project version from the pyproject.toml file under the [project] section.
    Assumes the file is located at the project root (two levels up from this file)
    """
    try:
        project_root = Path(__file__).resolve().parent.parent
        pyproject_path = project_root / "pyproject.toml"
        if not pyproject_path.exists():
            return "Unknown"
        config_data = toml.load(pyproject_path)
        return config_data.get("project", {}).get("version", "Unknown")
    except Exception:
        return "Unknown"


THREATMANAGER_VERSION = get_version()

# List of random startup log messages.
STARTUP_MESSAGES = [
    "Initializing ThreatXManager... Ready to secure your world!",
    "Loading modules... All systems operational.",
    "ThreatXManager booting up. Modules loaded and ready.",
    "System check complete. ThreatXManager is online.",
    "Welcome to ThreatXManager. Your security, our priority!",
]


class ThreatXCLI:
    def __init__(self, config_instance: Config | None = None) -> None:
        # Use the provided config instance or create a new one.
        self.config = config_instance if config_instance is not None else Config()
        self.console = Console()
        # Mapping of available modules: module name -> class reference.
        self.modules: dict[str, object] = {
            "SalesModule": SalesModule,
            "MyModule": MyModule,
        }
        self.current_module: object | None = None
        self.current_module_name: str | None = None

        # Base nested completer for static commands.
        self.base_completer_dict: dict[str, object] = {
            "list": None,
            "use": {name: None for name in self.modules},  # SIM118 fixed
            "show": {"info": None, "config": None},
            "set": None,
            "run": None,
            "help": None,
            "exit": None,
        }
        self.session = PromptSession(
            completer=NestedCompleter.from_nested_dict(self.base_completer_dict),
            style=Style.from_dict({"prompt": "ansicyan bold"}),
            rprompt=self.get_rprompt,
        )
        self.prompt = "threatXmanager> "

        # Print startup info with a random message and module count.
        self.print_startup_info()

    def print_startup_info(self) -> None:
        """Print a random startup message and display the count of available modules."""
        msg = secrets.choice(
            STARTUP_MESSAGES
        )  # Use secrets.choice for a more secure random selection.
        module_count = len(self.modules)
        self.console.print(f"[bold green]{msg}[/bold green]")
        self.console.print(f"[bold blue]Loaded {module_count} modules.[/bold blue]")

    def get_rprompt(self) -> str:
        """
        Returns a dynamic right prompt string showing the connected database (by name),
        the SQLAlchemy connector (dialect), pool parameters, and the ThreatManager version.
        """

        def fetch_db_info() -> (str, str, str):
            env = self.config.get_default_env()
            database_section = self.config.get("database", {})
            bancode_config = database_section.get("bancode_dados", {})
            db_config = bancode_config.get(env, {})
            if not db_config:
                error_message = (
                    f"Environment '{env}' not found in the 'database.bancode_dados' section."
                )
                raise DatabaseConfigError(error_message)
            db_url = db_config.get("DATABASE_URL", "N/A")
            pool_size = db_config.get("POOL_SIZE", "N/A")
            max_overflow = db_config.get("MAX_OVERFLOW", "N/A")
            pool_info = f"{pool_size}/{max_overflow}"
            from sqlalchemy.engine.url import make_url

            parsed_url = make_url(db_url)
            dialect = parsed_url.get_backend_name() if db_url != "N/A" else "N/A"
            db_name = parsed_url.database if parsed_url.database is not None else "N/A"
            return db_name, dialect, pool_info

        try:
            db_name, dialect, pool_info = fetch_db_info()
        except Exception:
            db_name, dialect, pool_info = "Error", "Error", "Error"
        return f"DB: {db_name} ({dialect}) | Pool: {pool_info} | v{THREATMANAGER_VERSION}"

    def update_prompt(self) -> None:
        """Update the CLI prompt to include the selected module name, if any."""
        if self.current_module_name:
            self.prompt = f"threatxmanager({self.current_module_name})> "
        else:
            self.prompt = "threatxmanager> "

    def update_completer(self) -> None:
        """
        Dynamically update the 'set' command autocompletion keys based on current module configuration.
        """
        config_keys = list(self.current_module.module_config.keys()) if self.current_module else []
        new_completer_dict = self.base_completer_dict.copy()
        new_completer_dict["set"] = {key: None for key in config_keys}
        self.session.completer = NestedCompleter.from_nested_dict(new_completer_dict)

    def print_help(self) -> None:
        """Display detailed help information for all available commands."""
        help_text = (
            "[bold cyan]Available Commands:[/bold cyan]\n\n"
            "  [green]list[/green]              - List all available modules.\n"
            "  [green]use <module_name>[/green] - Select a module to use (e.g., use SalesModule).\n"
            "  [green]show info[/green]         - Display detailed metadata for the selected module.\n"
            "  [green]show config[/green]       - Display the selected module's configuration (from config file).\n"
            "  [green]set <key> <value>[/green]   - Update a configuration parameter of the selected module.\n"
            "                                  Autocompletion suggests available keys.\n"
            "  [green]run[/green]               - Execute the currently selected module.\n"
            "  [green]help[/green]              - Display this help message.\n"
            "  [green]exit[/green]              - Exit the CLI.\n"
        )
        self.console.print(Panel(help_text, title="ThreatXManager CLI Help", style="bold blue"))

    def list_modules(self) -> None:
        """Display all available modules in a formatted table with clear row separators."""
        table = Table(title="Available Modules", show_lines=True)
        table.add_column("Module Name", style="cyan", no_wrap=True)
        table.add_column("Description", style="magenta")
        for name, module_cls in self.modules.items():  # Removed .keys() per SIM118
            try:
                instance = module_cls()
                description = instance.info.get("Description", "No description provided")
            except Exception as e:
                description = f"Error: {e}"
            table.add_row(name, description)
        self.console.print(table)

    def complete_use(self, text: str, line: str, begidx: int, endidx: int) -> list[str]:
        if not text:
            return list(self.modules)  # Fixed SIM118
        return [m for m in self.modules if m.lower().startswith(text.lower())]

    def use_module(self, module_name: str) -> None:
        """Select a module using its name."""
        module_name = module_name.strip()
        if not module_name:
            self.console.print("[red]Please specify a module name. Usage: use <module_name>[/red]")
            return
        if module_name in self.modules:
            try:
                self.current_module = self.modules[module_name]()
                self.current_module_name = module_name
                self.console.print(f"[green]Module '{module_name}' selected.[/green]")
                self.update_prompt()
            except Exception as e:
                self.console.print(f"[red]Error initializing module '{module_name}': {e}[/red]")
        else:
            self.console.print(f"[red]Module '{module_name}' not found.[/red]")

    def complete_show(self, text: str, line: str, begidx: int, endidx: int) -> list[str]:
        options = ["info", "config"]
        if not text:
            return options
        return [opt for opt in options if opt.lower().startswith(text.lower())]

    def show_info(self) -> None:
        """Display the metadata (info) for the selected module in a structured, pretty-printed format."""
        if not self.current_module:
            self.console.print("[red]No module selected. Use 'use <module_name>' first.[/red]")
            return
        info_data = {
            "Module": self.current_module.__class__.__name__,
            "Config": self.current_module.module_config,
            "Info": self.current_module.info,
        }
        info_str = json.dumps(info_data, indent=2, ensure_ascii=False)
        self.console.print(
            Panel(
                info_str,
                title=f"Module Info: {self.current_module.__class__.__name__}",
                style="bold green",
            )
        )

    def show_config(self) -> None:
        """Display the module's dynamic configuration in a structured, pretty-printed format."""
        if not self.current_module:
            self.console.print("[red]No module selected. Use 'use <module_name>' first.[/red]")
            return
        config_str = json.dumps(self.current_module.module_config, indent=2, ensure_ascii=False)
        self.console.print(
            Panel(
                config_str,
                title=f"Module Config: {self.current_module.__class__.__name__}",
                style="bold green",
            )
        )

    def complete_set(self, text: str, line: str, begidx: int, endidx: int) -> list[str]:
        if not self.current_module:
            return []
        keys = list(self.current_module.module_config.keys())
        if not text:
            return keys
        return [key for key in keys if key.lower().startswith(text.lower())]

    def set_param(self, key: str, value: str) -> None:
        """Update a configuration parameter for the current module."""
        if not self.current_module:
            self.console.print("[red]No module selected. Use 'use <module_name>' first.[/red]")
            return
        self.current_module.set_parameter(key, value)
        self.console.print(
            f"[green]Parameter '{key}' set to '{value}' for module '{self.current_module.__class__.__name__}'.[/green]"
        )

    def run_module(self) -> None:
        """Execute the currently selected module."""
        if not self.current_module:
            self.console.print("[red]No module selected. Use 'use <module_name>' first.[/red]")
            return
        try:
            self.console.print(
                f"[green]Running module '{self.current_module.__class__.__name__}'...[/green]"
            )
            self.current_module.run()
        except Exception as e:
            self.console.print(
                f"[red]Error running module '{self.current_module.__class__.__name__}': {e}[/red]"
            )

    def run(self) -> None:
        """Main interactive CLI loop."""
        self.console.print(
            "[bold green]Welcome to ThreatXManager CLI (Interactive Mode)[/bold green]"
        )
        while True:
            self.update_completer()  # Update dynamic autocompletion for 'set' keys.
            try:
                user_input = self.session.prompt(self.prompt)
            except KeyboardInterrupt:
                continue
            except EOFError:
                break

            if not user_input.strip():
                continue

            parts = user_input.strip().split()
            command = parts[0].lower()

            if command == "list":
                self.list_modules()
            elif command == "use":
                if len(parts) < 2:
                    self.console.print("[red]Usage: use <module_name>[/red]")
                else:
                    self.use_module(parts[1])
            elif command == "show":
                if len(parts) < 2:
                    self.console.print("[red]Usage: show <info|config>[/red]")
                else:
                    subcmd = parts[1].lower()
                    if subcmd == "info":
                        self.show_info()
                    elif subcmd == "config":
                        self.show_config()
                    else:
                        self.console.print(
                            "[red]Unknown show command. Use 'show info' or 'show config'.[/red]"
                        )
            elif command == "set":
                if len(parts) < 3:
                    self.console.print("[red]Usage: set <key> <value>[/red]")
                else:
                    key = parts[1]
                    value = " ".join(parts[2:])
                    self.set_param(key, value)
            elif command == "run":
                self.run_module()
            elif command == "help":
                self.print_help()
            elif command == "exit":
                self.console.print("[bold red]Exiting ThreatXManager CLI.[/bold red]")
                break
            else:
                self.console.print(f"[red]Unknown command: {command}[/red]")


if __name__ == "__main__":
    cli = ThreatXCLI()
    cli.run()
