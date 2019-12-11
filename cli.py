import argparse
import os

args_parser = argparse.ArgumentParser(
    prog='jgraph', 
    description='JGraph is tool to create dependecy graph for JAVA language')


class check_dir(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        prospective_dir=values
        if not os.path.isdir(prospective_dir):
            raise argparse.ArgumentTypeError("Error: \"{0}\" is not a valid path".format(prospective_dir))
        if os.access(prospective_dir, os.R_OK):
            setattr(namespace,self.dest,prospective_dir)
        else:
            raise argparse.ArgumentTypeError("Error: \"{0}\" is not a readable dir".format(prospective_dir))

args_parser.add_argument('-c', '--class', type=str, help='The starting class of the dependency tree')
args_parser.add_argument('-l', '--max-levels', type=int, help='How deep you want to go int the dependency tree')
args_parser.add_argument('-p', '--package', type=str, help='Filter by package')
args_parser.add_argument('path', type=str, action=check_dir, help='The path to the project or JAVA file')

try:
    args = args_parser.parse_args()
except argparse.ArgumentTypeError as error:
    print(error)
    exit(0)

def get_cli_arg(key):
    return getattr(args, key)

