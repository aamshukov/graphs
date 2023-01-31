# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" B* Tree implementation """
from graph.core.flags import Flags
from graph.core.colors import Colors
from graph.core.text import Text
from graph.adt.tree import Tree
from graph.core.entity import Entity
from graph.patterns.visitable import Visitable


class BTree(Tree):
    """
    """

    def __init__(self,
                 id,
                 version='1.0'):
        """
        """
        super().__init__(id, version)

    def __repr__(self):
        """
        """
        return f"{type(self).__name__}"

    __str__ = __repr__

    def __hash__(self):
        """
        """
        return super().__hash__()

    def __eq__(self, other):
        """
        """
        return super().__eq__(other)

    def __lt__(self, other):
        """
        """
        return super().__lt__(other)

    def __le__(self, other):
        """
        """
        return super().__le__(other)

    def validate(self):
        """
        """
        pass

    def accept(self, visitor, *args, **kwargs):
        """
        """
        pass
