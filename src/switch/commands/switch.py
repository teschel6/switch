import os
import subprocess
from pathlib import Path

from switch.select import select_project
from switch import utils


def switch():
    config = utils.load_user_config()
    selected = select_project(config)

    if selected is None:
        print("Nothing selected.")
        return

    project = utils.load_project(selected.directory)
    editor = utils.get_editior()

    print(f"selected '{selected.name}' switching to '{selected.directory}'")
    os.chdir(Path(selected.directory))

    if project.activate is not None:
        shell = os.environ.get("SHELL", "/bin/bash")
        activate_cmd = " ".join(project.activate)

        print(f"activating project with '{activate_cmd}'")
        print(f"opening in editor '{editor}' ...")

        full_command = f"{activate_cmd} && {editor} ."
        subprocess.run([shell, "-c", full_command])
    else:
        print(f"opening in editor '{editor}' ...")
        subprocess.run([editor, "."])
