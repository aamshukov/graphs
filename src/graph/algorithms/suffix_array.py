#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
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
        This is Python implementation of C++ code (see algorithms project) based on
          I. 'Linear Suffix Array Construction by Almost Pure Induced-Sorting' Nong, G., Zhang, S. and Chan, W.
              Data Compression Conference, 2009
          II. and on awesome explanation https://zork.net/~st/jottings/sais.html (thanks!)
        """
        string = string + '\0'  # includes virtual sentinel (empty suffix)
        string_len = len(string)

        class SuffixType(str, Enum):
            """
            """
            U = '?',
            S = 'S',
            L = 'L'

        def classify_suffixes():
            """
            Builds S/L-type map (classifies suffixes)
            t: array [0 ... n] of booleans to represent the S-type and L-type vector,
            original paper has [0 ... n - 1] but in our case we have n + 1 elements, + 1 for virtual sentinel
            ...
            SA-IS divides suffixes into two groups: S-type suffixes and L-type suffixes.
            S-type suffixes are smaller (in the sorting sense) than the suffix to their right
            (and so must appear closer to the start of the finished suffix array) and L-type suffixes
            are larger than the suffix to their right (and so appear closer to the end).
            """
            result = [SuffixType.U] * string_len
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

        def classification_to_string(lms_classification):
            """
            """
            part1 = ''.join(str(e.value) for e in lms_classification)
            part2 = ''.join('^' if is_left_most_s_char(k, lms_classification)
                            else ' ' for k in range(len(lms_classification)))
            return f"\n{part1}\n{part2}"

        def is_left_most_s_char(index, lms_classification):
            """
            True if the char at index = i is a left-most S-type (LMS)
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

        class Bucket(object):
            """
            """
            def __init__(self):
                """
                """
                self.size = 0
                self.head = 0
                self.tail = 0
                self.char = 0

            def __repr__(self):
                """
                """
                return f"({self.size},{self.head},{self.tail},{self.char})"
            __str__ = __repr__

        def build_buckets(abc_size=128):
            """
            """
            result = [Bucket() for _ in range(abc_size)]
            # collect stats
            for ch in string:
                k = ord(ch)
                result[k].size += 1
                result[k].char = ch
            # calculate heads
            offset = 0
            for bucket in result:
                if bucket.size > 0:
                    bucket.head = offset
                    offset += bucket.size
            # calculate tails
            offset = 0
            for bucket in result:
                if bucket.size > 0:
                    offset += bucket.size
                    bucket.tail = offset - 1
            return result

        def get_bucket_sizes(sort_buckets):
            """
            """
            return [bucket.size for bucket in sort_buckets]

        def get_bucket_heads(sort_buckets):
            """
            """
            return [bucket.head for bucket in sort_buckets]

        def get_bucket_tails(sort_buckets):
            """
            """
            return [bucket.tail for bucket in sort_buckets]

        def suffix_array_to_string(suffix_array, position=None):
            """
            """
            assert position < len(suffix_array) if position is not None else True
            part1 = ' '.join(f'{e:02d}' for e in suffix_array)
            part2 = ''
            if position is not None:
                part2 = ' '.join('^^' if e == position else '  ' for e in range(len(suffix_array)))
            return f"\n{part1}\n{part2}"

        def place_lms_suffixes(lms_classification, sort_buckets, show=False):
            """
            Puts all LMS suffixes into their appropriate bucket (at the end)
            05 Bucket: $    i                         m       p       s
            06 SA:     {16} {-1 -1 -1 -1 -1 10 06 02} {-1 -1} {-1 -1} {-1 -1 -1 -1}
                                             |  |  | first insertion
                                             |  | second insertion
                                             | third insertion
            """
            result = [-1] * string_len  # LMS suffixes
            tails = get_bucket_tails(sort_buckets)
            for k in range(string_len - 1):  # -1 for excluding virtual sentinel
                if not is_left_most_s_char(k, lms_classification):
                    continue  # not start of LMX suffix
                index = ord(string[k])  # bucket index
                result[tails[index]] = k
                tails[index] -= 1  # move tail index backward to insert the next element
                if show:           # in front of the last inserted element
                    print(suffix_array_to_string(result))
            result[0] = string_len - 1  # set the single sentinel LMS-substring, -1 for excluding virtual sentinel
            if show:
                print(suffix_array_to_string(result))
            return result

        def induce_sort_l_type_suffixes(lms_suffixes, lms_classification, sort_buckets, show=False):
            """
            Places L-type suffixes into correct positions (left-to-right).
            """
            heads = get_bucket_heads(sort_buckets)
            for k in range(len(lms_suffixes)):
                if lms_suffixes[k] == -1:
                    continue  # skip non initialized entries
                j = lms_suffixes[k]  # current suffix ...
                if j == 0:
                    continue  # this entry for the suffix which is the entire string - no suffix to the left of it
                # get the index of the suffix that begins to the left of the suffix this entry points to
                j -= 1  # -1 is left of the current position
                if lms_classification[j] != SuffixType.L:
                    continue  # considering only L-type suffixes
                index = ord(string[j])  # bucket index
                lms_suffixes[heads[index]] = j
                heads[index] += 1  # move head index forward where to insert the next element
                if show:
                    print(suffix_array_to_string(lms_suffixes, k))

        def induce_sort_s_type_suffixes(lms_suffixes, lms_classification, sort_buckets, show=False):
            """
            Places S-type suffixes into positions (right-to-left).
            """
            tails = get_bucket_tails(sort_buckets)
            for k in range(len(lms_suffixes) - 1, -1, -1):  # backwards
                j = lms_suffixes[k]  # current suffix ...
                if j == 0:
                    continue  # this entry for the suffix which is the entire string - no suffix to the left of it
                # get the index of the suffix that begins to the left of the suffix this entry points to
                j -= 1  # -1 is left of the current position
                if lms_classification[j] != SuffixType.S:
                    continue  # considering only S-type suffixes
                index = ord(string[j])  # bucket index
                lms_suffixes[tails[index]] = j
                tails[index] -= 1  # move tail index backward where to insert the next element
                if show:
                    print(suffix_array_to_string(lms_suffixes, k))

        sa = []
        classification = classify_suffixes()
        print(classification_to_string(classification))
        buckets = build_buckets()
        print([bucket for bucket in buckets if bucket.char != 0])
        print(get_bucket_sizes(buckets))
        print(get_bucket_heads(buckets))
        print(get_bucket_tails(buckets))
        suffixes = place_lms_suffixes(classification, buckets, True)
        induce_sort_l_type_suffixes(suffixes, classification, buckets, True)
        induce_sort_s_type_suffixes(suffixes, classification, buckets, True)
        return sa

    @staticmethod
    def collect_suffixes(string, suffixes):
        """
        """
        for suffix in suffixes:
            yield suffix, string[suffix:]

    @staticmethod
    def build_longest_common_prefixes(string, suffixes):
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

    @staticmethod
    def find_longest_repeated_substring(string, algorithm='sa-is'):
        """
        Finds The Longest Repeated Substring (LRS) with overlapping allowed.
        """
        if algorithm is None:
            sa = SuffixArray.build_suffix_array(string)
        else:
            sa = SuffixArray.build_suffix_array_induced_sorting(string)
        lcp = SuffixArray.build_longest_common_prefixes(string, sa)
        lrs_start, lrs_length = 0, 0
        for k in range(len(lcp)):
            if lcp[k] > lrs_length:
                lrs_start, lrs_length = sa[k], lcp[k]
        return lrs_start, lrs_length
