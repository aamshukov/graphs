# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Vertex """
from graph.core.flags import Flags
from graph.core.colors import Colors
from graph.core.text import Text
from graph.core.entity import Entity
from graph.patterns.visitable import Visitable


class Tree(Entity, Visitable):
    """
    """

    def __init__(self,
                 id,
                 label='',
                 value=None,        # vertex specific value
                 attributes=None,   # vertex specific attributes
                 flags=Flags.CLEAR,
                 color=Colors.UNKNOWN,
                 papa=None,
                 version='1.0'):
        """
        """
        super().__init__(id, version)
        self._label = label
        self._value = value
        self._attributes = attributes
        self._flags = flags
        self._color = color
        self._papa = papa
        self._kids = list()

    def __repr__(self):
        """
        """
        return f"{type(self).__name__}:{self._id}:{self._label}:{self._value}:[{self._attributes}]:" \
               f"{self._flags}:{self._color}:{self._papa}:[{self._kids}]]"

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
                  self._papa == other.papa and
                  tuple(self._kids) == tuple(other.kids))
        return result

    def __lt__(self, other):
        """
        """
        result = (super().__lt__(other) and
                  self._value < other.value)
        return result

    def __le__(self, other):
        """
        """
        result = (super().__le__(other) and
                  self._value <= other.value)
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
    def papa(self):
        return self._papa

    @papa.setter
    def papa(self, papa):
        self._papa = papa

    @property
    def kids(self):
        return tuple(self._kids)

    def add_kid(self, kid):
        """
        """
        kid.papa = self
        self._kids.append(kid)

    def remove_kid(self, kid):
        """
        """
        kid.papa = None
        self._kids.remove(kid)

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
            for kid in self._kids:
                if (kid.flags & Flags.VISITED) != Flags.VISITED:
                    kid.accept(visitor, *args, **kwargs)
