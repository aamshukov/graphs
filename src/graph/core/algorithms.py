#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Collection of algorithms """
import math
from enum import IntEnum
from functools import lru_cache
from graph.core.base import Base


class Algorithms(Base):
    """
    """

    class Functions(IntEnum):
        """
        """
        MIN = 0
        MAX = 1

    @staticmethod
    def execute_range_minmax_queries(array, queries, function=Functions.MIN):
        """
        Range Minimum Query (RMQ) implementation based on Sparse Table lookup.
        Based on:
        https://www.youtube.com/watch?v=uUatD9AudXo&list=PLDV1Zeh2NRsB6SWUrDFW2RmDotAfPbeHu&index=55
        """
        assert function in set(item.value for item in Algorithms.Functions), f"Invalid function type {function}."
        n = len(array)  # N

        @lru_cache(maxsize=1024)
        def populate_logs_lut():
            """
            """
            logs = [0] * (n + 1)  # logs lut for floor(log(i)), 1 <= i <= N, index 0 unused
            for k in range(2, n + 1):
                logs[k] = logs[k//2] + 1
            return logs

        def build_luts():
            """
            Builds Sparse and Indices tables. Tables are cached for performance.
            """
            # populate the first row of luts
            p = math.floor(math.log2(n))  # P, row number, the largest 2^P which fits in N
            sparse_table = [[float('-inf')] * n for _ in range(p + 1)]  # sparce table, P+1 rows and N columns
            indices_table = [[0] * n for _ in range(p + 1)]  # indices table, P+1 rows and N columns
            for k in range(0, n):
                sparse_table[0][k] = array[k]
                indices_table[0][k] = k
            # populate luts
            for pk in range(1, p + 1):
                k = 0
                while True:
                    if (k + (1 << pk)) > n:
                        break
                    lhs = sparse_table[pk - 1][k]
                    rhs = sparse_table[pk - 1][k + (1 << (pk - 1))]
                    if function == Algorithms.Functions.MIN:
                        sparse_table[pk][k] = min(lhs, rhs)
                        if lhs <= rhs:
                            indices_table[pk][k] = indices_table[pk - 1][k]
                        else:
                            indices_table[pk][k] = indices_table[pk - 1][k + (1 << (pk - 1))]
                    elif function == Algorithms.Functions.MAX:
                        sparse_table[pk][k] = max(lhs, rhs)
                        if lhs >= rhs:
                            indices_table[pk][k] = indices_table[pk - 1][k]
                        else:
                            indices_table[pk][k] = indices_table[pk - 1][k + (1 << (pk - 1))]
                    # indices ...
                    k += 1
            return sparse_table, indices_table

        logs_lut = populate_logs_lut()
        table, indices = build_luts()

        def min_value_query(lb, rb):
            pk = logs_lut[rb - lb + 1]
            k = 1 << pk
            lhs = table[pk][lb]
            rhs = table[pk][rb - k + 1]
            return min(lhs, rhs)

        def max_value_query(lb, rb):
            pk = logs_lut[rb - lb + 1]
            k = 1 << pk
            lhs = table[pk][lb]
            rhs = table[pk][rb - k + 1]
            return max(lhs, rhs)

        def min_index_query(lb, rb):
            pk = logs_lut[rb - lb + 1]
            k = 1 << pk
            lhs = table[pk][lb]
            rhs = table[pk][rb - k + 1]
            if lhs <= rhs:
                index = indices[pk][lb]
            else:
                index = indices[pk][rb - k + 1]
            return index

        def max_index_query(lb, rb):
            pk = logs_lut[rb - lb + 1]
            k = 1 << pk
            lhs = table[pk][lb]
            rhs = table[pk][rb - k + 1]
            if lhs >= rhs:
                index = indices[pk][lb]
            else:
                index = indices[pk][rb - k + 1]
            return index

        result = list()
        for query in queries:
            if function == Algorithms.Functions.MIN:
                result.append((min_value_query(query[0], query[1]),
                               min_index_query(query[0], query[1])))
            elif function == Algorithms.Functions.MAX:
                result.append((max_value_query(query[0], query[1]),
                               max_index_query(query[0], query[1])))
        return result
