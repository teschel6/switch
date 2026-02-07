import os
from switch import utils
from switch.datatypes import Reference, UserConfig
from pathlib import Path


def add(directory: str, recursive: bool = False):
    """Add project(s) to user config.

    Args:
        directory (str): the directory to add or search
        recursive (bool): if True, recursively search for all projects
    """
    directory = os.path.abspath(directory)
    config = utils.load_user_config()

    if recursive:
        project_dirs = _find_project_configs(directory)

        if not project_dirs:
            print(f"No projects found in '{directory}' or its subdirectories.")
            return

        print(f"Found {len(project_dirs)} project(s) in '{directory}':")

        for project_dir in project_dirs:
            project_dir = os.path.abspath(project_dir)
            _add_single_project(str(project_dir), config)
    else:
        _add_single_project(directory, config)


def _add_single_project(directory: str, config: UserConfig):
    """Add a single project."""
    project = utils.load_project(directory)
    ref = Reference(id=project.id, name=project.name, directory=directory)

    if any(ref.id == r.id for r in config.projects):
        print(f"project '{ref.name}:{ref.id}' already added.")
        return

    config.projects.append(ref)
    utils.write_user_config(config)


def _find_project_configs(directory: str) -> list[Path]:
    """Find all .switch.toml files recursively in directory.

    Args:
        directory (str): the root directory to search from

    Returns:
        list[Path]: list of paths to .switch.toml files
    """
    root = Path(directory)
    project_configs = []

    # recursively search for all project configs
    for path in root.rglob(utils.PROJECT_CONFIG):
        project_configs.append(path.parent)

    return project_configs
