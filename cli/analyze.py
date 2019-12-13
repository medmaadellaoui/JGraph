import argparse
import os
from core.parser import Parser
from utils import cli_validator as validator
from cli import cli
from cli.cli import Command

class Analyze(Command):

    def setup(self):
        self.args_parser = cli.add_sub_parser(
            'analyze', 
            'Creating a file database of all dependencies in a given path.')

        self.args_parser.add_argument('-o', '--output', type=str, help='Output file')
        self.args_parser.add_argument('path', type=str, action=validator.check_dir, help='The path to the project or JAVA file')

        self.args_parser.set_defaults(func=self.execute)

    def execute(self, args):

        #Get arguments
        try:
            # args = self.args_parser.parse_args()
            path = args.path
            output = args.output
        except argparse.ArgumentTypeError as error:
            print(error)
            exit(0)

        #Parse files in the given path
        parser = Parser(output)
        parser.parse(path)
