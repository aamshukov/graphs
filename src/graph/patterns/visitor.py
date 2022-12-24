#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Visitor design pattern """
from abc import abstractmethod
from graph.core.base import Base


class Visitor(Base):
    """
    """

    @abstractmethod
    def visit(self, visitable, *args, **kwargs):
        """
        """
        pass
