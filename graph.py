from graphviz import Digraph
import pydot
from IPython.display import Image, display
import pydotplus
import os
import sqlite3
import random

DEFAULT_NODE_LEVEL = -1
DEFAULT_NODE_COLOR = '#01b28c'

class Graph:

    conn = None
    cursor = None
    graph = pydot.Dot(
        graph_type="digraph", 
        sep='+30,30', 
        rankdir='TB', 
        rank='same', 
        ranksep='4', 
        nodesep='0',
        overlap=False, 
        splines=True, 
        diredgeconstraints=True,
        levelsgap=3, 
        mode="hier"
    )
    edges = []
    clusters = dict()
    links_colors = dict()
    package_filter = ''
    max_levels=DEFAULT_NODE_LEVEL

    def __init__(self, input_db_path, starting_cls, package_filter='', max_levels=DEFAULT_NODE_LEVEL):

        #Init database
        self.conn = sqlite3.connect(input_db_path)
        self.cursor = self.conn.cursor()

        self.max_levels

        #fetch packages
        self.cursor.execute('SELECT * FROM package')
        packages = self.cursor.fetchall()

        self.package_filter = package_filter
        for package in packages:
            if package[1].startswith(package_filter):
                self.clusters[package[0]] = pydot.Cluster(str(package[0]), bgcolor='#cccccc', label=package[1])

        #fetch links
        c = self.cursor.execute(f'SELECT * FROM class where class_name = "{starting_cls}"')
        orig_cls = c.fetchone()
        assert orig_cls, 'origin class not found'
        orig_cls_id = orig_cls[0]
        self.__add_graph_tree(orig_cls_id)

    def __fetch_direct_links(self, cls_id) -> set:
        """Get direct links to the giving class"""
        c = self.cursor.execute(f'SELECT * FROM link WHERE class_src="{cls_id}"')
        return c.fetchall()

    def __create_cls_node(self, cls_id : str, color=DEFAULT_NODE_COLOR) -> (pydot.Node, int):
        """Create a graph node for a class"""
        c = self.cursor.execute(f'SELECT * FROM class WHERE id="{cls_id}"')
        result = c.fetchone()
        
        #get the class name
        cls_name = result[1]
        print(f'Creating class node : {cls_name}')

        if not result:
            return None, -1

        package_id = result[3]
        c = self.cursor.execute(f'SELECT package_name FROM package WHERE id="{package_id}"')
        package_result = c.fetchone()

        #Select only the project classes
        print(package_result)
        if not package_result  or not package_result[0].startswith(self.package_filter) :
            return None, -1
        
        return pydot.Node(cls_id, label=cls_name, style="filled", fillcolor=color, group=package_id), package_id


    def __add_graph_links(self, links : set) :
        for link in links:
            #if link[2] not in (20, 174, 2, 80) : continue
            node_src, cluster_src_id = self.__create_cls_node(link[1])

            #Add the source class if it doesn't exist
            if node_src : 
                if( not self.clusters[cluster_src_id].get_node(node_src.get_name())):
                    self.clusters[cluster_src_id].add_node(node_src)

            #Add the destination class if it doesn't exist
            node_dst, cluster_dst_id = self.__create_cls_node(link[2])
            if node_dst: 
                if( not self.clusters[cluster_dst_id].get_node(node_dst.get_name())):
                    self.clusters[cluster_dst_id].add_node(node_dst)

            if node_dst and node_src :
                edge = pydot.Edge(node_src, node_dst)
                edge.set_parent_graph(self.graph)
                if edge not in self.edges:
                    self.edges.append(edge)

    def __get_link_count(self, cls_id, in_graph=True):

        if in_graph:
            count = 0
            for edge in self.edges:
                if(edge.get_destination() == cls_id):
                    count += 1
            return count

        c = self.cursor.execute(f'SELECT count(id) FROM link WHERE class_dst="{cls_id}"')
        count = c.fetchone()
        if(count) : return count[0]
        else : return 0

    def __get_dependencies_count(self, cls_id, in_graph=True):

        if in_graph:
            count = 0
            for edge in self.edges:
                if(edge.get_destination() == cls_id):
                    count += 1
            return count

        c = self.cursor.execute(f'SELECT count(id) FROM link WHERE class_src="{cls_id}"')
        count = c.fetchone()
        if(count) : return count[0]
        else : return 0

    def __add_graph_tree(self, cls_id : int, level=0, existing_links=set(), existing_tree=set()) : 
        links = self.__fetch_direct_links(cls_id)

        #Check the deep
        if(self.max_levels >= 0 and level >= self.max_levels):
            return
        
        if links : 

            #print(f'[tree] after => {links})')
            #print(f'[tree] existing => {existing_links})')
            for link in links :
                if(link[0] not in existing_links) :
                    print(f'[tree] exist => {link})')
                    existing_links.add(link[0])
                else :
                    print(f'[tree] remove => {link})')
                    links.remove(link)

            #print(f'[tree] before => {links})')
            print(f'[tree] links => {links})')
            self.__add_graph_links(links)        
            for link in links :
                if(link[2] not in existing_tree) :
                    print(f'[tree] search deeper => {link[2]})')
                    existing_tree.add(link[2])
                    self.__add_graph_tree(link[2], level + 1, existing_links, existing_tree)
            

    def create_graph(self):
            #add clusters to the global graph
        for _, cluster in self.clusters.items():

            for node in cluster.get_nodes():
                links_count = self.__get_link_count(node.get_name())
                print(f'count = {node.get_name()} => {links_count}')
                if(links_count >= 10):
                    node.set_fillcolor('#a73b00')

            self.graph.add_subgraph(cluster)
                
        #and finally add all links
        for edge  in self.edges:
            if(edge.get_source() not in self.links_colors.keys()):
                self.links_colors[edge.get_source()] = hex(random.randint(0, 0xFFFFFF)).replace('0x', '#')
            
            edge.set_color(self.links_colors[edge.get_source()])
            edge.set_penwidth(3)
            self.graph.add_edge(edge)

        self.graph.write('example1_graph.png',prog='dot', format='png')