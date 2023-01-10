#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import os
import random
import unittest
from collections import defaultdict
from datetime import datetime
import networkx as nx
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from graph.core.flags import Flags
from graph.core.colors import Colors
from graph.core.logger import Logger
from graph.core.text import Text
from graph.core.domainhelper import DomainHelper
from graph.core.algorithms import Algorithms
from graph.adt.disjoint_set import DisjointSet
from graph.core.value import Value
from graph.core.entity import Entity
from graph.adt.vertex import Vertex
from graph.adt.graph import Graph
from graph.adt.tree import Tree
from graph.algorithms.graph_algorithms import GraphAlgorithms
from graph.algorithms.graph_visitor import GraphVisitor


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
        plt.style.use('ggplot')
        matplotlib.use('tkagg')
        nx_graph = Test.build_networkx_graph(graph)
        nx.draw_networkx(nx_graph)
        plt.show()

    @staticmethod
    def build_networkx_tree(tree):
        """
        """
        result = nx.MultiDiGraph()
        stack = list()
        stack.append(tree)  # push
        while stack:
            node = stack.pop()
            # result.add_node(node.label)
            for kid in node.kids:
                result.add_edge(node.label, kid.label)
                stack.append(kid)  # push
        return result

    @staticmethod
    def show_tree(tree):
        plt.style.use('ggplot')
        matplotlib.use('tkagg')
        nx_tree = Test.build_networkx_tree(tree)
        nx.draw_networkx(nx_tree)
        plt.show()

    @staticmethod
    def generate_random_graph(n=3, digraph=False):
        p = np.random.rand(n, n)  # your "matrix of probabilities"
        adjacency = np.random.rand(*p.shape) <= p  # adjacency[ii, jj] is True with probability P[ii, jj]
        nx_graph = nx.from_numpy_matrix(adjacency, nx.DiGraph if digraph else nx.Graph)
        result = Graph(digraph=digraph)
        vertices = dict()
        for vertex in nx_graph.nodes:
            v = Vertex(vertex, str(vertex), vertex)
            vertices[vertex] = v
            result.add_vertex(v)
        for edge in nx_graph.edges:
            u, v = edge
            result.add_edge(vertices[u], vertices[v])
        return result

    @staticmethod
    def generate_random_tree(n=3):
        nx_tree = nx.random_tree(n, seed=0, create_using=nx.DiGraph)
        nodes = dict()
        for nx_node in nx_tree.nodes:
            node = Tree(nx_node, str(nx_node), nx_node)
            nodes[nx_node] = node
        for adj in nx_tree.adj.items():
            node = nodes[adj[0]]
            for kid in list(adj[1]):
                node.add_kid(nodes[kid])
        return nodes

    @staticmethod
    def generate_random_array_queries(n=3):
        p = np.random.rand(n, n)  # your "matrix of probabilities"
        adjacency = np.random.rand(*p.shape) <= p  # adjacency[ii, jj] is True with probability P[ii, jj]
        nx_graph = nx.from_numpy_matrix(adjacency, nx.Graph)
        array = list(nx_graph.nodes)
        queries = list(nx_graph.edges)
        random.shuffle(array)
        return array, queries

    @staticmethod
    def generate_random_queries(n=3):
        p = np.random.rand(n, n)
        adjacency = np.random.rand(*p.shape) <= p
        result = nx.from_numpy_matrix(adjacency, nx.MultiGraph)
        return list(result)

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

    def test_disjoint_set_success(self):  # union find
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

    def test_graph_degree_success(self):
        graph = Graph(digraph=False)
        v1 = Vertex(1, '1', 1)
        graph.add_vertex(v1)
        graph.add_edge(v1, v1, 'v1-v1-0')
        # Test.show_graph(graph)
        assert graph.get_vertex_degree(v1) == 2

    def test_digraph_degree_success(self):
        graph = Graph(digraph=True)
        v1 = Vertex(1, '1', 1)
        graph.add_vertex(v1)
        graph.add_edge(v1, v1, 'v1-v1-0')
        # Test.show_graph(graph)
        assert graph.get_vertex_degree(v1) == 2

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

    def test_graph_success_random(self):
        now = datetime.now()
        print(f"Start: {now}")
        n = 1000
        for k in range(1):
            now = datetime.now()
            print(f"Iteration: {k}  {now}")
            graph = Test.generate_random_graph(n)
            vertices = list(graph.vertices.values())
            print(f"Vertices collected ... {len(graph.vertices)}")
            print(f"Edges collected ... {len(graph.edges)}")
            while vertices:
                vertex = random.choice(vertices)
                graph.remove_vertex(vertex)
                vertices.remove(vertex)
            assert len(graph.vertices) == 0
            assert len(graph.edges) == 0
        now = datetime.now()
        print(f"End: {now}")

    def test_digraph_1_success(self):
        graph = Graph(digraph=True)
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

    def test_digraph_2_no_edges_success(self):
        graph = Graph(digraph=True)
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

    def test_digraph_2_success(self):
        graph = Graph(digraph=True)
        v1 = Vertex(1, '1', 1)
        v2 = Vertex(2, '2', 2)
        graph.add_vertex(v1)
        graph.add_vertex(v2)
        graph.add_edge(v1, v2, 'v1-v2')
        assert len(graph.vertices) == 2
        assert len(graph.edges) == 1
        # Test.show_graph(graph)
        predecessors = GraphAlgorithms.collect_predecessors(v1, graph)
        successors = GraphAlgorithms.collect_successors(v1, graph)
        assert len(predecessors) == 0
        assert len(successors) == 1
        predecessors = GraphAlgorithms.collect_predecessors(v2, graph)
        successors = GraphAlgorithms.collect_successors(v2, graph)
        assert len(predecessors) == 1
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

    def test_digraph_3_success(self):
        graph = Graph(digraph=True)
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
        assert len(graph.edges) == 3
        predecessors = GraphAlgorithms.collect_predecessors(v1, graph)
        successors = GraphAlgorithms.collect_successors(v1, graph)
        assert len(predecessors) == 1
        assert len(successors) == 1
        predecessors = GraphAlgorithms.collect_predecessors(v2, graph)
        successors = GraphAlgorithms.collect_successors(v2, graph)
        assert len(predecessors) == 1
        assert len(successors) == 1
        predecessors = GraphAlgorithms.collect_predecessors(v3, graph)
        successors = GraphAlgorithms.collect_successors(v3, graph)
        assert len(predecessors) == 1
        assert len(successors) == 1
        graph.remove_vertex(v1)
        # Test.show_graph(graph)
        assert len(graph.vertices) == 2
        assert len(graph.edges) == 1
        predecessors = GraphAlgorithms.collect_predecessors(v2, graph)
        successors = GraphAlgorithms.collect_successors(v2, graph)
        assert len(predecessors) == 0
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

    def test_digraph_3_complex_success(self):
        graph = Graph(digraph=True)
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
        assert len(graph.edges) == 11
        predecessors = GraphAlgorithms.collect_predecessors(v1, graph)
        successors = GraphAlgorithms.collect_successors(v1, graph)
        assert len(predecessors) == 4
        assert len(successors) == 5
        predecessors = GraphAlgorithms.collect_predecessors(v2, graph)
        successors = GraphAlgorithms.collect_successors(v2, graph)
        assert len(predecessors) == 4
        assert len(successors) == 5
        predecessors = GraphAlgorithms.collect_predecessors(v3, graph)
        successors = GraphAlgorithms.collect_successors(v3, graph)
        assert len(predecessors) == 3
        assert len(successors) == 1
        graph.remove_vertex(v3)
        # Test.show_graph(graph)
        assert len(graph.vertices) == 2
        assert len(graph.edges) == 8
        predecessors = GraphAlgorithms.collect_predecessors(v1, graph)
        successors = GraphAlgorithms.collect_successors(v1, graph)
        assert len(predecessors) == 4
        assert len(successors) == 4
        graph.remove_vertex(v2)
        # Test.show_graph(graph)
        assert len(graph.vertices) == 1
        assert len(graph.edges) == 2
        predecessors = GraphAlgorithms.collect_predecessors(v1, graph)
        successors = GraphAlgorithms.collect_successors(v1, graph)
        assert len(predecessors) == 2
        assert len(successors) == 2
        graph.remove_vertex(v1)
        assert len(graph.vertices) == 0
        assert len(graph.edges) == 0

    def test_digraph_5_success(self):
        graph = Graph(digraph=True)
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
        assert len(graph.edges) == 10
        predecessors = GraphAlgorithms.collect_predecessors(v1, graph)
        successors = GraphAlgorithms.collect_successors(v1, graph)
        assert len(predecessors) == 0
        assert len(successors) == 3
        predecessors = GraphAlgorithms.collect_predecessors(v2, graph)
        successors = GraphAlgorithms.collect_successors(v2, graph)
        assert len(predecessors) == 3
        assert len(successors) == 2
        predecessors = GraphAlgorithms.collect_predecessors(v3, graph)
        successors = GraphAlgorithms.collect_successors(v3, graph)
        assert len(predecessors) == 4
        assert len(successors) == 1
        predecessors = GraphAlgorithms.collect_predecessors(v4, graph)
        successors = GraphAlgorithms.collect_successors(v4, graph)
        assert len(predecessors) == 2
        assert len(successors) == 2
        predecessors = GraphAlgorithms.collect_predecessors(v5, graph)
        successors = GraphAlgorithms.collect_successors(v5, graph)
        assert len(predecessors) == 1
        assert len(successors) == 0
        predecessors = GraphAlgorithms.collect_predecessors(v6, graph)
        successors = GraphAlgorithms.collect_successors(v6, graph)
        assert len(predecessors) == 0
        assert len(successors) == 2
        graph.remove_vertex(v1)
        # Test.show_graph(graph)
        assert len(graph.vertices) == 5
        assert len(graph.edges) == 7
        predecessors = GraphAlgorithms.collect_predecessors(v2, graph)
        successors = GraphAlgorithms.collect_successors(v2, graph)
        assert len(predecessors) == 2
        assert len(successors) == 2
        predecessors = GraphAlgorithms.collect_predecessors(v3, graph)
        successors = GraphAlgorithms.collect_successors(v3, graph)
        assert len(predecessors) == 4
        assert len(successors) == 1
        predecessors = GraphAlgorithms.collect_predecessors(v4, graph)
        successors = GraphAlgorithms.collect_successors(v4, graph)
        assert len(predecessors) == 1
        assert len(successors) == 2
        predecessors = GraphAlgorithms.collect_predecessors(v5, graph)
        successors = GraphAlgorithms.collect_successors(v5, graph)
        assert len(predecessors) == 0
        assert len(successors) == 0
        predecessors = GraphAlgorithms.collect_predecessors(v6, graph)
        successors = GraphAlgorithms.collect_successors(v6, graph)
        assert len(predecessors) == 0
        assert len(successors) == 2
        graph.remove_vertex(v2)
        # Test.show_graph(graph)
        assert len(graph.vertices) == 4
        assert len(graph.edges) == 3
        predecessors = GraphAlgorithms.collect_predecessors(v3, graph)
        successors = GraphAlgorithms.collect_successors(v3, graph)
        assert len(predecessors) == 3
        assert len(successors) == 1
        predecessors = GraphAlgorithms.collect_predecessors(v4, graph)
        successors = GraphAlgorithms.collect_successors(v4, graph)
        assert len(predecessors) == 0
        assert len(successors) == 1
        predecessors = GraphAlgorithms.collect_predecessors(v5, graph)
        successors = GraphAlgorithms.collect_successors(v5, graph)
        assert len(predecessors) == 0
        assert len(successors) == 0
        predecessors = GraphAlgorithms.collect_predecessors(v6, graph)
        successors = GraphAlgorithms.collect_successors(v6, graph)
        assert len(predecessors) == 0
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

    def test_digraph_success(self):
        now = datetime.now()
        print(f"Start: {now}")
        n = 1000
        for k in range(1):
            now = datetime.now()
            print(f"Iteration: {k}  {now}")
            graph = Test.generate_random_graph(n, digraph=True)
            # Test.show_graph(graph)
            vertices = list(graph.vertices.values())
            print(f"Vertices collected ... {len(graph.vertices)}")
            print(f"Edges collected ... {len(graph.edges)}")
            while vertices:
                vertex = random.choice(vertices)
                graph.remove_vertex(vertex)
                vertices.remove(vertex)
            assert len(graph.vertices) == 0
            assert len(graph.edges) == 0
        now = datetime.now()
        print(f"End: {now}")

    class CollectNodesVisitor(GraphVisitor):

        def __init__(self, graph):
            """
            """
            super().__init__(graph)
            self._collected_vertices = list()

        @property
        def collected_vertices(self):
            return self._collected_vertices

        def visit(self, vertex, *args, **kwargs):
            """
            """
            self._collected_vertices.append(vertex)

    def test_graph_dfs_3_complex_visitor_success(self):
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
        visitor = Test.CollectNodesVisitor(graph)
        for vertex in graph.vertices.values():
            vertex.accept(visitor)
        assert visitor.collected_vertices == [v1, v2, v3]

    def test_graph_dfs_visitor_success(self):
        now = datetime.now()
        print(f"Start: {now}")
        n = 200  # watch recursion
        for k in range(10):
            now = datetime.now()
            print(f"Iteration: {k}  {now}")
            graph = Test.generate_random_graph(n, digraph=False)
            # Test.show_graph(graph)
            vertices = list(graph.vertices.values())
            print(f"Vertices collected ... {len(graph.vertices)}")
            print(f"Edges collected ... {len(graph.edges)}")
            visitor = Test.CollectNodesVisitor(graph)
            for vertex in graph.vertices.values():
                vertex.accept(visitor)
            assert len(visitor.collected_vertices) == len(vertices)
        now = datetime.now()
        print(f"End: {now}")

    def test_graph_dfs_3_complex_success(self):
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
        collected_vertices = list()
        for vertex in graph.vertices.values():
            for v in GraphAlgorithms.dfs(vertex):
                collected_vertices.append(v)
        assert collected_vertices == [v1, v2, v3]

    def test_graph_dfs_success(self):
        now = datetime.now()
        print(f"Start: {now}")
        n = 1000  # watch recursion
        for k in range(10):
            now = datetime.now()
            print(f"Iteration: {k}  {now}")
            graph = Test.generate_random_graph(n, digraph=False)
            # Test.show_graph(graph)
            vertices = list(graph.vertices.values())
            print(f"Vertices collected ... {len(graph.vertices)}")
            print(f"Edges collected ... {len(graph.edges)}")
            collected_vertices = list()
            for vertex in graph.vertices.values():
                for v in GraphAlgorithms.dfs(vertex):
                    collected_vertices.append(v)

            assert len(collected_vertices) == len(vertices)
        now = datetime.now()
        print(f"End: {now}")

    def test_digraph_dfs_3_complex_visitor_success(self):
        graph = Graph(digraph=True)
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
        visitor = Test.CollectNodesVisitor(graph)
        for vertex in graph.vertices.values():
            vertex.accept(visitor)
        assert visitor.collected_vertices == [v1, v2, v3]

    def test_digraph_dfs_visitor_success(self):
        now = datetime.now()
        print(f"Start: {now}")
        n = 200  # watch recursion
        for k in range(10):
            now = datetime.now()
            print(f"Iteration: {k}  {now}")
            graph = Test.generate_random_graph(n, digraph=True)
            # Test.show_graph(graph)
            vertices = list(graph.vertices.values())
            print(f"Vertices collected ... {len(graph.vertices)}")
            print(f"Edges collected ... {len(graph.edges)}")
            visitor = Test.CollectNodesVisitor(graph)
            for vertex in graph.vertices.values():
                vertex.accept(visitor)
            assert len(visitor.collected_vertices) == len(vertices)
        now = datetime.now()
        print(f"End: {now}")

    def test_digraph_dfs_3_complex_success(self):
        graph = Graph(digraph=True)
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
        collected_vertices = list()
        for vertex in graph.vertices.values():
            for v in GraphAlgorithms.dfs(vertex):
                collected_vertices.append(v)
        assert collected_vertices == [v1, v3, v2]

    def test_digraph_dfs_success(self):
        now = datetime.now()
        print(f"Start: {now}")
        n = 1000  # watch recursion
        for k in range(10):
            now = datetime.now()
            print(f"Iteration: {k}  {now}")
            graph = Test.generate_random_graph(n, digraph=True)
            # Test.show_graph(graph)
            vertices = list(graph.vertices.values())
            print(f"Vertices collected ... {len(graph.vertices)}")
            print(f"Edges collected ... {len(graph.edges)}")
            collected_vertices = list()
            for vertex in graph.vertices.values():
                for v in GraphAlgorithms.dfs(vertex):
                    collected_vertices.append(v)
            assert len(collected_vertices) == len(vertices)
        now = datetime.now()
        print(f"End: {now}")

    def test_graph_bfs_4_success(self):
        graph = Graph(digraph=False)
        v0 = Vertex(0, '0', 0)
        v1 = Vertex(1, '1', 1)
        v2 = Vertex(2, '2', 2)
        v3 = Vertex(3, '3', 3)
        graph.add_vertex(v0)
        graph.add_vertex(v1)
        graph.add_vertex(v2)
        graph.add_vertex(v3)
        graph.add_edge(v0, v1, 'v0-v1')
        graph.add_edge(v0, v2, 'v0-v2')
        graph.add_edge(v1, v2, 'v1-v2')
        graph.add_edge(v2, v0, 'v2-v0')
        graph.add_edge(v2, v3, 'v2-v3')
        graph.add_edge(v3, v3, 'v3-v3')
        # Test.show_graph(graph)
        collected_vertices = list()
        for vertex in graph.vertices.values():
            for v in GraphAlgorithms.bfs(v2):
                collected_vertices.append(v)
        assert collected_vertices == [v2, v0, v1, v3]

    def test_digraph_bfs_4_success(self):
        graph = Graph(digraph=True)
        v0 = Vertex(0, '0', 0)
        v1 = Vertex(1, '1', 1)
        v2 = Vertex(2, '2', 2)
        v3 = Vertex(3, '3', 3)
        graph.add_vertex(v0)
        graph.add_vertex(v1)
        graph.add_vertex(v2)
        graph.add_vertex(v3)
        graph.add_edge(v0, v1, 'v0-v1')
        graph.add_edge(v0, v2, 'v0-v2')
        graph.add_edge(v1, v2, 'v1-v2')
        graph.add_edge(v2, v0, 'v2-v0')
        graph.add_edge(v2, v3, 'v2-v3')
        graph.add_edge(v3, v3, 'v3-v3')
        # Test.show_graph(graph)
        collected_vertices = list()
        for vertex in graph.vertices.values():
            for v in GraphAlgorithms.bfs(v2):
                collected_vertices.append(v)
        assert collected_vertices == [v2, v0, v3, v1]  # 2, 0, 3, 1

    def test_graph_bfs_success(self):
        now = datetime.now()
        print(f"Start: {now}")
        n = 1000  # watch recursion
        for k in range(10):
            now = datetime.now()
            print(f"Iteration: {k}  {now}")
            graph = Test.generate_random_graph(n, digraph=False)
            # Test.show_graph(graph)
            vertices = list(graph.vertices.values())
            print(f"Vertices collected ... {len(graph.vertices)}")
            print(f"Edges collected ... {len(graph.edges)}")
            collected_vertices = list()
            for vertex in graph.vertices.values():
                for v in GraphAlgorithms.dfs(vertex):
                    collected_vertices.append(v)
            assert len(collected_vertices) == len(vertices)
        now = datetime.now()
        print(f"End: {now}")

    def test_digraph_bfs_success(self):
        now = datetime.now()
        print(f"Start: {now}")
        n = 1000  # watch recursion
        for k in range(10):
            now = datetime.now()
            print(f"Iteration: {k}  {now}")
            graph = Test.generate_random_graph(n, digraph=True)
            # Test.show_graph(graph)
            vertices = list(graph.vertices.values())
            print(f"Vertices collected ... {len(graph.vertices)}")
            print(f"Edges collected ... {len(graph.edges)}")
            collected_vertices = list()
            for vertex in graph.vertices.values():
                for v in GraphAlgorithms.dfs(vertex):
                    collected_vertices.append(v)
            assert len(collected_vertices) == len(vertices)
        now = datetime.now()
        print(f"End: {now}")

    def test_digraph_bfs_abcdef_success(self):
        graph = Graph(digraph=True)
        v_a = Vertex(0, 'A', 'A')
        v_b = Vertex(1, 'B', 'B')
        v_c = Vertex(2, 'C', 'C')
        v_d = Vertex(3, 'D', 'D')
        v_e = Vertex(4, 'E', 'E')
        v_f = Vertex(5, 'F', 'F')
        graph.add_vertex(v_a)
        graph.add_vertex(v_b)
        graph.add_vertex(v_c)
        graph.add_vertex(v_d)
        graph.add_vertex(v_e)
        graph.add_vertex(v_f)
        graph.add_edge(v_a, v_b, 'A->B')
        graph.add_edge(v_a, v_c, 'A->C')
        graph.add_edge(v_a, v_d, 'A->D')
        graph.add_edge(v_c, v_e, 'C->E')
        graph.add_edge(v_d, v_f, 'D->F')
        # Test.show_graph(graph)
        collected_vertices = list()
        for vertex in graph.vertices.values():
            for v in GraphAlgorithms.bfs(v_a):
                collected_vertices.append(v)
        assert collected_vertices == [v_a, v_b, v_c, v_d, v_e, v_f]

    def test_digraph_dfs_abcdef_success(self):
        graph = Graph(digraph=True)
        v_a = Vertex(0, 'A', 'A')
        v_b = Vertex(1, 'B', 'B')
        v_c = Vertex(2, 'C', 'C')
        v_d = Vertex(3, 'D', 'D')
        v_e = Vertex(4, 'E', 'E')
        v_f = Vertex(5, 'F', 'F')
        graph.add_vertex(v_a)
        graph.add_vertex(v_b)
        graph.add_vertex(v_c)
        graph.add_vertex(v_d)
        graph.add_vertex(v_e)
        graph.add_vertex(v_f)
        graph.add_edge(v_a, v_b, 'A->B')
        graph.add_edge(v_a, v_c, 'A->C')
        graph.add_edge(v_a, v_d, 'A->D')
        graph.add_edge(v_c, v_e, 'C->E')
        graph.add_edge(v_d, v_f, 'D->F')
        # Test.show_graph(graph)
        collected_vertices = list()
        for vertex in graph.vertices.values():
            for v in GraphAlgorithms.dfs(v_a):
                collected_vertices.append(v)
        assert collected_vertices == [v_a, v_d, v_f, v_c, v_e, v_b]

    def test_graph_dfs_connected_components_success(self):
        graph = Graph(digraph=False)
        v0 = Vertex(0, '0', 0)
        v1 = Vertex(1, '1', 1)
        v2 = Vertex(2, '2', 2)
        v3 = Vertex(3, '3', 3)
        v4 = Vertex(4, '4', 4)
        v5 = Vertex(5, '5', 5)
        v6 = Vertex(6, '6', 6)
        v7 = Vertex(7, '7', 7)
        v8 = Vertex(8, '8', 8)
        v9 = Vertex(9, '9', 9)
        v10 = Vertex(10, '10', 10)
        v11 = Vertex(11, '11', 11)
        v12 = Vertex(12, '12', 12)
        v13 = Vertex(13, '13', 13)
        v14 = Vertex(14, '14', 14)
        v15 = Vertex(15, '15', 15)
        v16 = Vertex(16, '16', 16)
        v17 = Vertex(17, '17', 17)
        graph.add_vertex(v0)
        graph.add_vertex(v1)
        graph.add_vertex(v2)
        graph.add_vertex(v3)
        graph.add_vertex(v4)
        graph.add_vertex(v5)
        graph.add_vertex(v6)
        graph.add_vertex(v7)
        graph.add_vertex(v8)
        graph.add_vertex(v9)
        graph.add_vertex(v10)
        graph.add_vertex(v11)
        graph.add_vertex(v12)
        graph.add_vertex(v13)
        graph.add_vertex(v14)
        graph.add_vertex(v15)
        graph.add_vertex(v16)
        graph.add_vertex(v17)
        graph.add_edge(v0, v4, '0->4')
        graph.add_edge(v0, v8, '0->4')
        graph.add_edge(v0, v13, '0->4')
        graph.add_edge(v0, v14, '0->4')
        graph.add_edge(v1, v5, '1->5')
        graph.add_edge(v2, v9, '2->9')
        graph.add_edge(v2, v15, '2->15')
        graph.add_edge(v3, v9, '3->9')
        graph.add_edge(v4, v0, '4->0')
        graph.add_edge(v4, v8, '4->8')
        graph.add_edge(v5, v1, '5->1')
        graph.add_edge(v5, v16, '5->16')
        graph.add_edge(v5, v17, '5->17')
        graph.add_edge(v6, v7, '6->7')
        graph.add_edge(v6, v11, '6->11')
        graph.add_edge(v7, v6, '7->6')
        graph.add_edge(v7, v11, '7->11')
        graph.add_edge(v8, v0, '8->0')
        graph.add_edge(v8, v4, '8->4')
        graph.add_edge(v8, v14, '8->14')
        graph.add_edge(v9, v2, '9->2')
        graph.add_edge(v9, v3, '9->3')
        graph.add_edge(v9, v15, '9->15')
        graph.add_edge(v10, v15, '10->15')
        graph.add_edge(v11, v6, '11->6')
        graph.add_edge(v11, v7, '11->7')
        graph.add_edge(v13, v0, '13->0')
        graph.add_edge(v13, v14, '13->14')
        graph.add_edge(v15, v2, '15->2')
        graph.add_edge(v15, v9, '15->9')
        graph.add_edge(v15, v10, '15->10')
        graph.add_edge(v16, v5, '16->5')
        graph.add_edge(v17, v5, '17->5')
        # Test.show_graph(graph)
        collected_vertices = list()
        components = defaultdict(list)
        component_number = 0
        for vertex in graph.vertices.values():
            prev_count = len(collected_vertices)
            for v in GraphAlgorithms.dfs(vertex):
                collected_vertices.append(v)
                components[component_number].append(v)
            if len(collected_vertices) != prev_count:
                component_number += 1
        assert len(collected_vertices) == len(graph.vertices)
        assert len(components) == 5
        assert (v0 in components[0] and
                v4 in components[0] and
                v8 in components[0] and
                v13 in components[0] and
                v14 in components[0])
        assert (v1 in components[1] and
                v5 in components[1] and
                v16 in components[1] and
                v17 in components[1])
        assert (v2 in components[2] and
                v3 in components[2] and
                v9 in components[2] and
                v10 in components[2] and
                v15 in components[2])
        assert (v6 in components[3] and
                v7 in components[3] and
                v11 in components[3])
        assert (v12 in components[4])

    def test_graph_dfs_connected_components_random_success(self):
        now = datetime.now()
        print(f"Start: {now}")
        n = 1000  # watch recursion
        for k in range(100):
            now = datetime.now()
            print(f"Iteration: {k}  {now}")
            graph = Test.generate_random_graph(n, digraph=False)
            # Test.show_graph(graph)
            vertices = list(graph.vertices.values())
            print(f"Vertices collected ... {len(graph.vertices)}")
            print(f"Edges collected ... {len(graph.edges)}")
            collected_vertices = list()
            components = defaultdict(list)
            component_number = 0
            for vertex in graph.vertices.values():
                prev_count = len(collected_vertices)
                for v in GraphAlgorithms.dfs(vertex):
                    collected_vertices.append(v)
                    components[component_number].append(v)
                if len(collected_vertices) != prev_count:
                    component_number += 1
            print(f"Components: {len(components)}")
            assert len(collected_vertices) == len(graph.vertices)
            assert len(components) > 0
        now = datetime.now()
        print(f"End: {now}")

    def test_find_tree_center_success(self):
        graph = Graph(digraph=False)
        v0 = Vertex(0, '0', 0)
        v1 = Vertex(1, '1', 1)
        v2 = Vertex(2, '2', 2)
        v3 = Vertex(3, '3', 3)
        v4 = Vertex(4, '4', 4)
        v5 = Vertex(5, '5', 5)
        v6 = Vertex(6, '6', 6)
        v7 = Vertex(7, '7', 7)
        v8 = Vertex(8, '8', 8)
        v9 = Vertex(9, '9', 9)
        graph.add_vertex(v0)
        graph.add_vertex(v1)
        graph.add_vertex(v2)
        graph.add_vertex(v3)
        graph.add_vertex(v4)
        graph.add_vertex(v5)
        graph.add_vertex(v6)
        graph.add_vertex(v7)
        graph.add_vertex(v8)
        graph.add_vertex(v9)
        graph.add_edge(v0, v1, '0->1')
        # graph.add_edge(v1, v0, '1->0')
        graph.add_edge(v1, v2, '1->2')
        # graph.add_edge(v2, v1, '2->1')
        graph.add_edge(v2, v3, '2->3')
        graph.add_edge(v2, v6, '2->6')
        graph.add_edge(v2, v9, '2->9')
        # graph.add_edge(v3, v2, '3->2')
        graph.add_edge(v3, v4, '3->4')
        graph.add_edge(v3, v5, '3->5')
        # graph.add_edge(v4, v3, '4->3')
        # graph.add_edge(v5, v3, '5->3')
        graph.add_edge(v6, v7, '6->7')
        graph.add_edge(v6, v8, '6->8')
        # graph.add_edge(v7, v6, '7->6')
        # graph.add_edge(v8, v6, '8->6')
        # graph.add_edge(v9, v2, '9->2')
        # Test.show_graph(graph)
        roots = GraphAlgorithms.find_tree_centers(graph)
        print(f"Roots: {roots}")
        assert len(roots) == 1
        assert roots[0] == v2

    def test_find_tree_centers_success(self):
        graph = Graph(digraph=False)
        v0 = Vertex(0, '0', 0)
        v1 = Vertex(1, '1', 1)
        v2 = Vertex(2, '2', 2)
        v3 = Vertex(3, '3', 3)
        v4 = Vertex(4, '4', 4)
        v5 = Vertex(5, '5', 5)
        v6 = Vertex(6, '6', 6)
        v7 = Vertex(7, '7', 7)
        v8 = Vertex(8, '8', 8)
        v9 = Vertex(9, '9', 9)
        graph.add_vertex(v0)
        graph.add_vertex(v1)
        graph.add_vertex(v2)
        graph.add_vertex(v3)
        graph.add_vertex(v4)
        graph.add_vertex(v5)
        graph.add_vertex(v6)
        graph.add_vertex(v7)
        graph.add_vertex(v8)
        graph.add_vertex(v9)
        graph.add_edge(v0, v1, '0->1')
        graph.add_edge(v1, v3, '1->3')
        graph.add_edge(v1, v4, '1->4')
        graph.add_edge(v2, v3, '2->3')
        # graph.add_edge(v3, v1, '3->1')
        # graph.add_edge(v3, v2, '3->2')
        graph.add_edge(v3, v6, '3->6')
        graph.add_edge(v3, v7, '3->7')
        # graph.add_edge(v4, v1, '4->1')
        graph.add_edge(v4, v5, '4->5')
        graph.add_edge(v4, v8, '4->8')
        # graph.add_edge(v5, v4, '5->4')
        # graph.add_edge(v6, v3, '6->3')
        graph.add_edge(v6, v9, '6->9')
        # graph.add_edge(v7, v3, '7->3')
        # graph.add_edge(v8, v4, '8->4')
        # graph.add_edge(v9, v6, '9->6')
        # Test.show_graph(graph)
        roots = GraphAlgorithms.find_tree_centers(graph)
        print(f"Roots: {roots}")
        assert len(roots) == 2
        assert roots[0] == v1
        assert roots[1] == v3

    def test_find_tree_centers_random_success(self):
        now = datetime.now()
        print(f"Start: {now}")
        n = 100  # watch recursion
        for k in range(100):
            now = datetime.now()
            print(f"Iteration: {k}  {now}")
            graph = Test.generate_random_graph(n, digraph=False)
            # Test.show_graph(graph)
            print(f"Vertices collected ... {len(graph.vertices)}")
            print(f"Edges collected ... {len(graph.edges)}")
            roots = GraphAlgorithms.find_tree_centers(graph)
            print([root.id for root in roots])
        now = datetime.now()
        print(f"End: {now}")

    @staticmethod
    def get_topological_order_dfs_colored_graph():
        graph = Graph(digraph=True)
        va = Vertex(0,  'A', 'A', color=Colors.WHITE)
        vb = Vertex(1,  'B', 'B', color=Colors.WHITE)
        vc = Vertex(2,  'C', 'C', color=Colors.WHITE)
        vd = Vertex(3,  'D', 'D', color=Colors.WHITE)
        ve = Vertex(4,  'E', 'E', color=Colors.WHITE)
        vf = Vertex(5,  'F', 'F', color=Colors.WHITE)
        vg = Vertex(6,  'G', 'G', color=Colors.WHITE)
        vh = Vertex(7,  'H', 'H', color=Colors.WHITE)
        vj = Vertex(8,  'J', 'J', color=Colors.WHITE)
        vi = Vertex(9,  'I', 'I', color=Colors.WHITE)
        vk = Vertex(10, 'K', 'K', color=Colors.WHITE)
        vl = Vertex(11, 'L', 'L', color=Colors.WHITE)
        vm = Vertex(12, 'M', 'M', color=Colors.WHITE)
        graph.add_vertex(va)
        graph.add_vertex(vb)
        graph.add_vertex(vc)
        graph.add_vertex(vd)
        graph.add_vertex(ve)
        graph.add_vertex(vf)
        graph.add_vertex(vg)
        graph.add_vertex(vh)
        graph.add_vertex(vj)
        graph.add_vertex(vi)
        graph.add_vertex(vk)
        graph.add_vertex(vl)
        graph.add_vertex(vm)
        graph.add_edge(va, vd, 'A->D')
        graph.add_edge(vb, vd, 'B->D')
        graph.add_edge(vc, va, 'C->A')
        graph.add_edge(vc, vb, 'C->B')
        graph.add_edge(vd, vh, 'D->H')
        graph.add_edge(vd, vg, 'D->G')
        graph.add_edge(ve, va, 'E->A')
        graph.add_edge(ve, vd, 'E->D')
        graph.add_edge(ve, vf, 'E->F')
        graph.add_edge(vf, vj, 'F->J')
        graph.add_edge(vf, vk, 'F->K')
        graph.add_edge(vg, vi, 'G->I')
        graph.add_edge(vh, vi, 'H->I')
        graph.add_edge(vh, vj, 'H->J')
        graph.add_edge(vj, vl, 'J->L')
        graph.add_edge(vj, vm, 'J->M')
        graph.add_edge(vi, vl, 'I->L')
        graph.add_edge(vk, vj, 'K->J')
        # Test.show_graph(graph)
        return graph

    def test_get_topological_order_dfs_colored(self):
        graph = Test.get_topological_order_dfs_colored_graph()
        topological_order = GraphAlgorithms.get_topological_order_dfs_colored(graph)
        topological_order_result = [v.value for v in topological_order]
        print(f"Topological order: {topological_order_result}")
        assert len(topological_order_result) == len(graph.vertices)
        assert topological_order_result == ['E', 'F', 'K', 'C', 'B', 'A', 'D', 'H', 'J', 'M', 'G', 'I', 'L']

    def test_get_topological_order_dfs_colored_gen(self):
        graph = Test.get_topological_order_dfs_colored_graph()
        topological_order_gen = GraphAlgorithms.get_topological_order_dfs_colored_gen(graph)
        topological_order = [v.value for v in topological_order_gen]
        topological_order = [topological_order[k] for k in range(len(topological_order)-1, -1, -1)]
        print(f"Topological order: {topological_order}")
        assert len(topological_order) == len(graph.vertices)
        assert topological_order == ['E', 'F', 'K', 'C', 'B', 'A', 'D', 'H', 'J', 'M', 'G', 'I', 'L']

    def test_get_topological_order_dfs_colored_random(self):
        now = datetime.now()
        print(f"Start: {now}")
        n = 100  # watch recursion
        for k in range(1):
            now = datetime.now()
            print(f"Iteration: {k}  {now}")
            graph = Test.generate_random_graph(n, digraph=True)
            for vertex in graph.vertices.values():
                vertex.color = color=Colors.WHITE
            # Test.show_graph(graph)
            print(f"Vertices collected ... {len(graph.vertices)}")
            print(f"Edges collected ... {len(graph.edges)}")
            try:
                topological_order = GraphAlgorithms.get_topological_order_dfs_colored(graph)
                topological_order_result = [v.value for v in topological_order]
                print(f"Topological order: {topological_order_result}")
                assert len(topological_order_result) == len(graph.vertices)
            except ValueError:
                pass
            else:
                pass
        now = datetime.now()
        print(f"End: {now}")

    def test_get_topological_order_kahn(self):
        graph = Test.get_topological_order_dfs_colored_graph()
        topological_order_gen = GraphAlgorithms.get_topological_order_kahn(graph)
        topological_order = [v.value for v in topological_order_gen]
        print(f"Topological order: {topological_order}")
        assert len(topological_order) == len(graph.vertices)
        assert topological_order == ['E', 'F', 'K', 'C', 'B', 'A', 'D', 'G', 'H', 'J', 'M', 'I', 'L']

    def test_get_topological_order_kahn_small(self):
        graph = Graph(digraph=True)
        v0 = Vertex(0, '0', 0)
        v1 = Vertex(1, '1', 1)
        v2 = Vertex(2, '2', 2)
        v3 = Vertex(3, '3', 3)
        v4 = Vertex(4, '4', 4)
        v5 = Vertex(5, '5', 5)
        graph.add_vertex(v0)
        graph.add_vertex(v1)
        graph.add_vertex(v2)
        graph.add_vertex(v3)
        graph.add_vertex(v4)
        graph.add_vertex(v5)
        graph.add_edge(v0, v1, '0->1')
        graph.add_edge(v0, v3, '0->3')
        graph.add_edge(v2, v0, '2->0')
        graph.add_edge(v2, v4, '2->4')
        graph.add_edge(v3, v1, '3->1')
        graph.add_edge(v4, v3, '4->3')
        graph.add_edge(v4, v5, '4->5')
        graph.add_edge(v5, v1, '5->1')
        topological_order_gen = GraphAlgorithms.get_topological_order_kahn(graph)
        topological_order = [v.value for v in topological_order_gen]
        print(f"Topological order: {topological_order}")
        assert len(topological_order) == len(graph.vertices)
        assert topological_order == [2, 4, 5, 0, 3, 1]

    def test_get_topological_order_kahn_random(self):
        now = datetime.now()
        print(f"Start: {now}")
        n = 100  # watch recursion
        for k in range(1):
            now = datetime.now()
            print(f"Iteration: {k}  {now}")
            graph = Test.generate_random_graph(n, digraph=True)
            for vertex in graph.vertices.values():
                vertex.color = color=Colors.WHITE
            # Test.show_graph(graph)
            print(f"Vertices collected ... {len(graph.vertices)}")
            print(f"Edges collected ... {len(graph.edges)}")
            topological_order_gen = GraphAlgorithms.get_topological_order_kahn(graph)
            topological_order = [v.value for v in topological_order_gen]
            if len(topological_order) == len(graph.vertices):
                print(f"Topological order: {topological_order}")
                assert len(topological_order) == len(graph.vertices)
            else:
                print("Topological order does not exists, ound cycle(s).")
        now = datetime.now()
        print(f"End: {now}")

    def test_adjacency_matrix(self):
        graph = Graph(digraph=True)
        v0 = Vertex(0)
        v1 = Vertex(1)
        v2 = Vertex(2)
        v3 = Vertex(3)
        v4 = Vertex(4)
        v5 = Vertex(5)
        graph.add_vertex(v0)
        graph.add_vertex(v1)
        graph.add_vertex(v2)
        graph.add_vertex(v3)
        graph.add_vertex(v4)
        graph.add_vertex(v5)
        graph.add_edge(v0, v1, 1.3)
        graph.add_edge(v0, v3, -2.53)
        graph.add_edge(v2, v0, 3.67)
        graph.add_edge(v2, v4, 4.99)
        graph.add_edge(v3, v1, -5.19)
        graph.add_edge(v4, v3, 6.76)
        graph.add_edge(v4, v5, -7.54)
        graph.add_edge(v5, v1, 8.623)
        matrix = graph.matrix()
        DomainHelper.print_matrix(matrix)
        matrix = graph.matrix(int)
        DomainHelper.print_matrix(matrix)
        pass

    def test_adjacency_matrix_random(self):
        now = datetime.now()
        print(f"Start: {now}")
        n = 100  # watch recursion
        for k in range(1):
            now = datetime.now()
            print(f"Iteration: {k}  {now}")
            graph = Test.generate_random_graph(n, digraph=True)
            for vertex in graph.vertices.values():
                vertex.color = color=Colors.WHITE
            # Test.show_graph(graph)
            print(f"Vertices collected ... {len(graph.vertices)}")
            print(f"Edges collected ... {len(graph.edges)}")
            matrix = graph.matrix()
            DomainHelper.print_matrix(matrix)
            assert matrix.size == len(graph.vertices)**2
        now = datetime.now()
        print(f"End: {now}")

    def test_calculate_tree_traverses(self):
        v1 = Tree(1, '1')
        v2 = Tree(2, '2')
        v3 = Tree(3, '3')
        v4 = Tree(4, '4')
        v5 = Tree(5, '5')
        v6 = Tree(6, '6')
        v7 = Tree(7, '7')
        v1.add_kid(v2)
        v1.add_kid(v3)
        v2.add_kid(v4)
        v2.add_kid(v5)
        v3.add_kid(v6)
        v3.add_kid(v7)
        # Test.show_tree(v0)
        preorder, postorder = GraphAlgorithms.calculate_tree_traverses(v1)
        assert preorder == [v1, v2, v4, v5, v3, v6, v7]
        assert postorder == [v4, v5, v2, v6, v7, v3, v1]

    def test_networkx_random_tree(self):
        now = datetime.now()
        print(f"Start: {now}")
        n = 1000  # watch recursion
        for k in range(100):
            now = datetime.now()
            print(f"Iteration: {k}  {now}")
            tree = Test.generate_random_tree(n)
            # Test.show_tree(tree)
            preorder, postorder = GraphAlgorithms.calculate_tree_traverses(tree[0])
            assert len(preorder) == n
            assert len(postorder) == n
        now = datetime.now()
        print(f"End: {now}")

    def test_calculate_euler_tour(self):
        v0 = Tree(0, '0')
        v1 = Tree(1, '1')
        v2 = Tree(2, '2')
        v3 = Tree(3, '3')
        v4 = Tree(4, '4')
        v5 = Tree(5, '5')
        v6 = Tree(6, '6')
        v0.add_kid(v1)
        v0.add_kid(v2)
        v1.add_kid(v3)
        v2.add_kid(v4)
        v2.add_kid(v5)
        v4.add_kid(v6)
        # Test.show_tree(v0)
        nodes, depths, lasts = GraphAlgorithms.calculate_euler_tour(v0)
        assert len(nodes) == (2 * 7 - 1)
        assert nodes == [v0, v1, v3, v1, v0, v2, v4, v6, v4, v2, v5, v2, v0]
        assert depths == [0, 1, 2, 1, 0, 1, 2, 3, 2, 1, 2, 1, 0]
        assert len(depths) == (2 * 7 - 1)
        assert list(lasts.values()) == [12, 3, 2, 11, 8, 7, 10]
        assert len(lasts) == 7

    def test_calculate_euler_tour2(self):
        v1 = Tree(1, '1')
        v2 = Tree(2, '2')
        v3 = Tree(3, '3')
        v4 = Tree(4, '4')
        v5 = Tree(5, '5')
        v6 = Tree(6, '6')
        v7 = Tree(7, '7')
        v1.add_kid(v2)
        v1.add_kid(v3)
        v1.add_kid(v4)
        v3.add_kid(v5)
        v3.add_kid(v6)
        v3.add_kid(v7)
        # Test.show_tree(v1)
        nodes, depths, lasts = GraphAlgorithms.calculate_euler_tour(v1)
        assert len(nodes) == (2 * 7 - 1)
        assert nodes == [v1, v2, v1, v3, v5, v3, v6, v3, v7, v3, v1, v4, v1]
        assert len(depths) == (2 * 7 - 1)
        assert depths == [0, 1, 0, 1, 2, 1, 2, 1, 2, 1, 0, 1, 0]
        assert list(lasts.values()) == [12, 1, 9, 4, 6, 8, 11]
        assert len(lasts) == 7

    def test_calculate_euler_tour_random(self):
        now = datetime.now()
        print(f"Start: {now}")
        n = 1000  # watch recursion
        for k in range(100):
            now = datetime.now()
            print(f"Iteration: {k}  {now}")
            tree = Test.generate_random_tree(n)
            # Test.show_tree(tree)
            nodes, depths, lasts = GraphAlgorithms.calculate_euler_tour(tree[0])
            assert len(nodes) == (2 * n - 1)
            assert len(lasts) == n
        now = datetime.now()
        print(f"End: {now}")

    @staticmethod
    def tree_cleaner(vertex):
        vertex.flags = Flags.CLEAR

    def test_calculate_lowest_common_ancestor(self):
        v0 = Tree(0, '0')
        v1 = Tree(1, '1')
        v2 = Tree(2, '2')
        v3 = Tree(3, '3')
        v4 = Tree(4, '4')
        v5 = Tree(5, '5')
        v6 = Tree(6, '6')
        v0.add_kid(v1)
        v0.add_kid(v2)
        v1.add_kid(v3)
        v2.add_kid(v4)
        v2.add_kid(v5)
        v4.add_kid(v6)
        GraphAlgorithms.calculate_tree_traverses(v0, Test.tree_cleaner)
        tree = GraphAlgorithms.calculate_lowest_common_ancestor(v0, v6, v5)
        assert tree == v2
        GraphAlgorithms.calculate_tree_traverses(v0, Test.tree_cleaner)
        tree = GraphAlgorithms.calculate_lowest_common_ancestor(v0, v3, v3)
        assert tree == v3

    def test_calculate_lowest_common_ancestor_17_nodes(self):
        v0 = Tree(0, '0')
        v1 = Tree(1, '1')
        v2 = Tree(2, '2')
        v3 = Tree(3, '3')
        v4 = Tree(4, '4')
        v5 = Tree(5, '5')
        v6 = Tree(6, '6')
        v7 = Tree(6, '7')
        v8 = Tree(6, '8')
        v9 = Tree(6, '9')
        v10 = Tree(10, '10')
        v11 = Tree(11, '11')
        v12 = Tree(12, '12')
        v13 = Tree(13, '13')
        v14 = Tree(14, '14')
        v15 = Tree(15, '15')
        v16 = Tree(16, '16')
        v0.add_kid(v1)
        v0.add_kid(v2)
        v1.add_kid(v3)
        v1.add_kid(v4)
        v2.add_kid(v5)
        v2.add_kid(v6)
        v2.add_kid(v7)
        v3.add_kid(v8)
        v3.add_kid(v9)
        v5.add_kid(v10)
        v5.add_kid(v11)
        v7.add_kid(v12)
        v7.add_kid(v13)
        v11.add_kid(v14)
        v11.add_kid(v15)
        v11.add_kid(v16)
        GraphAlgorithms.calculate_tree_traverses(v0, Test.tree_cleaner)
        tree = GraphAlgorithms.calculate_lowest_common_ancestor(v0, v14, v13)
        assert tree == v2
        GraphAlgorithms.calculate_tree_traverses(v0, Test.tree_cleaner)
        tree = GraphAlgorithms.calculate_lowest_common_ancestor(v0, v12, v12)
        assert tree == v12
        GraphAlgorithms.calculate_tree_traverses(v0, Test.tree_cleaner)
        tree = GraphAlgorithms.calculate_lowest_common_ancestor(v0, v16, v12)
        assert tree == v2
        GraphAlgorithms.calculate_tree_traverses(v0, Test.tree_cleaner)
        tree = GraphAlgorithms.calculate_lowest_common_ancestor(v0, v10, tree)
        assert tree == v2

    def test_calculate_lowest_common_ancestor_random(self):
        now = datetime.now()
        print(f"Start: {now}")
        n = 1000  # watch recursion
        for k in range(100):
            now = datetime.now()
            print(f"Iteration: {k}  {now}")
            tree = Test.generate_random_tree(n)
            k1 = random.randint(0, len(tree) - 1)
            k2 = random.randint(0, len(tree) - 1)
            tree = GraphAlgorithms.calculate_lowest_common_ancestor(tree[0], tree[k1], tree[k2])
            print(tree.id)
        now = datetime.now()
        print(f"End: {now}")

    def test_execute_range_minimum_queries(self):
        array = [4, 2, 3, 7, 1, 5, 3, 3, 9, 6, 7, -1, 4]
        queries = [(2, 7), (2, 10), (5, 9), (7, 9), (1, 11), (3, 5), (10, 14)]
        answers = Algorithms.execute_range_minmax_queries(array, queries)
        assert answers == [(1, 4), (1, 4), (3, 6), (3, 7), (-1, 11), (1, 4), (float('-inf'), 0)]

    def test_execute_range_minimum_queries_same(self):
        array = [5, 5, 5, 5, 5, 5, 5]
        queries = [(0, len(array) - 1)]
        answers = Algorithms.execute_range_minmax_queries(array, queries)
        assert answers == [(5, 0)]

    def test_execute_range_minimum_queries_random(self):
        now = datetime.now()
        print(f"Start: {now}")
        n = 1000  # watch recursion
        for k in range(100):
            now = datetime.now()
            print(f"Iteration: {k}  {now}")
            array, queries = Test.generate_random_array_queries(n)
            answers = Algorithms.execute_range_minmax_queries(array, queries)
        now = datetime.now()
        print(f"End: {now}")

    def test_execute_range_maximum_queries(self):
        array = [4, 2, 3, 7, 1, 5, 3, 3, 9, 6, 7, -1, 4]
        queries = [(2, 7), (2, 10), (5, 9), (7, 9), (1, 11), (3, 5), (10, 14)]
        answers = Algorithms.execute_range_minmax_queries(array, queries, function=Algorithms.Functions.MAX)
        assert answers == [(7, 3), (9, 8), (9, 8), (9, 8), (9, 8), (7, 3), (float('-inf'), 0)]

    def test_execute_range_maximum_queries_same(self):
        array = [5, 5, 5, 5, 5, 5, 5]
        queries = [(0, len(array) - 1)]
        answers = Algorithms.execute_range_minmax_queries(array, queries, function=Algorithms.Functions.MAX)
        assert answers == [(5, 0)]

    def test_execute_range_maximum_queries_random(self):
        now = datetime.now()
        print(f"Start: {now}")
        n = 1000  # watch recursion
        for k in range(100):
            now = datetime.now()
            print(f"Iteration: {k}  {now}")
            array, queries = Test.generate_random_array_queries(n)
            answers = Algorithms.execute_range_minmax_queries(array, queries, function=Algorithms.Functions.MAX)
        now = datetime.now()
        print(f"End: {now}")


if __name__ == '__main__':
    """
    """
    unittest.main()
