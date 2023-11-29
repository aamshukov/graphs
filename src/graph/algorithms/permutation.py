#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Permutation """
from copy import deepcopy
from graph.core.base import Base


class Permutation(Base):
    """
    """ # noqa
    @staticmethod
    def rank(permutation):
        """
        Wendy Myrvold, Frank Ruskey, April 2000
        'Ranking and Unranking Permutations in Linear Time'
        ALGORITHM 317 (CACM) April-May-July 1967
        Charles L. Robinson
        Institute for Computer Research, U. of Chicago, Chicago, Ill.
        """ # noqa
        def _rank(_p, _pr, _n):
            if _n == 1:
                return 0
            s = _p[_n - 1]
            _p[_n - 1], _p[_pr[_n - 1]] = _p[_pr[_n - 1]], _p[_n - 1]
            _pr[s], _pr[_n - 1] = _pr[_n - 1], _pr[s]
            return s + _n * _rank(_p, _pr, _n - 1)

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
        https://gist.github.com/begriffs/2211881
        """ # noqa
        perm = set(permutation)
        result = list()
        while perm:
            n = perm.pop()
            cycle = [n]
            while True:
                n = permutation[n]
                if n not in perm:
                    break
                perm.remove(n)
                cycle.append(n)
            if len(cycle) > 1 or keep_singles:
                result.append(cycle)
        return result

    @staticmethod
    def cycles_to_string(cycles):
        """
        """ # noqa
        return ' '.join(["(" + " ".join([str(e + 1) for e in cycle]) + ")" for cycle in cycles])
