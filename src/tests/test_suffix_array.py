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
        string = 'cabbage'
        sa = SuffixArray.build_suffix_array(string)
        assert sa == [7, 1, 4, 3, 2, 0, 6, 5]
        lcp = SuffixArray.build_longest_common_prefix(string, sa)
        assert lcp == [0, 1, 0, 1, 0, 0, 0, 0]

    def test_naive_implementation_rikki_tikki_tikka_success(self):
        string = 'rikki-tikki-tikka'
        sa = SuffixArray.build_suffix_array(string)
        assert sa == [17, 11, 5, 16, 10, 4, 13, 7, 1, 15, 9, 3, 14, 8, 2, 0, 12, 6]
        lcp = SuffixArray.build_longest_common_prefix(string, sa)
        assert lcp == [0, 5, 0, 0, 6, 1, 3, 9, 0, 1, 7, 1, 2, 8, 0, 0, 4, 0]

    def test_naive_implementation_baabaabac_success(self):
        string = 'baabaabac'
        sa = SuffixArray.build_suffix_array(string)
        assert sa == [9, 1, 4, 2, 5, 7, 0, 3, 6, 8]
        lcp = SuffixArray.build_longest_common_prefix(string, sa)
        assert lcp == [0, 4, 1, 3, 1, 0, 5, 2, 0, 0]

    def test_naive_implementation_abracadabra_success(self):
        string = 'ABRACADABRA'
        sa = SuffixArray.build_suffix_array(string)
        assert sa == [11, 10, 7, 0, 3, 5, 8, 1, 4, 6, 9, 2]
        lcp = SuffixArray.build_longest_common_prefix(string, sa)
        assert lcp == [0, 1, 4, 1, 1, 0, 3, 0, 0, 0, 2, 0]

    def test_build_suffix_array_induced_sorting_cabbage_success(self):
        string = 'cabbage'
        sa = SuffixArray.build_suffix_array_induced_sorting(string)
        assert sa == [7, 1, 4, 3, 2, 0, 6, 5]
        lcp = SuffixArray.build_longest_common_prefix(string, sa)
        assert lcp == [0, 1, 0, 1, 0, 0, 0, 0]

    def test_build_suffix_array_induced_sorting_mmiissiissiippii_success(self):
        string = 'mmiissiissiippii'
        sa = SuffixArray.build_suffix_array_induced_sorting(string)
        assert sa == [7, 1, 4, 3, 2, 0, 6, 5]
        lcp = SuffixArray.build_longest_common_prefix(string, sa)
        assert lcp == [0, 1, 0, 1, 0, 0, 0, 0]

    def test_build_suffix_array_induced_sorting_rikki_tikki_tikka_success(self):
        string = 'rikki-tikki-tikka'
        sa = SuffixArray.build_suffix_array_induced_sorting(string)
        assert sa == [17, 11, 5, 16, 10, 4, 13, 7, 1, 15, 9, 3, 14, 8, 2, 0, 12, 6]
        lcp = SuffixArray.build_longest_common_prefix(string, sa)
        assert lcp == [0, 5, 0, 0, 6, 1, 3, 9, 0, 1, 7, 1, 2, 8, 0, 0, 4, 0]


if __name__ == '__main__':
    """
    """
    unittest.main()
