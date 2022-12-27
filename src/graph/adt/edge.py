#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Edge """
from graph.core.flags import Flags
from graph.core.entity import Entity


class Edge(Entity):
    """
    """

    def __init__(self,
                 id,
                 value=None,  # edge value, might be weight, etc.
                 rank=2,      # usually has two vertices and more vertices in hyper-graphs
                 flags=Flags.CLEAR,
                 version='1.0'):
        """
        """
        super().__init__(id, version)
        self._endpoints = [None] * rank
        self._value = value
        self._flags = flags

    def __repr__(self):
        """
        """
        return f"{self._value}:{self._flags}:({self._endpoints})"

    __str__ = __repr__

    @property
    def endpoints(self):
        """
        """
        return self._endpoints

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
