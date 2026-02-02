from typing import Optional
import os
from pathlib import Path
import toml
from ulid import ULID

from switch.utils import PROJECT_CONFIG
from switch.datatypes import Project
from switch.commands import add

from switch import commands


def init(name: Optional[str], directory: str):
    if name is None:
        normalized = os.path.normpath(directory)
        name = os.path.basename(normalized)

    project_config = Path(directory) / Path(PROJECT_CONFIG)

    if project_config.exists():
        print("project already initialized. Adding project instead.")
        add(directory)
        return

    project = Project(
        id=str(ULID()),
        name=name,
        activate=[],
    )

    print(f"initialized new project {project.name}:{project.id} in {project_config}")

    with open(project_config, "w") as f:
        toml.dump(vars(project), f)

    # add new project
    commands.add(directory)
