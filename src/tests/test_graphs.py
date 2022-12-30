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
from graph.adt.disjoint_set import DisjointSet
from graph.core.value import Value
from graph.core.entity import Entity
from graph.adt.vertex import Vertex
from graph.adt.edge import Edge
from graph.adt.graph import Graph
from graph.algorithms.graph_algorithms import GraphAlgorithms


class Person(Entity):
    def __init__(self, name, age, address, manager=None):
        super().__init__(1, '2.1')
        self._name = name
        self._age = age
        self._manager = manager
        self._address = address

    def __hash__(self):
        result = super().__hash__()
        result ^= hash(self._name)
        result ^= hash(self._age)
        result ^= hash(self._manager)
        result ^= hash(self._address)
        return result

    def __eq__(self, other):
        result = (super().__eq__(other) and
                  Text.equal(self._name, other.name) and
                  self._age == other.age and
                  self._manager == other.manager and
                  self._address == other.address)
        return result

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

    def __hash__(self):
        result = super().__hash__()
        result ^= hash(self._street)
        result ^= hash(self._city)
        return result

    def __eq__(self, other):
        result = (super().__eq__(other) and
                  Text.equal(self._street, other.street) and
                  Text.equal(self._city, other.city))
        return result

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
            result = nx.MultiDiGraph()
        else:
            result = nx.MultiGraph()
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

    @staticmethod
    def generate_random_graph(n=3, digraph=False):
        import numpy as np
        import networkx as nx
        p = np.random.rand(n, n)  # your "matrix of probabilities"
        adjacency = np.random.rand(*p.shape) <= p  # adjacency[ii, jj] is True with probability P[ii, jj]
        nx_graph = nx.from_numpy_matrix(adjacency, nx.DiGraph if digraph else nx.Graph)
        result = Graph(digraph)
        vertices = dict()
        for vertex in nx_graph.nodes:
            v = Vertex(vertex, str(vertex), vertex)
            vertices[vertex] = v
            result.add_vertex(v)
        for edge in nx_graph.edges:
            u, v = edge
            result.add_edge(vertices[u], vertices[v])
        return result

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

    def test_graph_0_success(self):
        graph = Graph(digraph=False)
        assert len(graph.vertices) == 0
        assert len(graph.edges) == 0

    def test_graph_1_success(self):
        graph = Graph(digraph=False)
        v1 = Vertex(1, '1', 1)
        graph.add_vertex(v1)
        # Test.show_graph(graph)
        assert len(graph.vertices) == 1
        assert len(graph.edges) == 0
        predecessors = GraphAlgorithms.collect_predecessors(v1, graph)
        successors = GraphAlgorithms.collect_successors(v1, graph)
        assert len(predecessors) == 0
        assert len(successors) == 0
        graph.remove_vertex(v1)
        assert len(graph.vertices) == 0
        assert len(graph.edges) == 0

    def test_graph_2_no_edges_success(self):
        graph = Graph(digraph=False)
        v1 = Vertex(1, '1', 1)
        v2 = Vertex(2, '2', 2)
        graph.add_vertex(v1)
        graph.add_vertex(v2)
        assert len(graph.vertices) == 2
        assert len(graph.edges) == 0
        predecessors = GraphAlgorithms.collect_predecessors(v1, graph)
        successors = GraphAlgorithms.collect_successors(v1, graph)
        assert len(predecessors) == 0
        assert len(successors) == 0
        predecessors = GraphAlgorithms.collect_predecessors(v2, graph)
        successors = GraphAlgorithms.collect_successors(v2, graph)
        assert len(predecessors) == 0
        assert len(successors) == 0
        graph.remove_vertex(v1)
        assert len(graph.vertices) == 1
        assert len(graph.edges) == 0
        predecessors = GraphAlgorithms.collect_predecessors(v2, graph)
        successors = GraphAlgorithms.collect_successors(v2, graph)
        assert len(predecessors) == 0
        assert len(successors) == 0
        graph.remove_vertex(v2)
        assert len(graph.vertices) == 0
        assert len(graph.edges) == 0

    def test_graph_2_success(self):
        graph = Graph(digraph=False)
        v1 = Vertex(1, '1', 1)
        v2 = Vertex(2, '2', 2)
        graph.add_vertex(v1)
        graph.add_vertex(v2)
        graph.add_edge(v1, v2, 'v1-v2')
        assert len(graph.vertices) == 2
        assert len(graph.edges) == 2
        # Test.show_graph(graph)
        predecessors = GraphAlgorithms.collect_predecessors(v1, graph)
        successors = GraphAlgorithms.collect_successors(v1, graph)
        assert len(predecessors) == 1
        assert len(successors) == 1
        predecessors = GraphAlgorithms.collect_predecessors(v2, graph)
        successors = GraphAlgorithms.collect_successors(v2, graph)
        assert len(predecessors) == 1
        assert len(successors) == 1
        graph.remove_vertex(v1)
        assert len(graph.vertices) == 1
        assert len(graph.edges) == 0
        predecessors = GraphAlgorithms.collect_predecessors(v2, graph)
        successors = GraphAlgorithms.collect_successors(v2, graph)
        assert len(predecessors) == 0
        assert len(successors) == 0
        graph.remove_vertex(v2)
        assert len(graph.vertices) == 0
        assert len(graph.edges) == 0

    def test_graph_3_success(self):
        graph = Graph(digraph=False)
        v1 = Vertex(1, '1', 1)
        v2 = Vertex(2, '2', 2)
        v3 = Vertex(3, '3', 3)
        graph.add_vertex(v1)
        graph.add_vertex(v2)
        graph.add_vertex(v3)
        graph.add_edge(v1, v2, 'v1-v2')
        graph.add_edge(v2, v3, 'v2-v3')
        graph.add_edge(v3, v1, 'v3-v1')
        # Test.show_graph(graph)
        assert len(graph.vertices) == 3
        assert len(graph.edges) == 6
        predecessors = GraphAlgorithms.collect_predecessors(v1, graph)
        successors = GraphAlgorithms.collect_successors(v1, graph)
        assert len(predecessors) == 2
        assert len(successors) == 2
        predecessors = GraphAlgorithms.collect_predecessors(v2, graph)
        successors = GraphAlgorithms.collect_successors(v2, graph)
        assert len(predecessors) == 2
        assert len(successors) == 2
        predecessors = GraphAlgorithms.collect_predecessors(v3, graph)
        successors = GraphAlgorithms.collect_successors(v3, graph)
        assert len(predecessors) == 2
        assert len(successors) == 2
        graph.remove_vertex(v1)
        # Test.show_graph(graph)
        assert len(graph.vertices) == 2
        assert len(graph.edges) == 2
        predecessors = GraphAlgorithms.collect_predecessors(v2, graph)
        successors = GraphAlgorithms.collect_successors(v2, graph)
        assert len(predecessors) == 1
        assert len(successors) == 1
        graph.remove_vertex(v2)
        assert len(graph.vertices) == 1
        assert len(graph.edges) == 0
        predecessors = GraphAlgorithms.collect_predecessors(v3, graph)
        successors = GraphAlgorithms.collect_successors(v3, graph)
        assert len(predecessors) == 0
        assert len(successors) == 0
        graph.remove_vertex(v3)
        assert len(graph.vertices) == 0
        assert len(graph.edges) == 0

    def test_graph_3_complex_success(self):
        graph = Graph(digraph=False)
        v1 = Vertex(1, '1', 1)
        v2 = Vertex(2, '2', 2)
        v3 = Vertex(3, '3', 3)
        graph.add_vertex(v1)
        graph.add_vertex(v2)
        graph.add_vertex(v3)
        graph.add_edge(v1, v1, 'v1-v1-0')
        graph.add_edge(v1, v1, 'v1-v1-1')
        graph.add_edge(v1, v2, 'v1-v2-2')
        graph.add_edge(v1, v2, 'v1-v2-3')
        graph.add_edge(v1, v3, 'v1-v3-6')
        graph.add_edge(v2, v2, 'v2-v2-4')
        graph.add_edge(v2, v2, 'v2-v2-5')
        graph.add_edge(v2, v1, 'v2-v1-2')
        graph.add_edge(v2, v1, 'v2-v1-3')
        graph.add_edge(v2, v3, 'v2-v3-7')
        graph.add_edge(v3, v3, 'v3-v3-8')
        # Test.show_graph(graph)
        assert len(graph.vertices) == 3
        assert len(graph.edges) == 22
        predecessors = GraphAlgorithms.collect_predecessors(v1, graph)
        successors = GraphAlgorithms.collect_successors(v1, graph)
        assert len(predecessors) == 9
        assert len(successors) == 9
        predecessors = GraphAlgorithms.collect_predecessors(v2, graph)
        successors = GraphAlgorithms.collect_successors(v2, graph)
        assert len(predecessors) == 9
        assert len(successors) == 9
        predecessors = GraphAlgorithms.collect_predecessors(v3, graph)
        successors = GraphAlgorithms.collect_successors(v3, graph)
        assert len(predecessors) == 4
        assert len(successors) == 4
        graph.remove_vertex(v3)
        # Test.show_graph(graph)
        assert len(graph.vertices) == 2
        assert len(graph.edges) == 16
        predecessors = GraphAlgorithms.collect_predecessors(v1, graph)
        successors = GraphAlgorithms.collect_successors(v1, graph)
        assert len(predecessors) == 8
        assert len(successors) == 8
        graph.remove_vertex(v2)
        # Test.show_graph(graph)
        assert len(graph.vertices) == 1
        assert len(graph.edges) == 4
        predecessors = GraphAlgorithms.collect_predecessors(v1, graph)
        successors = GraphAlgorithms.collect_successors(v1, graph)
        assert len(predecessors) == 4
        assert len(successors) == 4
        graph.remove_vertex(v1)
        assert len(graph.vertices) == 0
        assert len(graph.edges) == 0

    def test_graph_5_success(self):
        graph = Graph(digraph=False)
        v1 = Vertex(1, '1', 1)
        v2 = Vertex(2, '2', 2)
        v3 = Vertex(3, '3', 3)
        v4 = Vertex(4, '4', 4)
        v5 = Vertex(5, '5', 5)
        v6 = Vertex(6, '6', 6)
        graph.add_vertex(v1)
        graph.add_vertex(v2)
        graph.add_vertex(v3)
        graph.add_vertex(v4)
        graph.add_vertex(v5)
        graph.add_vertex(v6)
        graph.add_edge(v1, v2, 'v1-v2')
        graph.add_edge(v1, v4, 'v1-v4')
        graph.add_edge(v1, v5, 'v1-v5')
        graph.add_edge(v2, v3, 'v2-v3')
        graph.add_edge(v2, v4, 'v2-v4')
        graph.add_edge(v3, v3, 'v3-v3')
        graph.add_edge(v4, v2, 'v4-v2')
        graph.add_edge(v4, v3, 'v4-v3')
        graph.add_edge(v6, v2, 'v6-v2')
        graph.add_edge(v6, v3, 'v6-v3')
        # Test.show_graph(graph)
        assert len(graph.vertices) == 6
        assert len(graph.edges) == 20
        predecessors = GraphAlgorithms.collect_predecessors(v1, graph)
        successors = GraphAlgorithms.collect_successors(v1, graph)
        assert len(predecessors) == 3
        assert len(successors) == 3
        predecessors = GraphAlgorithms.collect_predecessors(v2, graph)
        successors = GraphAlgorithms.collect_successors(v2, graph)
        assert len(predecessors) == 5
        assert len(successors) == 5
        predecessors = GraphAlgorithms.collect_predecessors(v3, graph)
        successors = GraphAlgorithms.collect_successors(v3, graph)
        assert len(predecessors) == 5
        assert len(successors) == 5
        predecessors = GraphAlgorithms.collect_predecessors(v4, graph)
        successors = GraphAlgorithms.collect_successors(v4, graph)
        assert len(predecessors) == 4
        assert len(successors) == 4
        predecessors = GraphAlgorithms.collect_predecessors(v5, graph)
        successors = GraphAlgorithms.collect_successors(v5, graph)
        assert len(predecessors) == 1
        assert len(successors) == 1
        predecessors = GraphAlgorithms.collect_predecessors(v6, graph)
        successors = GraphAlgorithms.collect_successors(v6, graph)
        assert len(predecessors) == 2
        assert len(successors) == 2
        graph.remove_vertex(v1)
        # Test.show_graph(graph)
        assert len(graph.vertices) == 5
        assert len(graph.edges) == 14
        predecessors = GraphAlgorithms.collect_predecessors(v2, graph)
        successors = GraphAlgorithms.collect_successors(v2, graph)
        assert len(predecessors) == 4
        assert len(successors) == 4
        predecessors = GraphAlgorithms.collect_predecessors(v3, graph)
        successors = GraphAlgorithms.collect_successors(v3, graph)
        assert len(predecessors) == 5
        assert len(successors) == 5
        predecessors = GraphAlgorithms.collect_predecessors(v4, graph)
        successors = GraphAlgorithms.collect_successors(v4, graph)
        assert len(predecessors) == 3
        assert len(successors) == 3
        predecessors = GraphAlgorithms.collect_predecessors(v5, graph)
        successors = GraphAlgorithms.collect_successors(v5, graph)
        assert len(predecessors) == 0
        assert len(successors) == 0
        predecessors = GraphAlgorithms.collect_predecessors(v6, graph)
        successors = GraphAlgorithms.collect_successors(v6, graph)
        assert len(predecessors) == 2
        assert len(successors) == 2
        graph.remove_vertex(v2)
        # Test.show_graph(graph)
        assert len(graph.vertices) == 4
        assert len(graph.edges) == 6
        predecessors = GraphAlgorithms.collect_predecessors(v3, graph)
        successors = GraphAlgorithms.collect_successors(v3, graph)
        assert len(predecessors) == 4
        assert len(successors) == 4
        predecessors = GraphAlgorithms.collect_predecessors(v4, graph)
        successors = GraphAlgorithms.collect_successors(v4, graph)
        assert len(predecessors) == 1
        assert len(successors) == 1
        predecessors = GraphAlgorithms.collect_predecessors(v5, graph)
        successors = GraphAlgorithms.collect_successors(v5, graph)
        assert len(predecessors) == 0
        assert len(successors) == 0
        predecessors = GraphAlgorithms.collect_predecessors(v6, graph)
        successors = GraphAlgorithms.collect_successors(v6, graph)
        assert len(predecessors) == 1
        assert len(successors) == 1
        graph.remove_vertex(v3)
        # Test.show_graph(graph)
        assert len(graph.vertices) == 3
        assert len(graph.edges) == 0
        predecessors = GraphAlgorithms.collect_predecessors(v4, graph)
        successors = GraphAlgorithms.collect_successors(v4, graph)
        assert len(predecessors) == 0
        assert len(successors) == 0
        predecessors = GraphAlgorithms.collect_predecessors(v5, graph)
        successors = GraphAlgorithms.collect_successors(v5, graph)
        assert len(predecessors) == 0
        assert len(successors) == 0
        predecessors = GraphAlgorithms.collect_predecessors(v6, graph)
        successors = GraphAlgorithms.collect_successors(v6, graph)
        assert len(predecessors) == 0
        assert len(successors) == 0
        graph.remove_vertex(v4)
        # Test.show_graph(graph)
        assert len(graph.vertices) == 2
        assert len(graph.edges) == 0
        predecessors = GraphAlgorithms.collect_predecessors(v5, graph)
        successors = GraphAlgorithms.collect_successors(v5, graph)
        assert len(predecessors) == 0
        assert len(successors) == 0
        predecessors = GraphAlgorithms.collect_predecessors(v6, graph)
        successors = GraphAlgorithms.collect_successors(v6, graph)
        assert len(predecessors) == 0
        assert len(successors) == 0
        graph.remove_vertex(v5)
        # Test.show_graph(graph)
        assert len(graph.vertices) == 1
        assert len(graph.edges) == 0
        predecessors = GraphAlgorithms.collect_predecessors(v6, graph)
        successors = GraphAlgorithms.collect_successors(v6, graph)
        assert len(predecessors) == 0
        assert len(successors) == 0
        graph.remove_vertex(v6)
        # Test.show_graph(graph)
        assert len(graph.vertices) == 0
        assert len(graph.edges) == 0

    def test_graph_success(self):
        n = 100
        for _ in range(1):
            graph = Test.generate_random_graph(n)
            vertices = list(graph.vertices.values())
            while vertices:
                vertex = random.choice(vertices)
                graph.remove_vertex(vertex)
                vertices.remove(vertex)
            assert len(graph.vertices) == 0
            assert len(graph.edges) == 0

    def test_digraph_1_success(self):
        pass

    def test_digraph_2_success(self):
        pass

    def test_digraph_3_success(self):
        pass

    def test_digraph_5_success(self):
        pass

    def test_digraph_success(self):
        pass


if __name__ == '__main__':
    """
    """
    unittest.main()
