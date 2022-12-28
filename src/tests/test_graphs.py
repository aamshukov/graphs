#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import os
import sys
import random
import unittest

from graph.core.flags import Flags
from graph.core.logger import Logger
from graph.core.text import Text
from graph.core.value import Value
from graph.core.entity import Entity
from graph.adt.vertex import Vertex
from graph.adt.edge import Edge
from graph.adt.graph import Graph
from graph.adt.disjoint_set import DisjointSet


class Person(Entity):
    def __init__(self, name, age, address, manager=None):
        super().__init__(1, '2.1')
        self._name = name
        self._age = age
        self._manager = manager
        self._address = address

    @property
    def name(self):
        return self._name

    @property
    def age(self):
        return self._age

    @property
    def manager(self):
        return self._manager

    @property
    def address(self):
        return self._address

    def validate(self):
        pass


class Address(Value):
    __slots__ = '_street', '_city'

    def __init__(self, street, city):
        super().__init__('2.1')
        self._street = street
        self._city = city

    @property
    def street(self):
        return self._street

    @property
    def city(self):
        return self._city

    def validate(self):
        pass


class Test(unittest.TestCase):
    @staticmethod
    def build_networkx_graph(graph):
        """
        """
        import networkx as nx
        if graph.digraph:
            result = nx.DiGraph()
        else:
            result = nx.Graph()
        for vertex in graph.vertices.values():
            result.add_node(vertex.label)
        for edge in graph.edges.values():
            result.add_edge(edge.endpoints[0].label, edge.endpoints[1].label)
        return result

    @staticmethod
    def show_graph(graph):
        import networkx as nx
        import matplotlib
        import matplotlib.pyplot as plt
        plt.style.use('ggplot')
        matplotlib.use('tkagg')
        nx_graph = Test.build_networkx_graph(graph)
        nx.draw_networkx(nx_graph)
        plt.show()

    def test_logger_success(self):
        path = r'd:\tmp'
        logger = Logger(path=path)
        logger.debug('kuku')
        assert os.path.exists(os.path.join(path, f'{Logger.LOGGER_NAME}.log'))

    def test_equality_success(self):
        address = Address('Marine Drive', 'Oakville')
        address.validate()
        manager = Person('Arthur', 50, address)
        manager.validate()
        person1 = Person('Eric', 28, address, manager)
        person1.validate()
        person2 = Person('Jon', 38, address, manager)
        person2.validate()
        person3 = Person('Eric', 28, address, manager)
        person3.validate()
        assert manager == manager
        assert person1 != manager
        assert person1 == person1
        assert person1 != person2
        assert person1 == person3

    def test_strings_equality_success(self):
        assert Text.equal('', '')
        assert Text.equal('Rit\u0113', 'Rite\u0304')
        assert not Text.equal('', ' ')
        assert Text.equal('(ノಠ益ಠ)ノ彡 ɹoʇıpƎ ʇxǝ⊥', '(ノಠ益ಠ)ノ彡 ɹoʇıpƎ ʇxǝ⊥')
        assert Text.equal('သည် ဇော်ဂျီ နှင့် မြန်မာ ယူနီကုတ် တို့ကို အပြန်အလှန် ပြောင်းပေးနိုင်သည့်အပြင် အင်တာနက်မရှိချိန်တွင်လည်း '
                          'offline အသုံးပြုနိုင်တဲ့ converter တစ်',
                          'သည် ဇော်ဂျီ နှင့် မြန်မာ ယူနီကုတ် တို့ကို အပြန်အလှန် ပြောင်းပေးနိုင်သည့်အပြင် အင်တာနက်မရှိချိန်တွင်လည်း '
                          'offline အသုံးပြုနိုင်တဲ့ converter တစ်')
        assert Text.equal('Я с детства хотел завести собаку', 'Я с детства хотел завести собаку')
        assert not Text.equal('Я c детства хотел завести собаку', 'Я с детства хотел завести собаку')
        assert Text.equal('english text', 'english text')
        assert Text.equal('山乇ㄥ匚ㄖ爪乇　ㄒㄖ　ㄒ卄乇　爪ㄖ丂ㄒ　匚ㄖ爪卩ㄥ乇ㄒ乇　ﾌ卂卩卂几乇丂乇',
                          '山乇ㄥ匚ㄖ爪乇　ㄒㄖ　ㄒ卄乇　爪ㄖ丂ㄒ　匚ㄖ爪卩ㄥ乇ㄒ乇　ﾌ卂卩卂几乇丂乇')
        assert Text.equal('enGlisH texT', 'EngLish TeXt', case_insensitive=True)
        assert Text.equal('Я с дЕТства хоТЕЛ зАВестИ Собаку', 'я с деТСтвА ХотЕЛ ЗАВЕСТИ СОБАКУ', case_insensitive=True)

    def test_modify_flags_success(self):
        flags = Flags.DIRTY | Flags.PROCESSED | Flags.VISITED | Flags.LEAF | Flags.INVALID
        assert flags & Flags.DIRTY == Flags.DIRTY
        assert flags & Flags.PROCESSED == Flags.PROCESSED
        assert flags & Flags.VISITED == Flags.VISITED
        assert flags & Flags.LEAF == Flags.LEAF
        assert flags & Flags.INVALID == Flags.INVALID
        flags = Flags.modify_flags(flags,
                                   Flags.GENUINE | Flags.SYNTHETIC, Flags.PROCESSED | Flags.VISITED | Flags.INVALID)
        assert flags & Flags.DIRTY == Flags.DIRTY
        assert flags & Flags.GENUINE == Flags.GENUINE
        assert flags & Flags.SYNTHETIC == Flags.SYNTHETIC

    def test_disjoinset_success(self):  # union find
        elements = list('ABCDEFGHIJ')
        djs = DisjointSet(elements)
        djs.union('A', 'B')
        djs.union('C', 'D')
        djs.union('E', 'F')
        djs.union('G', 'H')
        djs.union('I', 'J')
        djs.union('J', 'G')
        djs.union('H', 'F')
        djs.union('A', 'C')
        djs.union('D', 'E')
        djs.union('G', 'B')
        djs.union('I', 'J')
        assert djs.count == 1

    def test_disjoint_set_ints_success(self):  # union find
        n = 10000
        elements = [random.randint(0, n) for _ in range(n)]
        djs = DisjointSet(elements)
        for k in range(0, n, 2):
            djs.union(elements[k + 0], elements[k + 1])
            assert djs.find(elements[k + 0]) == djs.find(elements[k + 1])
        for k in range(n):
            djs.find(elements[k])

    def test_disjoint_set_ints_sedgewick_success(self):  # union find
        elements = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        djs = DisjointSet(elements)
        djs.union(4, 3)
        djs.union(3, 8)
        djs.union(6, 5)
        djs.union(9, 4)
        djs.union(2, 1)
        djs.union(5, 0)
        djs.union(7, 2)
        djs.union(6, 1)
        assert djs.find(4) == djs.find(3)
        assert djs.find(3) == djs.find(8)
        assert djs.find(6) == djs.find(5)
        assert djs.find(9) == djs.find(4)
        assert djs.find(2) == djs.find(1)
        assert djs.find(5) == djs.find(0)
        assert djs.find(7) == djs.find(2)
        assert djs.find(6) == djs.find(1)
        assert djs.count == 2

    def test_disjoint_set_ints_sedgewick_tiny_success(self):  # union find
        elements = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        djs = DisjointSet(elements)
        with open(os.path.abspath(r'data/tiny_ds.txt'), 'r') as stream:
            while line := stream.readline().rstrip():
                el1, el2 = line.split()
                djs.union(int(el1), int(el2))
        assert djs.count == 2

    def test_disjoint_set_ints_sedgewick_medium_success(self):  # union find
        elements = [k for k in range(625)]
        djs = DisjointSet(elements)
        with open(os.path.abspath(r'data/medium_ds.txt'), 'r') as stream:
            while line := stream.readline().rstrip():
                el1, el2 = line.split()
                djs.union(int(el1), int(el2))
        assert djs.count == 3

    def test_disjoint_set_ints_sedgewick_large_success(self):  # union find
        elements = [k for k in range(1000000)]
        djs = DisjointSet(elements)
        with open(os.path.abspath(r'data/large_ds.txt'), 'r') as stream:
            while line := stream.readline().rstrip():
                el1, el2 = line.split()
                djs.union(int(el1), int(el2))
        assert djs.count == 6


if __name__ == '__main__':
    """
    """
    unittest.main()
