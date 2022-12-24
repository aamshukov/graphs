#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Value type """
from abc import abstractmethod
from graph.core.equatable import Equatable


class Value(Equatable):
    """
    """

    def __init__(self, version='1.0'):
        """
        """
        super().__init__()
        self._version = version.strip()


    @property
    def version(self):
        """
        """
        return self._version

    @abstractmethod
    def validate(self):
        """
        """
        pass
