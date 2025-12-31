from pathlib import Path
import toml
import os
import inquirer
from dataclasses import fields

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
# from rich.prompt import Prompt
# from rich.live import Live

from switch.datatypes import UserConfig, Reference, Project

PROJECT_CONFIG = ".switch.toml"
USER_CONFIG_FILE = ".config/switch/config.toml"


def safe_unpack(data: dict, dataclass_type):
    """Unpack a dataclass ignoring extra or missing fields.

    Args:
        data (dict): the dictionary to be unpacked.
        dataclass_type: a dataclass object to parse into.

    Returns:
        dataclass_type: the object parsed from dictionary.
    """
    field_names = [f.name for f in fields(dataclass_type)]

    safe_data = {name: data.get(name, None) for name in field_names}

    return dataclass_type(**safe_data)


def get_config_path() -> Path:
    """Get user config file path create if DNE"""
    path = Path.home() / Path(USER_CONFIG_FILE)

    path.parent.mkdir(parents=True, exist_ok=True)

    if not path.exists():
        path.touch()
        print(f"new user config created {path}")

    return path


def load_user_config() -> UserConfig:
    config_path = get_config_path()

    print(f"reading user config {config_path}")

    with open(config_path, "r") as file:
        data = toml.load(file)
        # TODO make safe_unpack recursive for dataobject fields
        data["projects"] = [safe_unpack(r, Reference) for r in data["projects"]]
        return safe_unpack(data, UserConfig)


def write_user_config(config: UserConfig):
    config_path = get_config_path()

    with open(config_path, "w") as file:
        # TODO use [[array]] toml object syntax with lib
        content = ""
        for ref in config.projects:
            content += "[[projects]]\n"
            content += toml.dumps(vars(ref))
            content += "\n"

        file.write(content)
        print(f"updated user config {config_path}")


def load_project(directory: str) -> Project:
    project_file = Path(directory) / Path(PROJECT_CONFIG)

    if not project_file.exists():
        error = f"fatal: not a switch project, missing '{PROJECT_CONFIG}' file."
        error += "\nhint: use 'init' command to make a new project"
        error += f"\n\nswitch init {directory}"
        raise SystemExit(error)

    with open(project_file, "r") as file:
        data = toml.load(file)

        return safe_unpack(data, Project)


def select_project_rich():
    table = Table(box=None, show_header=False)

    table.add_column("selected", justify="left", style="blue", no_wrap=True)
    table.add_column("name", justify="left", style="blue", no_wrap=True)
    table.add_column("directory", justify="left")
    table.add_column("id", justify="left", style="bright_black")

    config = load_user_config()

    # with Live(table, refresh_per_second=4):

    for ref in config.projects:
        table.add_row(" ", ref.name, ref.directory, ref.id)

    # example highlighted row
    table.add_row(">", ref.name, ref.directory, style="black on white")

    table_panel = Panel(table, title="projects")
    prompt_panel = Panel(">")

    console = Console()
    console.print()
    console.print(table_panel)
    console.print(prompt_panel)

    return None


# used for testing select
if __name__ == "__main__":
    select_project_rich()


def select_project() -> Reference:
    # TODO: add fuzzy searching to list selection

    config = load_user_config()

    query = inquirer.List(
        "project",
        message="select a project",
        choices=[(p.name, p) for p in config.projects],
    )
    answers = inquirer.prompt([query])

    if answers is None:
        raise SystemExit("fatal: no project selected")

    selected = answers["project"]

    return selected


def executable_exists(command: str):
    """Check if command is in PATH and executable"""
    for path in os.environ.get("PATH", "").split(os.pathsep):
        full_path = os.path.join(path, command)
        if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
            return True

    return False


def get_editior():
    """Find the best available editor in order of preference"""
    editors = ["nvim", "vim", "vi", "nano", "emacs"]

    for editor in editors:
        if executable_exists:
            return editor

    raise SystemExit("fatal: no suitable text editor found")
