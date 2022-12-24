#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Value type """
from abc import abstractmethod
from equatable import Equatable


class Value(Equatable):
    """
    """

    def __init__(self, version='1.0'):
        """
        """
        super().__init__()
        self.version = version.strip()


    @property
    def get_version(self):
        """
        """
        return self.version

    @abstractmethod
    def validate(self):
        """
        """
        pass
