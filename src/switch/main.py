import argparse

from switch.project import Project, Reference, UserConfig
from ulid import ULID
from typing import List, Optional
import os
import toml
from pathlib import Path

PROJECT_CONFIG = ".switch.toml"
USER_CONFIG_FILE = ".config/switch/config.toml"


def _get_config_path() -> Path:
    """Get user config file path create if DNE"""
    path = Path.home() / Path(USER_CONFIG_FILE)

    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        print(f"reading user config {path}")
    else:
        path.touch()
        print(f"user config created {path}")

    return path


def _load_user_config() -> UserConfig:
    config_path = _get_config_path()

    with open(config_path, "r") as file:
        config = toml.load(file)
        config["projects"] = config.get("projects", [])
        config = UserConfig(**config)
        config.projects = [Reference(**r) for r in config.projects]

        print(f"loaded projects from config {config.projects=}")
        return config


def _write_user_config(config: UserConfig):
    config_path = _get_config_path()

    with open(config_path, "w") as file:
        print(f"writing user config {config_path}")

        # TODO: use [[array]] toml object syntax with lib
        content = ""
        for ref in config.projects:
            content += "[[projects]]\n"
            content += f"id = '{ref.id}'\n"
            content += f"name = '{ref.name}'\n"
            content += f"directory = '{ref.directory}'\n"
            # content += toml.dumps(vars(ref))
            content += "\n"

        file.write(content)
        # toml.dump(vars(config), file)


def _load_project(directory: str) -> Project:
    project_file = Path(directory) / Path(PROJECT_CONFIG)

    if not project_file.exists():
        error = f"fatal: not a switch project, missing '{PROJECT_CONFIG}' file."
        error += "\nhint: use 'init' command to make a new project"
        raise SystemExit(error)

    with open(project_file, "r") as f:
        project = toml.load(f)
        return Project(**project)


def add(directory: str):
    cwd = os.getcwd()

    if directory is None:
        directory = cwd

    project = _load_project(directory)
    config = _load_user_config()

    ref = Reference(id=project.id, name=project.name, directory=directory)

    print(f"adding reference '{ref}'")

    if any(ref.id == r.id for r in config.projects):
        print(f"project '{ref.name}:{ref.id}' already added.")
        return

    config.projects.append(ref)

    _write_user_config(config)


def init(name: Optional[str], directory: Optional[str]):
    cwd = os.getcwd()

    if directory is None:
        directory = cwd

    if name is None:
        # TODO ignore final /
        name = os.path.basename(directory)

    project_config = Path(directory) / Path(PROJECT_CONFIG)
    print(f"{project_config=}")

    if project_config.exists():
        error = "fatal: project already initialized"
        error += "\nhint: add and existing project to user config with 'add' command"
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


def main():
    parser = argparse.ArgumentParser(
        description="Quickly switch between projects",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # init command
    parser_init = subparsers.add_parser("init", help="initialize a new project")
    parser_init.add_argument(
        "-d", "--directory", help="the project directory, defaults to present directory"
    )
    parser_init.add_argument(
        "-n", "--name", help="the project name, defaults to present directory name"
    )

    # add command
    parser_add = subparsers.add_parser(
        "add", help="add an existing project to user config"
    )
    parser_add.add_argument(
        "-d", "--directory", help="the project directory, defaults to present directory"
    )

    args = parser.parse_args()

    if args.command == "init":
        init(args.name, args.directory)
    elif args.command == "switch":
        raise NotImplementedError("switch project not implemented")
    elif args.command == "add":
        add(args.directory)
    elif args.command == "remove":
        raise NotImplementedError("add project not implemented")


if __name__ == "__main__":
    main()
