# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Vertex """
from graph.core.flags import Flags
from graph.core.colors import Colors
from graph.core.text import Text
from graph.core.domainhelper import DomainHelper
from graph.core.entity import Entity
from graph.patterns.visitable import Visitable


class Vertex(Entity, Visitable):
    """
    """

    def __init__(self,
                 id,
                 label='',
                 value=None,        # vertex specific value
                 attributes=None,   # vertex specific attributes
                 flags=Flags.CLEAR,
                 color=Colors.UNKNOWN,
                 version='1.0'):
        """
        """
        super().__init__(id, version)
        self._label = label
        self._value = value
        self._attributes = attributes
        self._flags = flags
        self._color = color
        self._adjacencies = list()  # list of Vn/Em pairs (AdjValue)

    def __repr__(self):
        """
        """
        return f"{type(self).__name__}:{self._id}:{self._label}:{self._value}:[{self._attributes}]:" \
               f"{self._flags}:{self._color}:[{self._adjacencies}]]"

    __str__ = __repr__

    def __hash__(self):
        """
        """
        result = super().__hash__()
        result ^= hash(self._label)
        return result

    def __eq__(self, other):
        """
        """
        result = (super().__eq__(other) and
                  Text.equal(self._label, other.label) and
                  self._value == other.value and
                  tuple(self._adjacencies) == tuple(other.adjacencies))
        return result

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
    def attributes(self):
        """
        """
        return self._attributes

    @attributes.setter
    def attributes(self, attributes):
        """
        """
        self._attributes = attributes

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
    def edges(self):
        """
        """
        return [adj.edge for adj in self._adjacencies]

    @property
    def adjacencies(self):
        """
        """
        return tuple(self._adjacencies)

    def add_adjacence(self, vertex, edge):
        """
        """
        self._adjacencies.append(DomainHelper.AdjValue(vertex, edge))

    def remove_adjacence(self, vertex, edge):
        """
        """
        self._adjacencies.remove(DomainHelper.AdjValue(vertex, edge))

    def validate(self):
        """
        """
        pass

    def accept(self, visitor, *args, **kwargs):
        """
        """
        if (self._flags & Flags.VISITED) != Flags.VISITED:
            self._flags = Flags.modify_flags(self._flags, Flags.VISITED, Flags.CLEAR)
            visitor.visit(self, *args, **kwargs)
            for adjacence in self._adjacencies:
                if (adjacence.vertex.flags & Flags.VISITED) != Flags.VISITED:
                    adjacence.vertex.accept(visitor, *args, **kwargs)
