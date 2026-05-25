import os
from typing import Annotated, Optional

import cyclopts

from switch import commands

app = cyclopts.App(help="Quickly switch between projects")


@app.default
def switch():
    """Switch projects."""
    commands.switch()


@app.command
def version():
    """Display switch version."""
    commands.version()


@app.command
def init(
    name: Annotated[
        Optional[str],
        cyclopts.Parameter(
            name=["-n", "--name"],
            help="Name of the new project; defaults to the directory name",
        ),
    ] = None,
    directory: Annotated[
        str,
        cyclopts.Parameter(
            name=["-d", "--directory"],
            help="Project directory; defaults to the current working directory",
        ),
    ] = os.getcwd(),
):
    """Initialize a new project."""
    commands.init(name, directory)


@app.command
def add(
    directory: Annotated[
        str,
        cyclopts.Parameter(
            name=["-d", "--directory"],
            help="Directory to add, or root to search when recursive; defaults to the current working directory",
        ),
    ] = os.getcwd(),
    recursive: Annotated[
        bool,
        cyclopts.Parameter(
            name=["-r", "--recursive"],
            help="Recursively search for and add all projects found under the directory",
        ),
    ] = False,
):
    """Add an existing project to user config."""
    commands.add(directory, recursive)


@app.command
def config():
    """Open switch user config."""
    commands.config()


@app.command
def rm(
    directory: Annotated[
        str,
        cyclopts.Parameter(
            name=["-d", "--directory"],
            help="Directory of the project to remove; defaults to the current working directory",
        ),
    ] = os.getcwd(),
):
    """Remove project from user config."""
    commands.rm(directory)


def main():
    app()


if __name__ == "__main__":
    main()
