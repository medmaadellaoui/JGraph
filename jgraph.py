#!/usr/bin/env python3
from core.parser import Parser
from core.graph import Graph
from cli import cli
from cli.cli import Command
from cli.analyze import Analyze
from cli.create import Create
from typing import Dict

commands = [
    Analyze(),
    Create()
]

cli.setup(*commands)

# if command == None:
#     class_ = cli.get_cli_arg('class')
#     package = cli.get_cli_arg('package')
#     max_levels = cli.get_cli_arg('max_levels')
#     path = cli.get_cli_arg('path')

#     #Parse the dependencies in the giving path
#     parser = Parser('test.db')
#     parser.parse(path)

#     graph_args = dict()
#     if package:
#         graph_args['package_filter'] = package
#     if max_levels: 
#         graph_args['max_levels'] = max_levels

#     graph = Graph('test.db', class_, **graph_args)
#     graph.create_graph()

# else:
#     commands[command].execute()
