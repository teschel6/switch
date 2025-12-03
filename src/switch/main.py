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
        # TODO: read the user config into UserConfig
        loaded = toml.load(file)

        projects = loaded.get("project")
        projects = projects if projects is not None else []
        projects = [
            Reference(
                p["id"],
                p["name"],
                p["directory"],
            )
            for p in projects
        ]

        print(f"loaded projects from config {projects=}")
        return UserConfig(projects)


def _write_user_config(config: UserConfig):
    config_path = _get_config_path()

    with open(config_path, "w") as file:
        print(f"writing user config {config_path}")

        # TODO: use [[array]] toml object syntax with lib
        content = ""
        for ref in config.projects:
            content += "[[project]]\n"
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
        # TODO: load directly to Project
        project = toml.load(f)
        return Project(project["id"], project["name"])


def add(directory: str):
    project = _load_project(directory)
    config = _load_user_config()

    ref = Reference(id=project.id, name=project.name, directory=directory)

    print(f"adding reference '{ref}'")

    config.projects.append(ref)

    _write_user_config(config)


def init(name: Optional[str], directory: Optional[str]):
    cwd = os.getcwd()

    if name is None:
        name = os.path.basename(cwd)

    if directory is None:
        directory = cwd

    project_config = Path(cwd) / Path(PROJECT_CONFIG)
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

    args = parser.parse_args()

    print(f"{args=}")

    if args.command == "init":
        init(args.name, args.directory)
    elif args.command == "switch":
        raise NotImplementedError("switch project not implemented")
    elif args.command == "add":
        raise NotImplementedError("add project not implemented")
    elif args.command == "remove":
        raise NotImplementedError("add project not implemented")


if __name__ == "__main__":
    main()
