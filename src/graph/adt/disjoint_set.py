#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Disjount set / Union Find """
# based on https://algs4.cs.princeton.edu/15uf/UF.java.html
# by Robert Sedgewick and Kevin Wayne
from graph.core.base import Base


class DisjointSet(Base):
    """
    """

    def __init__(self, elements):
        """
        """
        self._count = len(elements)         # number of elements
        assert self._count > 0, "Disjoin set (union find) ctor, number of element must be positive."
        self._parents = [0] * self._count   # parent[i] = parent of i
        self._ranks = [0] * self._count     # rank[i] = rank of subtree rooted at i
        self._mapping = dict()              # element to index map
        for k, element in enumerate(elements):
            self._parents[k] = k
            self._ranks[k] = 0
            self._mapping[element] = k

    @property
    def count(self):
        """
        """
        return self._count

    def find(self, element):
        """
        """
        r = self._mapping[element]   # get index
        while r != self._parents[r]: # locate root
            self._parents[r] = self._parents[self._parents[r]]  # path compression by halving, full path compression
            r = self._parents[r]                                # is more involving another another loop from
        return r                                                # the original element and up to the root

    def union(self, element1, element2):
        """
        """
        r1 = self.find(element1)
        r2 = self.find(element2)
        if r1 != r2:
            if self._ranks[r1] < self._ranks[r2]:
                self._parents[r1] = r2
            elif self._ranks[r1] > self._ranks[r2]:
                self._parents[r2] = r1
            else:
                self._parents[r2] = r1
                self._ranks[r1] += 1
            self._count -= 1
