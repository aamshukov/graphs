#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Entity type """
from abc import abstractmethod
from graph.core.value import Value


class Entity(Value):
    """
    """

    def __init__(self, id, version='1.0'):
        """
        """
        super().__init__(version)
        self._id = id

    @abstractmethod
    def __hash__(self):
        """
        """
        result = super().__hash__() ^ hash(self._id)
        return result

    @abstractmethod
    def __eq__(self, other):
        """
        """
        result = (super().__eq__(other) and
                  self._id == other.id)
        return result

    @abstractmethod
    def __lt__(self, other):
        """
        """
        result = (super().__lt__(other) and
                  self._id < other.id)
        return result

    @abstractmethod
    def __le__(self, other):
        """
        """
        result = (super().__le__(other) and
                  self._id <= other.id)
        return result

    @property
    def id(self):
        """
        """
        return self._id

    def validate(self):
        """
        """
        pass
