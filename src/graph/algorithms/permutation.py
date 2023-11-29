#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Permutation """
from copy import deepcopy
from graph.core.base import Base


class Permutation(Base):
    """
    """
    @staticmethod
    def rank(permutation):
        """
        Wendy Myrvold, Frank Ruskey, April 2000
        'Ranking and Unranking Permutations in Linear Time'
        wendym@csr.uvic.ca  fruskey@csr.uvic.ca
        ALGORITHM 317 (CACM) April-May-July 1967
        Charles L. Robinson
        Institute for Computer Research, U. of Chicago, Chicago, Ill.
        """ # noqa
        def _rank(p, pr, n):
            if n == 1:
                return 0
            s = p[n - 1]
            p[n - 1], p[pr[n - 1]] = p[pr[n - 1]], p[n - 1]
            pr[s], pr[n - 1] = pr[n - 1], pr[s]
            return s + n * _rank(p, pr, n - 1)

        n = len(permutation)
        p = deepcopy(permutation)
        pr = [0] * n
        for k in range(n):
            pr[p[k]] = k
        rank = _rank(p, pr, n)
        return rank

    @staticmethod
    def unrank(rank, size):
        """
        """ # noqa
        p = [0] * size
        for k in range(size):
            p[k] = k
        r = rank
        n = size
        while n > 0:
            lhs = n - 1
            rhs = r % n
            p[rhs], p[lhs] = p[lhs], p[rhs]
            r //= n
            n -= 1
        return p

    @staticmethod
    def calculate_cycles(permutation, keep_singles=False):
        """
        https://rosettacode.org/wiki/Cycles_of_a_permutation#Python
        """ # noqa
        v = permutation
        length = len(v)
        unchecked = [True] * length
        cycles = []
        for idx in range(length):
            if unchecked[idx]:
                c = [idx + 1]
                unchecked[idx] = False
                jidx = idx
                while unchecked[v[jidx] - 1]:
                    jidx = v[jidx]
                    c.append(jidx)
                    jidx -= 1
                    unchecked[jidx] = False
                if len(c) > 1 or keep_singles:
                    cycles.append(c)
        return sorted(cycles)

    @staticmethod
    def cycles_to_string(cycles):
        """
        """ # noqa
        return ' '.join(["(" + " ".join([str(i + 1) for i in c]) + ")" for c in cycles])

