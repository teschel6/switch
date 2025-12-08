from switch import utils


def rm(directory: str):
    project = utils.load_project(directory)
    config = utils.load_user_config()

    config.projects = [r for r in config.projects if r.id != project.id]

    utils.write_user_config(config)

    print(f"removed '{project.name}:{project.id}'")
