#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import sys
import random
import unittest
from datetime import datetime
from graph.algorithms.sorting import Sorting


class Test(unittest.TestCase):
    @staticmethod
    def generate_random_int_array(n):
        result = [random.randint(1, n) for _ in range(n)]
        return result

    @staticmethod
    def generate_random_array(n):
        result = [random.random() for _ in range(n)]
        return result

    def test_quicksort_empty_success(self):
        array = []
        sorted_array = sorted(array)
        Sorting.quicksort(array)
        assert array == sorted_array

    def test_quicksort_1_success(self):
        array = [1]
        sorted_array = sorted(array)
        Sorting.quicksort(array)
        assert array == sorted_array

    def test_quicksort_2_success(self):
        array = [1, 2]
        sorted_array = sorted(array)
        Sorting.quicksort(array)
        assert array == sorted_array

    def test_quicksort_3_success(self):
        array = [1, 2, 3]
        sorted_array = sorted(array)
        Sorting.quicksort(array)
        assert array == sorted_array

    def test_quicksort_success(self):
        array = [10, 7, 8, 9, 1, 5]
        print(array)
        sorted_array = sorted(array)
        Sorting.quicksort(array)
        print(array)
        assert array == sorted_array

    def test_quicksort_same_success(self):
        array = [1] * 1000
        print(array)
        sorted_array = sorted(array)
        Sorting.quicksort(array)
        print(array)
        assert array == sorted_array

    def test_quicksort_random_int_success(self):
        now = datetime.now()
        print(f"Start: {now}")
        n = 1000  # watch recursion
        for k in range(100):
            array = Test.generate_random_int_array(random.randint(1, 10000))
            sorted_array = sorted(array)
            Sorting.quicksort(array)
            assert array == sorted_array
        now = datetime.now()
        print(f"End: {now}")

    def test_quicksort_random_success(self):
        now = datetime.now()
        print(f"Start: {now}")
        n = 1000  # watch recursion
        for k in range(100):
            array = Test.generate_random_array(random.randint(1, 10000))
            sorted_array = sorted(array)
            Sorting.quicksort(array)
            assert array == sorted_array
        now = datetime.now()
        print(f"End: {now}")

    @staticmethod
    def get_lomuto_partition():
        result = Sorting.lomuto_partition
        return result

    def test_quicksort_lomuto_empty_success(self):
        array = []
        sorted_array = sorted(array)
        Sorting.quicksort(array, partition=Test.get_lomuto_partition())
        assert array == sorted_array

    def test_quicksort_lomuto_1_success(self):
        array = [1]
        sorted_array = sorted(array)
        Sorting.quicksort(array, partition=Test.get_lomuto_partition())
        assert array == sorted_array

    def test_quicksort_lomuto_2_success(self):
        array = [1, 2]
        sorted_array = sorted(array)
        Sorting.quicksort(array, partition=Test.get_lomuto_partition())
        assert array == sorted_array

    def test_quicksort_lomuto_3_success(self):
        array = [1, 2, 3]
        sorted_array = sorted(array)
        Sorting.quicksort(array, partition=Test.get_lomuto_partition())
        assert array == sorted_array

    def test_quicksort_lomuto_success(self):
        array = [10, 7, 8, 9, 1, 5]
        print(array)
        sorted_array = sorted(array)
        Sorting.quicksort(array, partition=Test.get_lomuto_partition())
        print(array)
        assert array == sorted_array

    def test_quicksort_lomuto_same_success(self):
        array = [1] * 1000
        print(array)
        sorted_array = sorted(array)
        sys.setrecursionlimit(10000)
        Sorting.quicksort(array, partition=Test.get_lomuto_partition())
        print(array)
        assert array == sorted_array

    def test_quicksort_lomuto_random_int_success(self):
        now = datetime.now()
        print(f"Start: {now}")
        n = 1000  # watch recursion
        for k in range(100):
            array = Test.generate_random_int_array(random.randint(1, 10000))
            sorted_array = sorted(array)
            Sorting.quicksort(array, partition=Test.get_lomuto_partition())
            assert array == sorted_array
        now = datetime.now()
        print(f"End: {now}")

    def test_quicksort_lomuto_random_success(self):
        now = datetime.now()
        print(f"Start: {now}")
        n = 1000  # watch recursion
        for k in range(100):
            array = Test.generate_random_array(random.randint(1, 10000))
            sorted_array = sorted(array)
            Sorting.quicksort(array, partition=Test.get_lomuto_partition())
            assert array == sorted_array
        now = datetime.now()
        print(f"End: {now}")
