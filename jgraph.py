#!/usr/bin/env python3


import cli
from parser import Parser
from graph import Graph

class_ = cli.get_cli_arg('class')
package = cli.get_cli_arg('package')
max_levels = cli.get_cli_arg('max_levels')
path = cli.get_cli_arg('path')

print(class_)
print(package)
print(max_levels)
print(path)

#Parse the dependencies in the giving path
parser = Parser()
parser.parse(path)

graph_args = dict()
if package:
    graph_args['package_filter'] = package
if max_levels: 
    graph_args['max_levels'] = max_levels

graph = Graph('test.db', class_, **graph_args)
graph.create_graph()

