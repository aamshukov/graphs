#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Depth First Search () DFS visitor"""
from graph.core.flags import Flags
from graph.patterns.visitor import Visitor


class DfsVisitor(Visitor):
    """
    """

    def __init__(self, graph):
        """
        """
        self._graph = graph

    def __repr__(self):
        return self.__class__.__name__

    __str__ = __repr__

    def visit(self, vertex, *args, **kwargs):
        """
        """
        if (vertex.flags & Flags.VISITED) != Flags.VISITED:
            vertex.flags = Flags.modify_flags(vertex.flags, Flags.VISITED, Flags.CLEAR)
            vertex.accept(self, *args, **kwargs)
            yield vertex
            for adjacence in vertex.adjacencies:
                if (adjacence.vertex.flags & Flags.VISITED) != Flags.VISITED:
                    adjacence.vertex.accept(self, *args, **kwargs)
