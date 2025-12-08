import os
import subprocess
from pathlib import Path
from switch import utils


def switch():
    selected = utils.select_project()

    print(f"selected '{selected.name}' switching to '{selected.directory}'")

    # TODO: find better way to open project
    os.chdir(Path(selected.directory))
    subprocess.run(["bash"])
