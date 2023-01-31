# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" B* Tree ReadOnly Repository """
from abc import abstractmethod
from graph.core.base import Base


class BTreeReadOnlyRepository(Base):
    """
    """
    def __init__(self, page_size):
        """
        """
        assert page_size > 0, "Page size must be greater than zero."
        super().__init__()
        self._page_size = page_size

    @property
    def page_size(self):
        """
        """
        return self._page_size

    @abstractmethod
    def read(self, offset, size):
        """
        Reads specific number of bytes at the offset.
        """
        raise NotImplementedError("BTreeReadOnlyRepository:read")
