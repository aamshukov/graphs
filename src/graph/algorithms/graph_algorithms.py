#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Graph algorithms """
from collections import deque
from graph.core.flags import Flags
from graph.core.domainhelper import DomainHelper
from graph.core.base import Base


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

    @staticmethod
    def dfs(vertex, *args, **kwargs):
        """
        """
        stack = deque()
        stack.append(vertex)  # push
        while stack:
            vertex = stack.pop()
            if (vertex.flags & Flags.VISITED) == Flags.VISITED:
                continue
            vertex.flags = Flags.modify_flags(vertex.flags, Flags.VISITED, Flags.CLEAR)
            yield vertex
            for adjacence in vertex.adjacencies:
                if (adjacence.vertex.flags & Flags.VISITED) != Flags.VISITED:
                    stack.append(adjacence.vertex)  # push
