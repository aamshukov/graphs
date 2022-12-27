#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Graph data type """
from collections import defaultdict
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
        self._vertex_edges_map = defaultdict(lambda: set())  # vertex-to-edges mapping

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

    def add_vertex(self, vertex):
        """
        """
        assert vertex not in self.vertices, f"Vertex already exist: {vertex}"
        vertex.adjacencies.clear()
        self._vertices.add(vertex)

    def remove_vertex(self, vertex):
        """
        """
        assert vertex in self.vertices, f"Missing vertex: {vertex}"
        edges = self.get_edges(vertex)
        for edge in edges:
            self.remove_edge(edge)
        self._vertices.remove(vertex)

    def get_edges(self, vertex):
        """
        """
        return self._vertex_edges_map[vertex]

    def add_edge(self, vertex_u, vertex_v, edge_value=None):
        """
        Add new edge either U <-> V or only U -> V in case of digraph
        """
        assert vertex_u in self.vertices, f"Missing vertex: {vertex_u}"
        assert vertex_v in self.vertices, f"Missing vertex: {vertex_v}"
        # update vertices' adjacencies
        vertex_u.adjacencies().add(vertex_v)    # add adjacent, U -> V
        vertex_v.add_ref()                      # mark V referenced by U
        if not self._digraph:
            vertex_v.adjacencies.add(vertex_u)  # add adjacent, U <- U
            vertex_u.add_ref()                  # mark U referenced by V
        # create edge
        result = Edge(edge_value, self._version)
        result.endpoints[0] = vertex_u
        result.endpoints[1] = vertex_v
        self._edges.add(result)
        # update vertex-to-edges mapping
        self._vertex_edges_map[vertex_u].add(result)
        self._vertex_edges_map[vertex_v].add(result)  # including digraphs
        return result

    def remove_edge(self, edge):
        """
        """
        vertex_u = edge.endpoints[0]
        vertex_v = edge.endpoints[1]
        assert vertex_u in self.vertices, f"Missing vertex: {vertex_u}"
        assert vertex_v in self.vertices, f"Missing vertex: {vertex_v}"
        vertex_u.adjacencies.remove(vertex_v)   # break U, V relation
        vertex_v.adjacencies.discard(vertex_u)  # break V, U relation (discard as it can be digraph)
        self._vertex_edges_map[vertex_u].remove(edge)  # clean up vertex_u-to-edges map
        self._vertex_edges_map[vertex_v].remove(edge)  # clean up vertex_v-to-edges map
        vertex_v.release()      # decrement V ref counter
        if not self._digraph:
            vertex_u.release()  # decrement U ref counter
        self._edges.remove(edge)

    def validate(self):
        """
        """
        pass
