#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
# This is Python implementation of my C++ code based on
#  I. 'Linear Suffix Array Construction by Almost Pure Induced-Sorting' Nong, G., Zhang, S. and Chan, W.
#      Data Compression Conference, 2009
#  II. and on awesome explanation https://zork.net/~st/jottings/sais.html (thanks!)
#
""" Suffix Array """
from enum import Enum
from graph.core.base import Base


class SuffixArray(Base):
    """
    """

    @staticmethod
    def build_suffix_array(string):
        """
        Naive and slow Suffix Array (SA) construction implementation.
        Based on https://zork.net/~st/jottings/sais.html#lms-substrings
        """
        suffixes = []
        string = string + '\0'  # includes virtual sentinel (empty suffix)
        len_string = len(string)
        for offset in range(len_string):
            suffixes.append(string[offset:])
        suffixes.sort()
        suffix_array = []
        for suffix in suffixes:
            offset = len_string - len(suffix)
            suffix_array.append(offset)
        return suffix_array

    @staticmethod
    def build_suffix_array_induced_sorting(string):
        """
        Suffix Array Induced-Sorting (SA-IS) algorithm implementation.
        """
        string = string + '\0'  # includes virtual sentinel (empty suffix)
        string_len = len(string)

        class SuffixType(str, Enum):
            S = 'S',
            L = 'L'

        def classify_suffixes():
            """
            builds S/L-type map (classifies suffixes)
            t: array [0 ... n] of booleans to represent the S-type and L-type vector,
            original paper has [0 ... n - 1] but in our case we have n + 1 elements, + 1 for virtual sentinel
            ...
            SA-IS divides suffixes into two groups: S-type suffixes and L-type suffixes.
            S-type suffixes are smaller (in the sorting sense) than the suffix to their right
            (and so must appear closer to the start of the finished suffix array) and L-type suffixes
            are larger than the suffix to their right (and so appear closer to the end).
            """
            result = [0] * string_len
            # the last suffix suf(S, n −1) (after the last character) consisting of
            # only the single character $ or 0 (the sentinel) is defined as S-type.
            result[-1] = SuffixType.S
            if string_len > 1:
                # the suffix containing only the last character (the last before virtual sentinel)
                # must necessarily be larger than the empty suffix, so it is L-type.
                result[-2] = SuffixType.L
                # properties:
                #  (i)  S[i] is S-type if (i.1)  S[i] < S[i + 1] or (i.2)  S[i] = S[i + 1] and suf(S, i + 1) is S-type
                #  (ii) S[i] is L-type if (ii.1) S[i] > S[i + 1] or (ii.2) S[i] = S[i + 1] and suf(S, i + 1) is L-type
                for k in range(string_len - 2, -1, -1):  # right to left
                    if string[k] > string[k + 1]:
                        result[k] = SuffixType.L
                    elif string[k] == string[k + 1] and result[k + 1] == SuffixType.L:
                        result[k] = SuffixType.L
                    else:
                        result[k] = SuffixType.S
            return result

        def is_left_most_s_char(index, lms_classification):
            """
            true if the char at index = i is a left-most S-type (LMS)
            if i == 0 -> true
            from the paper:
                00 Index: 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16
                01 S:      m  m  i  i  s  s  i  i  s  s  i  i  p  p  i  i  $
                02 t:      L  L  S  S  L  L  S  S  L  L  S  S  L  L  L  L  S
                03 LMS:          *           *           *                 *
                                                                           |
                                                                     always true
            ...
            Let’s say that some particular character in our input string is an S-character
            if an S-type suffix starts at that location (and likewise for an L character).
            A left-most S character (or LMS character for short), is just an S character
            that has an L character to its immediate left. The first character in the string can
            never be an LMS character (because there’s no character to the immediate left).
            ...
            cabbage
            LSLLSLLS
             ^  ^  ^
            caaaabbage
            LSSSSLLSLLS
             ^     ^  ^
            mmiissiissiippii
            LLSSLLSSLLSSLLLLS
              ^   ^   ^     ^
            """
            return (index > 0 and
                    lms_classification[index] == SuffixType.S and
                    lms_classification[index - 1] == SuffixType.L)

        def print_classification(lms_classification):
            print(''.join(str(e.value) for e in lms_classification))
            print(''.join('^' if is_left_most_s_char(k, lms_classification)
                          else ' ' for k in range(len(lms_classification))))

        def lms_substrings_are_equal(lms_classification,
                                     index_a,   # first string start offset/index
                                     index_b):  # second string start offset/index
            """
            An "LMS substring" is a portion of the input string starting at one LMS character and
            continuing up to (but not including) the next LMS character.
            In the string cabbage examined above, there are two LMS substrings: abb and age.
            ...
            Definition 2.2. (LMS-substring) A LMS-substring is (i) a substring S[i..j] with both S[i] and S[j]
            being LMS characters, and there is no other LMS character in the substring,
            for i != j; or (ii) the sentinel itself.
            ...
            """
            result = False
            if index_a < string_len and index_b < string_len:
                k = 0  # if progressed
                while True:
                    a_is_lms = is_left_most_s_char(k + index_a, lms_classification)
                    b_is_lms = is_left_most_s_char(k + index_b, lms_classification)
                    #  found start of the next LMS substrings ...
                    if k > 0 and a_is_lms and b_is_lms:  # ... and at least one element progressed
                        result = True
                        break
                    if a_is_lms != b_is_lms:  # LMS mismatch
                        break
                    if string[k + index_a] != string[k + index_b]:  # content mismatch
                        break
                    k += 1  # advance to the next element
            return result

        sa = []
        classification = classify_suffixes()
        print_classification(classification)
        return sa

    @staticmethod
    def build_longest_common_prefix(string, suffixes):
        """
        T. Kasai, G. Lee, H. Arimura, S.Arikawa and K. Park,
        "Linear-time longest-common-prefix computation in suffix arrays and its applications",
        Proc 12th Annual Conference on Combinatorial Pattern Matching, Springer, LNCS 2089 (2001) 181-192.
        """
        string = string + '\0'  # includes virtual sentinel (empty suffix)
        n = len(suffixes)
        lcp = [0] * n
        rank = [0] * n
        for i in range(n):
            rank[suffixes[i]] = i
        k = 0
        for i in range(n):
            if rank[i] == n - 1:
                k = 0
                continue
            j = suffixes[rank[i] + 1]
            while i + k < n and j + k < n and string[i + k] == string[j + k]:
                k += 1
            lcp[rank[i]] = k
            if k > 0:
                k -= 1
        return lcp
