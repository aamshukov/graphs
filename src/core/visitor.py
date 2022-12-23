"""
"""
from abc import abstractmethod
from objct import Objct


"""
"""
class Visitor(Objct):
    """
    """
    @abstractmethod
    def visit(self, visitable, *args, **kwargs):
        pass
