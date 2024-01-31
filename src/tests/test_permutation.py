#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import unittest
from graph.algorithms.permutation import Permutation


class Test(unittest.TestCase):
    def test_permutation_rank_unrank_1_success(self):
        p = [0, 1, 2, 3]
        r = Permutation.rank(p)
        print(f'{r}: {[e + 1 for e in p]}')
        assert r == 23
        p0 = Permutation.unrank(r, len(p))
        assert p0 == p

    def test_permutation_unrank_success(self):
        for k in range(24):
            p = Permutation.unrank(k, 4)
            print(f'{k}: {[e + 1 for e in p]}')
            r = Permutation.rank(p)
            print(f'{r}: {[e + 1 for e in p]}')
            p0 = Permutation.unrank(r, len(p))
            assert p0 == p

    def test_permutation_cycles_1_success(self):
        permutation = [0, 1, 2]
        cycles = Permutation.calculate_cycles(permutation, keep_singles=True)
        print(Permutation.cycles_to_string(cycles))
        assert cycles == [[0], [1], [2]]

    def test_permutation_3_cycles_success(self):
        """
        https://mathworld.wolfram.com/PermutationCycle.html
            1:  2 3 1   (1 2 3)
            2:  3 1 2   (1 3 2)
            3:  2 1 3   (1 2) (3)
            4:  3 2 1   (1 3) (2)
            5:  1 3 2   (1) (2 3)
            6:  1 2 3   (1) (2) (3)
        """  # noqa
        for k in range(6):
            permutation = Permutation.unrank(k, 3)
            cycles = Permutation.calculate_cycles(permutation, keep_singles=True)
            p = permutation
            print(f'{k + 1}:  {" ".join([str(e) for e in [e + 1 for e in p]])}   {Permutation.cycles_to_string(cycles)}')
            assert cycles

    def test_permutation_4_cycles_success(self):
        for k in range(23):  # ends at 23 as 24th permutation 1,2,3,4 has all single-cycles 0: (1) (2) (3) (4)
            permutation = Permutation.unrank(k, 4)
            cycles = Permutation.calculate_cycles(permutation, keep_singles=False)
            p = permutation
            print(f'{k + 1}:  {" ".join([str(e) for e in [e + 1 for e in p]])}   {Permutation.cycles_to_string(cycles)}')
            assert cycles

    def test_permutation_8_cycles_success(self):
        for k in range(40320 - 1):  # -1 to avoid single-cycle at the end
            permutation = Permutation.unrank(k, 8)
            cycles = Permutation.calculate_cycles(permutation, keep_singles=False)
            p = permutation
            print(f'{k + 1}:  {" ".join([str(e) for e in [e + 1 for e in p]])}   {Permutation.cycles_to_string(cycles)}')
            assert cycles
