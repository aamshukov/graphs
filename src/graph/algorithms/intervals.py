#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Intervals algorithms """
import math
from graph.core.base import Base


class Intervals(Base):
    """
    """

    @staticmethod
    def compress(intervals):
        """
        ChatGPT generated crap!!!
        """
        intervals_with_index = list(enumerate(intervals))
        intervals_with_index.sort(key=lambda x: x[1][0])
        compressed = []
        current, current_original = intervals_with_index[0]
        for index, interval in intervals_with_index[1:]:
            if interval[0] <= intervals[current][1] + 1:
                current = (current[0], max(intervals[current][1], interval[1]))
                current_original.append(index)
            else:
                compressed.append((intervals[current], current_original))
                current, current_original = interval, [index]
        compressed.append((intervals[current], current_original))
        return compressed

    @staticmethod
    def decompress(compressed_intervals):
        """
        ChatGPT generated crap!!!
        """
        result = []
        for compressed_interval in compressed_intervals:
            start, end = compressed_interval[0]
            for index in compressed_interval[1]:
                interval = (start, end)
                result.append(interval)
                start = end
                end = result[index][1]
        return result
