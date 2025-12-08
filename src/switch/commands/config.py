import subprocess

from switch import utils


def config():
    config_path = utils.get_config_path()
    editor = utils.get_editior()

    subprocess.run([editor, config_path])
