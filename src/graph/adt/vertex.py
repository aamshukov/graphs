#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Vertex """
from graph.core.value import Value
from graph.core.flags import Flags
from graph.core.colors import Colors
from graph.patterns.visitable import Visitable
from graph.adt.edge import Edge


class Vertex(Value, Visitable):
    """
    """

    def __init__(self,
                 label='',
                 value=None,  # vertex value
                 flags=Flags.CLEAR,
                 color=Colors.UNKNOWN,
                 version='1.0'):
        """
        """
        super().__init__(version)
        self._label = label
        self._value = value
        self._flags = flags
        self._color = color
        self._adjacencies = set()
        self._edges = set()
        self._ref_count = 0

    @property
    def label(self):
        """
        """
        return self._label

    @label.setter
    def label(self, label):
        """
        """
        self._label = label

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

    @property
    def color(self):
        """
        """
        return self._color

    @color.setter
    def color(self, color):
        """
        """
        self._color = color

    @property
    def adjacencies(self):
        """
        """
        return self._adjacencies

    @property
    def edges(self):
        """
        """
        return self._edges

    @property
    def ref_count(self):
        """
        """
        return self._ref_count

    def add_ref(self):
        """
        """
        return ++self._ref_count

    def release(self):
        """
        """
        if self._ref_count > 0:
            self._ref_count -= 1
        else:
            raise Exception("Vertex release ref count error.")
        return self._ref_count

    def validate(self):
        """
        """
        pass

    def accept(self, visitor, *args, **kwargs):
        """
        """
        visitor.visit(self, *args, **kwargs)