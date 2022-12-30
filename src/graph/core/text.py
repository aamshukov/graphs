#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" String extensions """
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
