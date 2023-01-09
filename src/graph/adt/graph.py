#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Graph data type """
import numpy as np
from graph.core.entity import Entity
from graph.adt.edge import Edge


class Graph(Entity):
    """
    """

    def __init__(self,
                 id=0,
                 attributes=None,  # graph specific attributes
                 digraph=False,
                 version='1.0'):
        """
        """
        super().__init__(id, version)
        self._root = None  # optional, used in some digraph algorithms
        self._digraph = digraph  # directed or not
        self._attributes = attributes
        self._vertices = dict()
        self._edges = dict()

    def __repr__(self):
        """
        """
        return f"{type(self).__name__}:{self._digraph}:[{self._vertices}]:({self._edges})"

    __str__ = __repr__

    def __hash__(self):
        """
        """
        raise NotImplemented

    def __eq__(self, other):
        """
        """
        raise NotImplemented

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
    def attributes(self):
        """
        """
        return self._attributes

    @attributes.setter
    def attributes(self, attributes):
        """
        """
        self._attributes = attributes

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

    def matrix(self, value_type=float):
        size = len(self._vertices)
        result = np.zeros((size, size), dtype=value_type)
        for edge in self._edges.values():
            result[edge.endpoints[0].id][edge.endpoints[1].id] = edge.value
        return result

    def add_vertex(self, vertex):
        """
        """
        assert vertex is not None, "Invalid argument 'vertex'"
        assert vertex.id not in self.vertices, f"Vertex already exist: {vertex}"
        self._vertices[vertex.id] = vertex

    def remove_vertex(self, vertex):
        """
        """
        assert vertex is not None, "Invalid argument 'vertex'"
        assert vertex.id in self.vertices, f"Missing vertex: {vertex}"
        edges = self._edges.values()
        for edge in list(edges):
            vertex_u = edge.endpoints[0]
            vertex_v = edge.endpoints[1]
            if vertex_u.id == vertex.id or vertex_v.id == vertex.id:
                self.remove_edge(edge)
        assert len(vertex.adjacencies) == 0
        del self._vertices[vertex.id]

    def add_edge(self, vertex_u, vertex_v, edge_value=None):
        """
        Add new edge either U <-> V or only U -> V in case of digraph
        """
        assert vertex_u is not None, "Invalid argument 'vertex'"
        assert vertex_v is not None, "Invalid argument 'vertex'"
        assert vertex_u.id in self.vertices, f"Missing vertex: {vertex_u}"
        assert vertex_v.id in self.vertices, f"Missing vertex: {vertex_v}"
        edge = Edge(len(self._edges) + 1, [vertex_u, vertex_v], edge_value, version=self._version)
        vertex_u.add_adjacence(vertex_v, edge)  # add adjacent, U -> V
        self._edges[edge.id] = edge
        if not self._digraph:
            edge = Edge(len(self._edges) + 1, [vertex_v, vertex_u], edge_value, version=self._version)
            vertex_v.add_adjacence(vertex_u, edge)  # add adjacent, U <- V
            self._edges[edge.id] = edge

    def remove_edge(self, edge):
        """
        Remove edge, only U -> V case is considered because when populated
        synthetic edges inserted in correct way:
        U -> V and then U <- V.
        """
        assert edge.id is not None, "Invalid argument 'edge'"
        vertex_u = edge.endpoints[0]
        vertex_v = edge.endpoints[1]
        assert vertex_u.id in self.vertices, f"Missing vertex: {vertex_u}"
        assert vertex_v.id in self.vertices, f"Missing vertex: {vertex_v}"
        vertex_u.remove_adjacence(vertex_v, edge)  # break U -> V relation
        del self._edges[edge.id]

    def get_vertex_degree(self, vertex):
        """
        """
        result = len(vertex.adjacencies)
        if self._digraph:
            for adjacency in vertex.adjacencies:
                if adjacency.vertex == vertex:
                    result += 1  # loop contributes 2 to a vertex's degree
        return result

    def is_leaf(self, vertex):
        degree = self.get_vertex_degree(vertex)
        return degree == 1 or degree == 0

    def validate(self):
        """
        """
        pass
