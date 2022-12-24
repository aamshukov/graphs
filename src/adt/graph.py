#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Graph data type """
from ..core.entity import Entity
from vertex import Vertex
from edge import Edge


class Graph(Entity):
    """
    """

    def __init__(self, id=0, digraph=False, version='1.0'):
        """
        """
        super().__init__(id, version)
        self._root = None  # optional, used in some digraph algorithms
        self._digraph;  # directed or not
        self._vertices = set()
        self._edges = set()

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

    def validate(self):
        """
        """
        pass
