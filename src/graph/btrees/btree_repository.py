# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" B* Tree Repository """
from abc import abstractmethod
from graph.btrees.btree_readonly_repository import BTreeReadOnlyRepository


class BTreeRepository(BTreeReadOnlyRepository):
    """
    """
    def __init__(self, page_size):
        """
        """
        super().__init__(page_size)

    @abstractmethod
    def write(self, offset, buffer):
        """
        Writes specific number of bytes from the buffer at the offset.
        """
        raise NotImplementedError("BTreeRepository:read")
