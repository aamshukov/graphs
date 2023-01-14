#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import unittest
from graph.algorithms.suffix_array import SuffixArray


class Test(unittest.TestCase):
    """
    """

    def test_naive_implementation_cabbage_success(self):
        sa = SuffixArray.build_suffix_array('cabbage')
        assert sa == [7, 1, 4, 3, 2, 0, 6, 5]

    def test_naive_implementation_rikki_tikki_tikka_success(self):
        sa = SuffixArray.build_suffix_array('rikki-tikki-tikka')
        assert sa == [17, 11, 5, 16, 10, 4, 13, 7, 1, 15, 9, 3, 14, 8, 2, 0, 12, 6]

    def test_naive_implementation_baabaabac_success(self):
        sa = SuffixArray.build_suffix_array('baabaabac')
        assert sa == [9, 1, 4, 2, 5, 7, 0, 3, 6, 8]


if __name__ == '__main__':
    """
    """
    unittest.main()
