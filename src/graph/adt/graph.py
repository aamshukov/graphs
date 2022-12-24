#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Graph data type """
from graph.core.entity import Entity
from graph.adt.vertex import Vertex
from graph.adt.edge import Edge


class Graph(Entity):
    """
    """

    def __init__(self, id=0, digraph=False, version='1.0'):
        """
        """
        super().__init__(id, version)
        self._root = None        # optional, used in some digraph algorithms
        self._digraph = digraph  # directed or not
        self._vertices = set()
        self._edges = set()
        self._synthetic_edges = set();  # holds synthetic edges in undirected graphs

    @property
    def root(self):
        """
        """
        return self._root

    @root.setter
    def root(self, root):
        """
        """
        self._root = root

    @property
    def digraph(self):
        """
        """
        return self._digraph

    @property
    def vertices(self):
        """
        """
        return self._vertices

    @property
    def edges(self):
        """
        """
        return self._edges

    def validate(self):
        """
        """
        pass

    def add_vertex(self, vertex):
        """
        """
        pass

    def remove_vertex(self, vertex):
        """
        """
        pass

    def get_edges(self, vertex):
        """
        """
        pass

    def add_edge(self, vertex_u, vertex_v, edge_value=None):
        """
        """
        pass

    def remove_edge(self, edge):
        """
        """
        pass
