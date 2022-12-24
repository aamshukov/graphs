#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Main entry point """
import os
import sys

sys.path.append(os.path.abspath('src/adt'))
sys.path.append(os.path.abspath('src/core'))
sys.path.append(os.path.abspath('src/patterns'))
sys.path.append(os.path.abspath('src/algorithms'))
sys.path.append(os.path.abspath('src'))

from core.logger import Logger
from core.value import Value
from core.entity import Entity
from core.colors import Colors
from core.flags import Flags


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
