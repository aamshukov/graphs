#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
# https://zork.net/~st/jottings/sais.html#lms-substrings
""" Suffix Array """
from graph.core.base import Base


class SuffixArray(Base):
    """
    """

    @staticmethod
    def build_suffix_array(data):
        """
        """
        suffixes = []
        for offset in range(len(data) + 1):  # includes +1 for virtual sentinel
            suffixes.append(data[offset:])
        suffixes.sort()
        suffix_array = []
        for suffix in suffixes:
            offset = len(data) - len(suffix)
            suffix_array.append(offset)
        return suffix_array
