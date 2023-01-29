#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import os
import random
import re
import unittest
from graph.core.text import Text
from graph.algorithms.text_algorithms import TextAlgorithms


class Test(unittest.TestCase):
    def test_search_text_kmp_success(self):
        text = 'ACABACACDACABACACD'
        pattern = 'ACABACACD'
        kmp_result = TextAlgorithms.search_text_kmp(text, pattern, how_many=0)
        assert kmp_result == [0, 9]
        print(kmp_result)
        result = [m.start() for m in re.finditer(pattern, text)]
        assert kmp_result == result
        text = 'ACABACACD'
        pattern = 'ACA'
        kmp_result = TextAlgorithms.search_text_kmp(text, pattern, how_many=0)
        assert kmp_result == [0, 4]
        print(kmp_result)
        result = [m.start() for m in re.finditer(pattern, text)]
        assert kmp_result == result
        kmp_result = TextAlgorithms.search_text_kmp(text, pattern, how_many=1)
        assert kmp_result == [0]
        print(kmp_result)
        result = [m.start() for m in re.finditer(pattern, text)]
        assert kmp_result == result[:1]

    def test_search_text_kmp_complex_success(self):
        text = 'ACABACACDACABACACD'
        pattern = 'ACABACACD'
        kmp_result = TextAlgorithms.search_text_kmp(text, pattern, how_many=0)
        assert kmp_result == [0, 9]
        print(kmp_result)
        result = [m.start() for m in re.finditer(pattern, text)]
        assert kmp_result == result
        text = 'ACABACACD'
        pattern = 'ACA'
        kmp_result = TextAlgorithms.search_text_kmp(text, pattern, how_many=0)
        assert kmp_result == [0, 4]
        print(kmp_result)
        result = [m.start() for m in re.finditer(pattern, text)]
        assert kmp_result == result
        kmp_result = TextAlgorithms.search_text_kmp(text, pattern, how_many=1)
        assert kmp_result == [0]
        print(kmp_result)
        result = [m.start() for m in re.finditer(pattern, text)]
        assert kmp_result == result[:1]
        text = '.6|45g[L0aU?RH24 ;``H2 \x0bF#"w:[g3\x0b*?y"^fEg=AO*$"8Xf>,:ClXp-S*BsAKW9L/=+muL~+V?{d4@11fA+_diS<t+P '
        pattern = '1fA+_di'
        kmp_result = TextAlgorithms.search_text_kmp(text, pattern, how_many=0)
        result = Text.find_all_substrings(text, pattern)
        assert kmp_result == result

    def test_search_text_kmp_random_success(self):
        def test_case(length):
            text = Text.generate_random_string(length)
            lhs = random.randint(0, length)
            rhs = random.randint(lhs, length)
            if lhs > rhs:
                lhs = rhs
            pattern = text[lhs:rhs]
            if not pattern:
                return
            kmp_result = TextAlgorithms.search_text_kmp(text, pattern, how_many=0)
            result = Text.find_all_substrings(text, pattern)
            assert kmp_result == result

        for k in range(1, 1000):
            test_case(k)
        for k in range(1, 10001):
            test_case(11 * k)


if __name__ == '__main__':
    """
    """
    unittest.main()
