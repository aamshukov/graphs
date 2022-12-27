#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Main entry point """
import sys
import os
ss = os.getcwd()
import core
from graph.core.flags import Flags
from graph.adt.disjoint_set import DisjointSet


def main(args):
    """
    """
    try:
        pass
    except Exception as ex:
        print(ex)
    return 1


if __name__ == '__main__':
    """
    """
    main(sys.argv[1:])
    # buggy microsoft cannot fix the crap --- sys.exit(main(sys.argv[1:]))
