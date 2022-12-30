#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Graph algorithms """
from graph.core.domainhelper import DomainHelper
from graph.core.base import Base
from graph.adt.vertex import Vertex
from graph.adt.edge import Edge


class GraphAlgorithms(Base):
    """
    """

    @staticmethod
    def collect_predecessors(vertex, graph):
        """
        """
        assert vertex is not None, "Invalid argument 'vertex'"
        assert vertex.id in graph.vertices, f"Missing vertex: {vertex}"
        result = list()
        edges = graph.edges.values()
        for edge in edges:
            vertex_u = edge.endpoints[0]
            vertex_v = edge.endpoints[1]
            if vertex_v.id == vertex.id:
                result.append(DomainHelper.AdjValue(vertex_u, edge))
        return result

    @staticmethod
    def collect_successors(vertex, graph):
        """
        """
        assert vertex is not None, "Invalid argument 'vertex'"
        assert vertex.id in graph.vertices, f"Missing vertex: {vertex}"
        result = [adjacence for adjacence in vertex.adjacencies]
        return result
