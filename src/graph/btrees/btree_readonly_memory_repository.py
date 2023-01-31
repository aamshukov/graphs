# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" B* Tree In-Memory Repository """
from graph.btrees.btree_repository import BTreeReadOnlyRepository


class BTreeInMemoryReadOnlyRepository(BTreeReadOnlyRepository):
    """
    """
    def __init__(self, page_size):
        """
        """
        super().__init__(page_size)
        self._pages = bytearray()

    def read(self, offset, size):
        """
        Reads specific number of bytes at the offset.
        """
        assert offset + size <= len(self._pages)
        result = bytearray()
        pages_to_read = size // self._page_size
        bytes_to_read = size % self._page_size
        pages_offset = offset
        for _ in range(pages_to_read):
            result.extend(self._pages[pages_offset:pages_offset + self._page_size])
            pages_offset += self._page_size
        result.extend(self._pages[pages_offset:pages_offset + bytes_to_read])
        return result
