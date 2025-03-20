import sys
from os import mkdir
from shutil import copyfile
from decimal import Inexact


# subcommand
# newproject
# newapp



def main():
    """
    code for CLI command that create a telebot_framework project.

    :return: None
    """

    argv = sys.argv[1:]

    try:
        subcommand = argv[1]
        argument = argv[2]

        if subcommand == "newproject":
            create_project(name=argument)

        elif subcommand == "newapp":
            create_app(name=argument)

        return None

    except IndexError as e:
        pass

    help()
    return None


def create_project(name:str):
    mkdir(f"../../../{name}")
    copyfile(src="../../../template/*", dst="../../../")
    return None


def create_app(name:str):
    return None



def print_help():
    """
    code for printing out usage of command 'mizuhara'

    :return: None
    """

    pass
