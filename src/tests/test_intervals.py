#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import sys
import random
import unittest
from graph.algorithms.intervals import Intervals


class Test(unittest.TestCase):
    def test_intervals_compression_success(self):
        intervals = [(1, 5), (2, 6), (8, 10), (9, 11)]
        compressed_intervals = [((1, 6), [0, 1]), ((8, 11), [2, 3])]  # Intervals.compress(intervals)
        decompressed_intervals = Intervals.decompress(compressed_intervals)
        assert intervals == decompressed_intervals

