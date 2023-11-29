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
        permutation = [3, 1, 0, 3]
        cycles = Permutation.calculate_cycles(permutation)
        print(Permutation.cycles_to_string(cycles))
        assert cycles == [[1, 3, 0]]

    def test_permutation_cycles_success(self):
        for k in range(1, 24):  # starts from 1 as 0 permutation 1,2,3,0 has all single-cycles 0: (1) (2) (3) (4)
            permutation = Permutation.unrank(k, 4)
            cycles = Permutation.calculate_cycles(permutation)
            print(f'{k}:  {" ".join([str(e) for e in permutation])}   {Permutation.cycles_to_string(cycles)}')
            assert cycles
