#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Graph algorithms """
from collections import defaultdict
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
        https://en.wikipedia.org/wiki/Topological_sorting#Depth-first_search
        https://www.geeksforgeeks.org/detect-cycle-direct-graph-using-colors/?ref=rp
        Colors:
            WHITE: Vertex is not processed yet. Initially, all vertices are WHITE.
            GRAY: Vertex is being processed (DFS for this vertex has started, but not finished
                  which means that all descendants (in DFS tree) of this vertex are not processed yet
                  or this vertex is in the function call stack.
            BLACK: Vertex and all its descendants are processed.
                   While doing DFS, if an edge is encountered from current vertex to a GRAY vertex,
                   then this edge is back edge and hence there is a cycle.
        """
        assert graph.digraph, "Invalid graph type, must be directed graph."
        result = list()
        stack = list()
        for vertex in graph.vertices.values():
            if vertex.color != Colors.WHITE:  # is being processed or processed
                continue
            stack.append(vertex)  # push
            while stack:
                vertex = stack[-1]  # peek
                if vertex.color == Colors.WHITE:  # about to explore
                    vertex.color = Colors.GRAY
                else:
                    vertex.color = Colors.BLACK  # mark as processed, add to result
                    result.insert(0, stack.pop())
                for adjacence in vertex.adjacencies:
                    if adjacence.vertex.color == Colors.GRAY:
                        raise ValueError("Invalid graph, found a cycle.")
                    else:
                        if adjacence.vertex.color == Colors.WHITE:
                            stack.append(adjacence.vertex)  # push
        return result

    @staticmethod
    def get_topological_order_dfs_colored_gen(graph):
        """
        Based on ... get_topological_order_dfs_colored
        """
        assert graph.digraph, "Invalid graph type, must be directed graph."
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
                    yield stack.pop()
                for adjacence in vertex.adjacencies:
                    if adjacence.vertex.color == Colors.GRAY:
                        raise ValueError("Invalid graph, found a cycle.")
                    else:
                        if adjacence.vertex.color == Colors.WHITE:
                            stack.append(adjacence.vertex)  # push

    @staticmethod
    def get_topological_order_kahn(graph):
        """
        Kahn's algorithm.
        """
        assert graph.digraph, "Invalid graph type, must be directed graph."
        in_degree = {vertex: 0 for vertex in graph.vertices.values()}
        for edge in graph.edges.values():
            in_degree[edge.endpoints[1]] += 1
        stack = list()
        for degree in in_degree.items():
            if degree[1] == 0:
                stack.append(degree[0])  # push
        while stack:
            vertex = stack.pop()  # pop
            yield vertex
            for adjacence in vertex.adjacencies:
                in_degree[adjacence.vertex] -= 1
                if in_degree[adjacence.vertex] == 0:
                    stack.append(adjacence.vertex)  # push

    @staticmethod
    def calculate_tree_traverses(tree):
        """
        Calculates preorder and postorder paths of the tree.
        """
        class Pair:
            __slots__ = ['tree', 'value']

            def __init__(self, tree, value):
                self.tree = tree
                self.value = value

        preorder = list()
        postorder = list()
        stack = [Pair(tree, 1)]  # push
        while stack:
            pair = stack.pop()  # pop
            if pair.value == 1:
                preorder.append(pair.tree)
                pair.value += 1
                stack.append(pair)
                for kid in reversed(pair.tree.kids):
                    stack.append(Pair(kid, 1))  # push
            elif pair.value == 2:  # keep going, for non-binary trees does not make sense
                pair.value += 1
                stack.append(pair)
            else:  # pair.value == 3
                postorder.append(pair.tree)
        return preorder, postorder

    @staticmethod
    def calculate_euler_tour(tree):
        """
        Calculates Euler tour around the tree.
        Mimics:
            def dfs(node):
                nodes.append(node)
                for kid in node.kids:
                    dfs(kid)
                    nodes.append(node)
        """
        nodes = list()   # array of visiting nodes, 2 * N - 1
        lasts = list()   # array of last euler tour indices
        depths = list()  # array of depths of nodes, 2 * N - 1
        stack = [tree]   # push root
        while stack:
            tree = stack[-1]  # peek
            tree.flags |= Flags.VISITED
            nodes.append(tree)
            prev_stack_len = len(stack)
            for kid in tree.kids:
                if (kid.flags & Flags.VISITED) != Flags.VISITED:
                    stack.append(kid)  # push
                    break  # important, mimics left most recursion
            if len(stack) == prev_stack_len:
                stack.pop()  # nodes are removed from stack when there are no more kids to visit
        return nodes, lasts, depths
