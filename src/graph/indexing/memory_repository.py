# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" In-Memory Repository """
from graph.indexing.readonly_memory_repository import InMemoryReadOnlyRepository


class InMemoryRepository(InMemoryReadOnlyRepository):
    """
    """
    def __init__(self, page_size):
        """
        """
        super().__init__(page_size)

    def write(self, offset, buffer):
        """
        Writes specific buffer at the offset.
        """
        if offset + len(buffer) > len(self._pages):
            page = [0] * self._page_size
            while offset + len(buffer) > len(self._pages):
                self._pages.extend(page)
        pages_to_write = len(buffer) // self._page_size
        pages_offset = offset
        buffer_offset = 0
        for _ in range(pages_to_write):
            self._pages[pages_offset:pages_offset + self._page_size] =\
                buffer[buffer_offset:buffer_offset + self._page_size]
            pages_offset += self._page_size
            buffer_offset += self._page_size
        bytes_to_write = len(buffer) % self._page_size
        self._pages[pages_offset:pages_offset + bytes_to_write] = buffer[buffer_offset:]
