#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Graph data type """
import os
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
        self._vertices = dict()
        self._edges = dict()
        self._vertex_edges_map = defaultdict(lambda: list())  # vertex-to-edges mapping

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
        assert vertex is not None, "Invalid argument 'vertex'"
        assert vertex.id not in self.vertices, f"Vertex already exist: {vertex}"
        vertex.adjacencies.clear()
        self._vertices[vertex.id] = vertex

    def remove_vertex(self, vertex):
        """
        """
        assert vertex is not None, "Invalid argument 'vertex'"
        assert vertex.id in self.vertices, f"Missing vertex: {vertex}"
        edges = self.get_edges(vertex)
        for edge in edges:
            self.remove_edge(edge)
        del(self._vertices[vertex.id])

    def get_edges(self, vertex):
        """
        """
        return self._vertex_edges_map[vertex]

    def add_edge(self, vertex_u, vertex_v, edge_value=None):
        """
        Add new edge either U <-> V or only U -> V in case of digraph
        """
        assert vertex_u is not None, "Invalid argument 'vertex'"
        assert vertex_v is not None, "Invalid argument 'vertex'"
        assert vertex_u.id in self.vertices, f"Missing vertex: {vertex_u}"
        assert vertex_v.id in self.vertices, f"Missing vertex: {vertex_v}"
        # update vertices' adjacencies
        vertex_u.adjacencies.append(vertex_v)   # add adjacent, U -> V
        vertex_v.add_ref()                      # mark V referenced by U
        if not self._digraph:
            vertex_v.adjacencies.append(vertex_u)  # add adjacent, U <- U
            vertex_u.add_ref()                  # mark U referenced by V
        # create edge
        result = Edge(len(self._edges) + 1, edge_value, version=self._version)
        result.endpoints[0] = vertex_u
        result.endpoints[1] = vertex_v
        self._edges[result.id] = result
        # update vertex-to-edges mapping
        self._vertex_edges_map[vertex_u.id].append(result)
        if not self._digraph:
            self._vertex_edges_map[vertex_v.id].append(result)
        return result

    def remove_edge(self, edge):
        """
        """
        assert edge is not None, "Invalid argument 'edge'"
        vertex_u = edge.endpoints[0]
        vertex_v = edge.endpoints[1]
        assert vertex_u.id in self.vertices, f"Missing vertex: {vertex_u}"
        assert vertex_v.id in self.vertices, f"Missing vertex: {vertex_v}"
        vertex_u.adjacencies.remove(vertex_v)   # break U, V relation
        vertex_v.adjacencies.discard(vertex_u)  # break V, U relation (discard as it can be digraph)
        self._vertex_edges_map[vertex_u.id].remove(edge)  # clean up vertex_u-to-edges map
        self._vertex_edges_map[vertex_v.id].remove(edge)  # clean up vertex_v-to-edges map
        vertex_v.release()      # decrement V ref counter
        if not self._digraph:
            vertex_u.release()  # decrement U ref counter
        self._edges.remove(edge.id)

    def validate(self):
        """
        """
        pass

    @staticmethod
    def build_networkx_graph(graph):
        """
        """
        import networkx as nx
        if graph.digraph:
            result = nx.DiGraph()
        else:
            result = nx.Graph()
        for vertex in graph.vertices.values():
            result.add_node(vertex.label)
        for edge in graph.edges.values():
            result.add_edge(edge.endpoints[0].label, edge.endpoints[1].label)
        return result
