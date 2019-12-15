import argparse
import os
from core.parser import Parser
from utils import cli_validator as validator
from cli import cli
from cli.cli import Command
from utils.cli_print_utils import bcolors

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

        files_count=0
        dirs_count=0
        java_files_count=0


        def update_progress(type, filename):

            nonlocal files_count
            nonlocal dirs_count
            nonlocal java_files_count

            if type == Parser.TYPE_FILE:  
                files_count = files_count + 1
            elif type == Parser.TYPE_DIR:
                dirs_count = dirs_count + 1
            elif type == Parser.TYPE_FILE_JAVA:
                java_files_count = java_files_count + 1

            print(f'processed dirs: {bcolors.OKBLUE}{dirs_count}{bcolors.ENDC}, processed files : {bcolors.OKBLUE}{files_count}{bcolors.ENDC}, found java files: {bcolors.OKGREEN}{java_files_count}{bcolors.ENDC}',end='\r')
        
        parser.parse(path, update_progress)
        print()
    
