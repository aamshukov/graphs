#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Equatable interface """
import itertools
import inspect
from abc import abstractmethod
from graph.core.base import Base
from graph.core.domain_helper import DomainHelper


class Equatable(Base):
    """
    """

    @abstractmethod
    def __hash__(self):
        """
        """
        result = super().__hash__()
        return result

    @abstractmethod
    def __eq__(self, other):
        """
        """
        return True

    @abstractmethod
    def __lt__(self, other):
        """
        """
        return True

    @abstractmethod
    def __le__(self, other):
        """
        """
        return True

    @staticmethod
    def collect_equality_components(obj):
        """
        """
        result = list()
        attributes = list()
        for attribute in itertools.chain(DomainHelper.collect_dicts(obj),
                                         DomainHelper.collect_slots(obj)):
            attributes.append(attribute)
        props = [prop for prop in attributes if not prop.startswith('_')]
        for prop in props:
            prop_value = getattr(obj, prop, None)
            if (prop_value and
                not inspect.isfunction(prop_value) and
                    not inspect.ismethod(prop_value)):
                if inspect.isclass(type(prop_value)) and issubclass(prop_value.__class__, Equatable):
                    result.extend(Equatable.collect_equality_components(prop_value))
                else:
                    result.append(prop_value)
        return result
