#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Edge """
from graph.core.value import Value
from graph.core.flags import Flags


class Edge(Value):
    """
    """

    def __init__(self,
                 value=None,  # edge value, might be weight, etc.
                 flags=Flags.CLEAR,
                 rank=2,  # usually has two vertices and more vertices in hyper-graphs
                 version='1.0'):
        """
        """
        super().__init__(version)
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
