#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Entity type """
from value import Value


class Entity(Value):
    """
    """

    def __init__(self, id=0, version='1.0'):
        """
        """
        super().__init__(version)
        self.id = id


    @property
    def get_id(self):
        """
        """
        return self.id
