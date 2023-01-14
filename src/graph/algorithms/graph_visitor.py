#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Depth First Search () DFS visitor """
from abc import abstractmethod
from graph.patterns.visitor import Visitor


class GraphVisitor(Visitor):
    """
    """

    def __init__(self, graph):
        """
        """
        self._graph = graph

    def __repr__(self):
        return self.__class__.__name__

    __str__ = __repr__

    @abstractmethod
    def visit(self, vertex, *args, **kwargs):
        """
        """
        pass
