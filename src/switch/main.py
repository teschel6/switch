import argparse

import os
from switch import commands


def _add_argument_directory(parser: argparse.ArgumentParser):
    """Add the directory argment to a parser"""
    parser.add_argument(
        "-d",
        "--directory",
        help="the project directory, defaults to current working directory",
        default=os.getcwd(),
    )


def main():
    parser = argparse.ArgumentParser(
        description="Quickly switch between projects",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # switch command
    subparsers.add_parser("switch", help="switch projects.")

    # init command
    parser_init = subparsers.add_parser("init", help="initialize a new project")
    parser_init.add_argument("-n", "--name", help="the name of the project")
    _add_argument_directory(parser_init)

    # add command
    parser_add = subparsers.add_parser(
        "add", help="add an existing project to user config"
    )
    _add_argument_directory(parser_add)

    # config command
    subparsers.add_parser("config", help="open switch user config")

    # rm command
    parser_add = subparsers.add_parser("rm", help="remove project from user config")
    _add_argument_directory(parser_add)

    args = parser.parse_args()

    if args.command is None:
        args.command = "switch"

    if args.command == "switch":
        commands.switch()
    elif args.command == "init":
        commands.init(args.name, args.directory)
    elif args.command == "add":
        commands.add(args.directory)
    elif args.command == "rm":
        commands.rm(args.directory)
    elif args.command == "config":
        commands.config()


if __name__ == "__main__":
    main()
