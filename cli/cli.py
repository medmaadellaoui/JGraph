import argparse
import os
from utils import cli_validator as validator

#A command interface
class Command:

    args_parser = None

    def setup(self):
        pass

    def execute(self):
        pass


#The general cli command
args_parser = argparse.ArgumentParser(
    prog='jgraph', 
    description='JGraph is tool to create dependecy graph for JAVA language')

subparsers = args_parser.add_subparsers()
args = None

def get_cli_arg(key):

    if args:
        return getattr(args, key)
    return None
    

def append_graph_args_to(args_parser : argparse.ArgumentParser):
    """Graph arguments"""
    args_parser.add_argument('database', type=str, help='The dependencies database created with the create command')
    args_parser.add_argument('-c', '--class', type=str, help='The starting class of the dependency tree')
    args_parser.add_argument('-l', '--max-levels', type=int, help='How deep you want to go int the dependency tree')
    args_parser.add_argument('-p', '--package', type=str, help='Filter by package')

def append_path_args_to(args_parser : argparse.ArgumentParser):
    """Java project or file path arguments"""
    args_parser.add_argument('path', type=str, action=validator.check_dir, help='The path to the project or JAVA file')

def add_sub_parser(name, help) -> argparse.ArgumentParser:
    return subparsers.add_parser(name, help=help)

def setup(*commands):
    """Setup cli commands"""

    if commands:
        for command in commands:
            command.setup()

    try:
        args = args_parser.parse_args()
        args.func(args)
    except argparse.ArgumentTypeError as error:
        print(error)
        exit(0)

