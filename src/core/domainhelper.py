#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Domain helper """
from base import Base


"""
"""
class DomainHelper(Base):
    """
    """

    @staticmethod
    def collect_slots(object):
        """
        """
        result = set()
        for klass in object.__class__.__mro__:
            result.update(getattr(klass, '__slots__', []))
        return result

    @staticmethod
    def collect_dicts(object):
        """
        """
        result = set()
        for klass in object.__class__.__mro__:
            result.update(getattr(klass, '__dict__', []))
        return result
