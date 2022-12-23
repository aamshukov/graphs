"""
"""
from abc import abstractmethod
from objct import Objct


"""
"""
class Visitable(Objct):
    """
    """
    @abstractmethod
    def accept(self, visitor, *args, **kwargs):
        visitor.visit(self, *args, **kwargs)
