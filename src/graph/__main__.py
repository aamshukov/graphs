#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Main entry point """
import sys
import os
ss = os.getcwd()
import core
from graph.core.flags import Flags
from graph.adt.disjoint_set import DisjointSet

from graph.adt.vertex import Vertex
from graph.adt.edge import Edge
from graph.adt.graph import Graph

import networkx as nx
import matplotlib.pyplot as plt


class GraphVisualization:
    def __init__(self):
        self.visual = []

    def addEdge(self, a, b):
        temp = [a, b]
        self.visual.append(temp)
          
    def visualize(self):
        import matplotlib
        import matplotlib.pyplot as plt
        plt.style.use('ggplot')
        matplotlib.use( 'tkagg' )
        G = nx.Graph()
        G.add_edges_from(self.visual)
        nx.draw_networkx(G)
        plt.show()


def main(args):
    """
    """
    try:
        G = GraphVisualization()
        G.addEdge(0, 2)
        G.addEdge(1, 2)
        G.addEdge(1, 3)
        G.addEdge(5, 3)
        G.addEdge(3, 4)
        G.addEdge(1, 0)
        # G.visualize()

        import matplotlib
        import matplotlib.pyplot as plt
        plt.style.use('ggplot')
        matplotlib.use('tkagg')
        graph = Graph()
        v1 = Vertex(1, 'odin')
        v2 = Vertex(2, 'dva')
        v3 = Vertex(3, 'three')
        graph.add_vertex(v1)
        graph.add_vertex(v2)
        graph.add_vertex(v3)
        graph.add_edge(v1, v2, 'v1-v2')
        graph.add_edge(v1, v3, 'v1-v3')
        graph.add_edge(v2, v3, 'v2-v3')
        nx_graph = Graph.build_networkx_graph(graph)
        nx.draw_networkx(nx_graph)
        plt.show()
    except Exception as ex:
        print(ex)
    return 1


if __name__ == '__main__':
    """
    """
    main(sys.argv[1:])
    # buggy microsoft cannot fix the crap --- sys.exit(main(sys.argv[1:]))
