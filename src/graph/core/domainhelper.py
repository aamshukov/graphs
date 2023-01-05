#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Domain helper """
from collections import namedtuple
from graph.core.base import Base


class DomainHelper(Base):
    """
    """

    AdjValue = namedtuple('AdjValue', 'vertex edge')

    @staticmethod
    def collect_slots(obj):
        """
        """
        result = set()
        for klass in obj.__class__.__mro__:
            result.update(getattr(klass, '__slots__', []))
        return result

    @staticmethod
    def collect_dicts(obj):
        """
        """
        result = set()
        for klass in obj.__class__.__mro__:
            result.update(getattr(klass, '__dict__', []))
        return result

    @staticmethod
    def print_matrix(matrix):
        print(matrix)
        print('')
