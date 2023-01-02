#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Graph algorithms """
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
        return set(result)

    @staticmethod
    def collect_successors(vertex, graph):
        """
        """
        assert vertex is not None, "Invalid argument 'vertex'"
        assert vertex.id in graph.vertices, f"Missing vertex: {vertex}"
        result = [adjacence for adjacence in vertex.adjacencies]
        return set(result)

    @staticmethod
    def collect_incidents(vertex, graph):
        """
        """
        assert vertex is not None, "Invalid argument 'vertex'"
        assert vertex.id in graph.vertices, f"Missing vertex: {vertex}"
        result = list()
        edges = graph.edges.values()
        for edge in edges:
            vertex_u = edge.endpoints[0]
            vertex_v = edge.endpoints[1]
            if vertex_u.id == vertex.id:
                result.append(DomainHelper.AdjValue(vertex_u, edge))
            if vertex_v.id == vertex.id:
                result.append(DomainHelper.AdjValue(vertex_v, edge))
        return set(result)

    @staticmethod
    def dfs(vertex, *args, **kwargs):
        """
        """
        stack = list()
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

    @staticmethod
    def bfs(vertex, *args, **kwargs):
        """
        """
        queue = list()
        queue.append(vertex)  # enqueue
        while queue:
            vertex = queue.pop(0)  # deque
            if (vertex.flags & Flags.VISITED) == Flags.VISITED:
                continue
            vertex.flags = Flags.modify_flags(vertex.flags, Flags.VISITED, Flags.CLEAR)
            yield vertex
            for adjacence in vertex.adjacencies:
                if (adjacence.vertex.flags & Flags.VISITED) != Flags.VISITED:
                    queue.append(adjacence.vertex)  # enqueue

    @staticmethod
    def find_tree_roots(graph):
        """
        """
        roots = {k: v.degree for (k, v) in graph.vertices.items()}
        level = 0
        while True:
            level += 1
            excluded_roots = list()
            for root in roots.items():
                if root[1] - level < 2:             # '< 2' because can be only up to 2 roots - alternative way
                    excluded_roots.append(root[0])  # to find root(s) is to find the longest path and take its middle,
            if len(excluded_roots) != len(roots):   # the longest path might be even or odd, that's way 2
                for root in excluded_roots:
                    del(roots[root])
            else:
                break
        return tuple(roots)
