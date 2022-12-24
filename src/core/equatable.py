#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Equatable interface """
import itertools
import inspect
from base import Base
from domainhelper import DomainHelper


class Equatable(Base):
    """
    """

    def __eq__(self, other):
        """
        """
        super().__init__()
        result = isinstance(other, Equatable)
        if result:
            lhs = Equatable.collect_equality_components(self)
            rhs = Equatable.collect_equality_components(other)
            result = len(lhs) == len(rhs)
            if result:
                for lhs_item, rhs_item in zip(lhs, rhs):
                    if lhs_item != rhs_item:
                        result = False
                        break
        return result


    @staticmethod
    def collect_equality_components(object):
        """
        """
        result = list()
        attributes = list()
        for attribute in itertools.chain(DomainHelper.collect_dicts(object),
                                         DomainHelper.collect_slots(object)):
            attributes.append(attribute)
        properties = [property for property in attributes if property.startswith('get_')]
        for property in properties:
            property_value = getattr(object, property, None)
            if property_value:
                if inspect.isclass(type(property_value)) and issubclass(property_value.__class__, Equatable):
                    result.extend(Equatable.collect_equality_components(property_value))
                else:
                    result.append(property_value)
        return result