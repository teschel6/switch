from pathlib import Path
import toml
import os
import inquirer
from switch.types import UserConfig, Reference, Project

PROJECT_CONFIG = ".switch.toml"
USER_CONFIG_FILE = ".config/switch/config.toml"


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
        # TODO parse file directly to config
        config = toml.load(file)
        config["projects"] = config.get("projects", [])
        config = UserConfig(**config)
        config.projects = [Reference(**r) for r in config.projects]

        return config


def write_user_config(config: UserConfig):
    config_path = get_config_path()

    with open(config_path, "w") as file:
        # TODO use [[array]] toml object syntax with lib
        content = ""
        for ref in config.projects:
            content += "[[projects]]\n"
            content += f"id = '{ref.id}'\n"
            content += f"name = '{ref.name}'\n"
            content += f"directory = '{ref.directory}'\n"
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

    with open(project_file, "r") as f:
        project = toml.load(f)
        return Project(**project)


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
