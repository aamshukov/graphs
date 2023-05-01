#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Sorting algorithms. """
from graph.core.base import Base


class Sorting(Base):
    """
    """
    @staticmethod
    def quicksort(ar, lo=0, hi=None, partition=None):
        """
        Quicksort. Default is Hoare partition scheme.
        https://en.wikipedia.org/wiki/Quicksort#Hoare_partition_scheme
            ar - array to sort
            lo - low/left index
            hi - high/right index
        """
        def _quicksort(_ar, _lo, _hi, _partition):
            if 0 <= _lo < _hi and _hi >= 0:
                k = partition(_ar, _lo, _hi)  # k is pivot index and ar[k] at the right place
                _quicksort(_ar, _lo, k, _partition)
                _quicksort(_ar, k + 1, _hi, _partition)

        def _hoare_partition(_ar, _lo, _hi):
            """
            The original partition scheme described by Tony Hoare uses two pointers (indices into the range)
            that start at both ends of the array being partitioned, then move toward each other, until they detect
            an inversion: a pair of elements, one greater than the bound (Hoare's terms for the pivot value)
            at the first pointer, and one less than the bound at the second pointer; if at this point
            the first pointer is still before the second, these elements are in the wrong order relative
            to each other, and they are then exchanged.[15] After this the pointers are moved inwards,
            and the search for an inversion is repeated; when eventually the pointers cross
            (the first points after the second), no exchange is performed; a valid partition is found,
            with the point of division between the crossed pointers (any entries that might be strictly
            between the crossed pointers are equal to the pivot and can be excluded from both sub-ranges formed).
            With this formulation it is possible that one sub-range turns out to be the whole original range,
            which would prevent the algorithm from advancing.
            """
            pivot = _ar[_lo]  # first/lowest element as pivot
            i = _lo - 1  # left index
            j = _hi + 1  # right index
            while True:
                i += 1  # move the left index to the right at least once (+1) ...
                while _ar[i] < pivot:  # ... and while the element at the left index is less than the pivot
                    i += 1
                j -= 1  # move the right index to the left at least once (-1) ...
                while _ar[j] > pivot:  # ... and while the element at the right index is greater than the pivot
                    j -= 1
                if i >= j:  # if two pointers crossed, either met or crossed
                    return j
                _ar[i], _ar[j] = _ar[j], _ar[i]

        if hi is None:
            hi = len(ar) - 1
        if partition is None:
            partition = _hoare_partition
        _quicksort(ar, lo, hi, partition)
