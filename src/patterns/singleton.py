#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Singleton design pattern """


def singleton(класс):
    """
    Singleton decorator
    """
    class Decorator(класс):
        """
        Decorator
        """

        def __init__(self, *args, **kwargs):
            """
            """
            if hasattr(класс, '__init__'):
                класс.__init__(self, *args, **kwargs)

        def __repr__(self):
            """
            """
            return f'{класс.__name__}-singleton'

        __str__ = __repr__

    Decorator.__name__ = класс.__name__

    class Instance:
        """
        Instance
        """

        def __init__(self):
            """
            """
            self.instance = None

        def __repr__(self):
            """
            """
            return класс.__name__

        __str__ = __repr__

        def __call__(self, *args, **kwargs):
            """
            """
            if self.instance is None:
                self.instance = Decorator(*args, **kwargs)
            return self.instance

    return Instance()
