#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" String extensions """
import ctypes
import functools
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
