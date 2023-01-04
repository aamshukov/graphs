#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Graph algorithms """
from graph.core.flags import Flags
from graph.core.colors import Colors
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
    def dfs(start_vertex, *args, **kwargs):
        """
        """
        stack = list()
        stack.append(start_vertex)  # push
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
    def dfs_postorder(start_vertex, *args, **kwargs):
        """
        """
        stack = list()
        stack.append(start_vertex)  # push
        while stack:
            vertex = stack.pop()
            if (vertex.flags & Flags.VISITED) == Flags.VISITED:
                continue
            vertex.flags = Flags.modify_flags(vertex.flags, Flags.VISITED, Flags.CLEAR)
            for adjacence in vertex.adjacencies:
                if (adjacence.vertex.flags & Flags.VISITED) != Flags.VISITED:
                    stack.append(adjacence.vertex)  # push
            yield vertex

    @staticmethod
    def bfs(start_vertex, *args, **kwargs):
        """
        """
        queue = list()
        queue.append(start_vertex)  # enqueue
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
    def find_tree_centers(graph):
        """
        Finds tree center(s) by 'pilling off onion' - removing leafs' layer by layer.
        Can be up to two centers.
        """
        assert not graph.digraph, "Invalid graph type, must be undirected graph."
        roots = {v: v.degree for v in graph.vertices.values()}
        while True:
            excluded_roots = list()
            for root in roots.items():
                if root[0].leaf or root[1] < 2:            # '< 2' because can be only up to 2 roots - alternative way
                    for adjacence in root[0].adjacencies:  # to find root(s) is to find the longest path and take its
                        if adjacence.vertex in roots:      # middle, the longest path might be even or odd, that's way 2
                            roots[adjacence.vertex] -= 1
                    excluded_roots.append(root[0])
            if not excluded_roots:
                roots.clear()  # no centers, 'leaf' nodes might have cycles
                break
            elif len(excluded_roots) != len(roots):
                for root in excluded_roots:
                    del(roots[root])
            else:
                break
        return [v for v in roots.keys()]

    @staticmethod
    def get_topological_order_dfs_colored(graph):
        """
        Based on HelloKoding
        https://hellokoding.com/topological-sort/
        """
        assert graph.digraph, "Invalid graph type, must be directed graph."
        result = list()
        stack = list()
        for vertex in graph.vertices.values():
            if vertex.color != Colors.WHITE:
                continue
            stack.append(vertex)  # push
            while stack:
                vertex = stack[-1]  # peek
                if vertex.color == Colors.WHITE:
                    vertex.color = Colors.GRAY
                else:
                    vertex.color = Colors.BLACK
                    result.append(stack.pop())
                for adjacence in vertex.adjacencies:
                    if adjacence.vertex.color == Colors.GRAY:
                        raise ValueError("Invalid graph, found a cycle.")
                    else:
                        if adjacence.vertex.color == Colors.WHITE:
                            stack.append(adjacence.vertex)  # push
        return [result[k] for k in range(len(result)-1, -1, -1)]
