#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Vertex """
from graph.core.flags import Flags
from graph.core.colors import Colors
from graph.patterns.visitable import Visitable
from graph.core.entity import Entity


class Vertex(Entity, Visitable):
    """
    """

    def __init__(self,
                 id,
                 label='',
                 value=None,  # vertex value
                 flags=Flags.CLEAR,
                 color=Colors.UNKNOWN,
                 version='1.0'):
        """
        """
        super().__init__(id, version)
        self._label = label
        self._value = value
        self._flags = flags
        self._color = color
        self._ref_count = 0
        self._adjacencies = set()

    def __repr__(self):
        """
        """
        return f"{self._label}:{self._value}:{self._flags}:{self._color}:{self._ref_count}:[{self._adjacencies}]"

    __str__ = __repr__

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
