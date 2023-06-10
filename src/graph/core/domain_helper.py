#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Domain helper """
import os
import sys
import struct
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
        """
        """
        print(matrix)
        print('')

    @staticmethod
    def get_max_int():
        """
        """
        return sys.maxsize

    @staticmethod
    def get_int_size():
        """
        """
        return (sys.maxsize + 1).bit_length()

    @staticmethod
    def generate_random_bytes(length):
        """
        """
        return bytearray(os.urandom(length))

    @staticmethod
    def serialize_string(string):
        """
        """
        string = bytes(string, 'utf-8')
        result = struct.pack("I", len(string)) + string
        return result

    @staticmethod
    def deserialize_string(data, template='I'):
        """
        """
        size = struct.calcsize(template)
        result = struct.unpack(template, data[:size]), data[size:]
        return result[1].decode('utf-8')

    @staticmethod
    def pad_string(string, size, filler=' '):
        """
        """
        return string.rjust(size, filler)
