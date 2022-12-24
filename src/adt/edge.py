#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Edge """
from ..core.value import Value
from ..core.flags import Flags
from vertex import Vertex


class Edge(Value):
    """
    """

    def __init__(self,
                 value=None,  # edge value, might be weight
                 flags=Flags.CLEAR,
                 rank=2,  # usually has two vertices and more vertices in hyper-graphs
                 version='1.0'):
        """
        """
        super().__init__(version)
        self._end_points = [Vertex(version=version)] * rank
        self._value = value
        self._flags = flags

    @property
    def end_points(self):
        """
        """
        return self._end_points

    @property
    def value(self):
        """
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        """
        self._value = value

    @property
    def flags(self):
        """
        """
        return self._flags

    @flags.setter
    def flags(self, flags):
        """
        """
        self._flags = flags

    def validate(self):
        """
        """
        pass
