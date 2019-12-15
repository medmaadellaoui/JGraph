import argparse
import os
from core.parser import Parser
from core.graph import Graph
from utils import cli_validator as validator
from cli import cli
from cli.cli import Command
import re


class Create(Command):

    def setup(self):
        self.args_parser = cli.add_sub_parser(
            'create', 
            'Create the graph file.')

        self.args_parser.add_argument('-o', '--output', type=str, help='Graph output file')
        self.args_parser.add_argument('-f', '--format', type=str, help='Graph output file format (supported format: png, svg, dot)')
        cli.append_graph_args_to(self.args_parser)

        self.args_parser.set_defaults(func=self.execute)

    def execute(self, args):

        #Get arguments
        try:
            database = args.database
            class_ = getattr(args, 'class')
            package = args.package
            max_levels = args.max_levels
            output_path = args.output
            format_ = args.format
        except argparse.ArgumentTypeError as error:
            print(error)
            exit(0)

        #Generating the dependency graph
        params = dict()
        if class_: params['starting_cls'] = class_
        if package: params['package_filter'] = package
        if max_levels: params['max_levels'] = max_levels
        

        #extract the desired format from the filename if no format was specified
        
        if output_path and not format_:
            array = output_path.split('.')
            print(array)
            if(len(array) >= 2 and array[-1]):
                format_ = array[-1]

        if format_: params['format_'] = format_
        
        if output_path and format_:
            output_path = re.sub(f'\.{format_}$', '', output_path)

        if output_path: params['output_path'] = output_path

        graph = Graph(input_db_path=database, **params)
        graph.create_graph()
        
