import argparse

from ulid import ULID
from typing import List, Optional
import os
import toml
from pathlib import Path
from dataclasses import dataclass
import inquirer
import subprocess

PROJECT_CONFIG = ".switch.toml"
USER_CONFIG_FILE = ".config/switch/config.toml"


@dataclass
class Project:
    id: str
    name: str


@dataclass
class Reference:
    id: str
    name: str
    directory: str


@dataclass
class UserConfig:
    projects: List[Reference]


def _get_config_path() -> Path:
    """Get user config file path create if DNE"""
    path = Path.home() / Path(USER_CONFIG_FILE)

    path.parent.mkdir(parents=True, exist_ok=True)

    if not path.exists():
        path.touch()
        print(f"new user config created {path}")

    return path


def _load_user_config() -> UserConfig:
    config_path = _get_config_path()

    print(f"reading user config {config_path}")

    with open(config_path, "r") as file:
        # TODO parse file directly to config
        config = toml.load(file)
        config["projects"] = config.get("projects", [])
        config = UserConfig(**config)
        config.projects = [Reference(**r) for r in config.projects]

        return config


def _write_user_config(config: UserConfig):
    config_path = _get_config_path()

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


def _load_project(directory: str) -> Project:
    project_file = Path(directory) / Path(PROJECT_CONFIG)

    if not project_file.exists():
        error = f"fatal: not a switch project, missing '{PROJECT_CONFIG}' file."
        error += "\nhint: use 'init' command to make a new project"
        error += f"\n\nswitch init {directory}"
        raise SystemExit(error)

    with open(project_file, "r") as f:
        project = toml.load(f)
        return Project(**project)


def _select_project() -> Reference:
    # TODO: add fuzzy searching to list selection

    config = _load_user_config()

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


def _executable_exists(command: str):
    """Check if command is in PATH and executable"""
    for path in os.environ.get("PATH", "").split(os.pathsep):
        full_path = os.path.join(path, command)
        if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
            return True

    return False


def _get_editior():
    """Find the best available editor in order of preference"""
    editors = ["nvim", "vim", "vi", "nano", "emacs"]

    for editor in editors:
        if _executable_exists:
            return editor

    raise SystemExit("fatal: no suitable text editor found")


def add(directory: str):
    project = _load_project(directory)
    config = _load_user_config()

    ref = Reference(id=project.id, name=project.name, directory=directory)

    if any(ref.id == r.id for r in config.projects):
        print(f"project '{ref.name}:{ref.id}' already added.")
        return

    config.projects.append(ref)

    _write_user_config(config)


def remove(directory: str):
    project = _load_project(directory)
    config = _load_user_config()

    config.projects = [r for r in config.projects if r.id != project.id]

    _write_user_config(config)

    print(f"removed '{project.name}:{project.id}'")


def init(name: Optional[str], directory: str):
    if name is None:
        # TODO ignore final /
        normalized = os.path.normpath(directory)
        name = os.path.basename(normalized)

    project_config = Path(directory) / Path(PROJECT_CONFIG)

    if project_config.exists():
        error = "fatal: project already initialized"
        error += "\nhint: add and existing project to user config with 'add' command"
        error += f"\n\nswitch add {directory}"
        raise SystemExit(error)

    project = Project(
        id=str(ULID()),
        name=name,
    )

    print(f"initialized new project {project.name}:{project.id} in {project_config}")

    with open(project_config, "w") as f:
        toml.dump(vars(project), f)

    # add new project
    add(directory)


def switch():
    selected = _select_project()

    print(f"selected '{selected.name}' switching to '{selected.directory}'")

    # TODO: find better way to open project
    os.chdir(Path(selected.directory))
    subprocess.run(["bash"])


def config():
    config_path = _get_config_path()
    editor = _get_editior()

    subprocess.run([editor, config_path])


def _add_argument_directory(parser: argparse.ArgumentParser):
    """Add the directory argment to a parser"""
    parser.add_argument(
        "-d",
        "--directory",
        help="the project directory, defaults to current working directory",
        default=os.getcwd(),
    )


def main():
    parser = argparse.ArgumentParser(
        description="Quickly switch between projects",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # switch command
    subparsers.add_parser("switch", help="switch projects.")

    # init command
    parser_init = subparsers.add_parser("init", help="initialize a new project")
    parser_init.add_argument("-n", "--name", help="the name of the project")
    _add_argument_directory(parser_init)

    # add command
    parser_add = subparsers.add_parser(
        "add", help="add an existing project to user config"
    )
    _add_argument_directory(parser_add)

    # config command
    subparsers.add_parser("config", help="open switch user config")

    # rm command
    parser_add = subparsers.add_parser("rm", help="remove project from user config")
    _add_argument_directory(parser_add)

    args = parser.parse_args()

    if args.command is None:
        args.command = "switch"

    if args.command == "switch":
        switch()
    elif args.command == "init":
        init(args.name, args.directory)
    elif args.command == "add":
        add(args.directory)
    elif args.command == "rm":
        remove(args.directory)
    elif args.command == "config":
        config()


if __name__ == "__main__":
    main()
