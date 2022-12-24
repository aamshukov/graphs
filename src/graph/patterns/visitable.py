#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Visitable design pattern """
from abc import abstractmethod
from graph.core.base import Base


class Visitable(Base):
    """
    """

    @abstractmethod
    def accept(self, visitor, *args, **kwargs):
        """
        """
        pass
