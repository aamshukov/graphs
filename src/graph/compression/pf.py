#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Permutation fantasy based compression """
from graph.core.base import Base


class Pf(Base):
    """
    """

    def __init__(self, version='1.0'):
        """
        """
        super().__init__()
        self.version = version.strip()

    def encode(self, raw_data=None):
        """
        """
        data = [] if raw_data is None else raw_data
        result = data
        return result

    def decode(self, compressed_data):
        """
        """
        data = [] if compressed_data is None else compressed_data
        result = data
        return result
