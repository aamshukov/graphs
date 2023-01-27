#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" String extensions """
import ctypes
import functools
import random
import string
from unicodedata import normalize
from graph.core.base import Base


class Text(Base):
    """
    """

    @staticmethod
    def equal(lhs, rhs, case_insensitive=False, normalization_form='NFC'):
        """
        """
        assert lhs is not None
        assert rhs is not None
        nfc = functools.partial(normalize, normalization_form)
        if case_insensitive:
            return nfc(lhs).casefold() == nfc(rhs).casefold()
        else:
            return nfc(lhs) == nfc(rhs)

    class PyUnicodeObject(ctypes.Structure):
        """
        """
        PyUnicode_WCHAR_KIND = 0
        PyUnicode_1BYTE_KIND = 1
        PyUnicode_2BYTE_KIND = 2
        PyUnicode_4BYTE_KIND = 4
        _fields_ = (('kind', ctypes.c_uint, 3), )

    @staticmethod
    def get_string_kind(string):
        """
        """
        return Text.PyUnicodeObject.from_address(id(string)).kind

    @staticmethod
    def list_category(category, filepath=r"D:\Tmp\UnicodeData.txt"):
        """
        """
        with open(filepath) as stream:
            baskets = []
            index = -1
            curr_num = -1
            for _, line in enumerate(stream):
                num, _, cat, _ = line.split(';', 3)
                if cat == category:
                    num = int(num, 16)
                    if num - curr_num != 1:
                        baskets.append([])
                        index += 1
                    baskets[index].append(num)
                    curr_num = num
            result = baskets
        return result

    @staticmethod
    def collect_by_category(category):
        """
        """
        # collect_by_category('Cf')
        print(f"Listing  {category}  category ...")
        ranges = Text.list_category(category)
        # print(ranges)
        result = "    return\n"
        for r in ranges:
            def convert(num):
                res = "{0:#0{1}x}".format(num, 6)
                res = list(res)
                prefix = res[0:2]
                suffix = res[2:]
                suffix = [ch.upper() for ch in suffix]
                res = ''.join(prefix) + ''.join(suffix)
                return res
            start = convert(r[0])
            end = convert(r[len(r)-1])
            # print("{}, {}".format(start, end))
            result += "           in_range(codepoint, {}, {}) ||\n".format(start, end)
        result += ";"
        print(result)

    @staticmethod
    def concatenate_strings_with_sentinels(strings):
        """
        """
        result = ""
        for k, string in enumerate(strings):
            result += string + chr(k)
        return result

    @staticmethod
    def generate_random_string(length):
        """
        """
        data = string.printable
        return ''.join(random.choice(data) for i in range(length))
