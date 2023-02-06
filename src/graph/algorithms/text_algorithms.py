#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Text algorithms """
from functools import lru_cache
from graph.core.base import Base


class TextAlgorithms(Base):
    """
    """

    @staticmethod
    def search_text_kmp(text, pattern, how_many=0):
        """
        Knuth Morris Pratt (KMP) algorithm string matching.
        https://binary-baba.medium.com/string-matching-kmp-algorithm-27c182efa387
        """
        @lru_cache
        def calculate_longest_prefix_suffix_array(pattern0):
            """
            Calculates the Longest (Proper) Prefix Suffix (LSP) array of lengths.
            tp - top pointer, tracks LPS entries
            bp - bottom pointer, iterates over pattern
            """
            lps0 = [0] * len(pattern0)
            tp = 0
            for bp in range(1, len(pattern0)):  # starts from 1 because lps[0] = 0, always
                # phase 1: calibrate start index - roll tp back to 0 or to a match
                while tp and pattern0[tp] != pattern0[bp]:
                    tp = lps0[tp - 1]
                # phase 2: while symbols match (tp == bp) move both kids
                if pattern0[tp] == pattern0[bp]:
                    tp += 1  # bp advanced implicitly by loop
                    lps0[bp] = tp
                # phase 3: mimics - move bp until matches the first symbol at tp
                #   bp += 1
                #   lps0[tp] = 0
            return lps0

        assert text, "Text is empty."
        assert pattern, "Pattern is empty."
        result = list()  # list of found indices
        lps = calculate_longest_prefix_suffix_array(pattern)
        pattern_k = 0
        for text_k, ch in enumerate(text):
            # phase 1: calibrate index - rollback pattern's index
            while pattern_k and pattern[pattern_k] != ch:
                pattern_k = lps[pattern_k - 1]
            # phase 2: while symbols match move both kids
            if pattern[pattern_k] == ch:
                if pattern_k == len(pattern) - 1:  # if end of pattern
                    result.append(text_k - pattern_k)
                    if len(result) == how_many:
                        break
                    pattern_k = lps[pattern_k]
                else:
                    pattern_k += 1  # text_k advanced implicitly by loop
            # phase 3: mimics - move on until text_k matches the first pattern's symbol at pattern_k
            #   text_k += 1
        return result
