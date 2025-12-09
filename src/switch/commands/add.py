from switch import utils
from switch.datatypes import Reference


def add(directory: str):
    project = utils.load_project(directory)
    config = utils.load_user_config()

    ref = Reference(id=project.id, name=project.name, directory=directory)

    if any(ref.id == r.id for r in config.projects):
        print(f"project '{ref.name}:{ref.id}' already added.")
        return

    config.projects.append(ref)

    utils.write_user_config(config)
