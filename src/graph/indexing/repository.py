# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Repository """
from abc import abstractmethod
from graph.indexing.readonly_repository import ReadOnlyRepository


class Repository(ReadOnlyRepository):
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
        raise NotImplementedError("Repository:read")
