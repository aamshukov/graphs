#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import random
import unittest
import locale
from graph.core.domain_helper import DomainHelper
from graph.core.text import Text
from graph.indexing.index import Index
from graph.indexing.memory_repository import InMemoryRepository


class Test(unittest.TestCase):
    def test_in_memory_repository_init_success(self):
        for n in range(1, 127):
            page_size = n
            repository = InMemoryRepository(page_size)
            data_to_write = bytearray([k + 1 for k in range(page_size)])
            print([str(ch) for ch in data_to_write])
            repository.write(0, data_to_write)
            read_data = repository.read(0, len(data_to_write))
            assert data_to_write == read_data

    def test_in_memory_repository_access_success(self):
        for n in range(1, 127):
            page_size = n
            repository = InMemoryRepository(page_size)
            data_to_write = bytearray([k + 1 for k in range(2 * page_size - 1)])
            print([str(ch) for ch in data_to_write])
            repository.write(10, data_to_write)
            read_data = repository.read(10, len(data_to_write))
            assert data_to_write == read_data

    def test_in_memory_repository_page_access_random_success(self):
        for n in range(1, 10000):
            page_size = random.randint(1, 4097)
            data_count = random.randint(1, page_size)
            data_count = data_count * 2 if data_count % 2 == 0 else data_count
            data_count = data_count - 1 if data_count % 5 == 0 else data_count
            offset = random.randint(0, page_size)
            repository = InMemoryRepository(page_size)
            data_to_write = bytearray()
            for chunk in range(1, data_count // 256):
                data_to_write.extend([k + 1 for k in range(chunk)])
            data_to_write.extend([k + 1 for k in range(data_count % 256)])
            if page_size < 128:
                print([str(ch) for ch in data_to_write])
            repository.write(offset, data_to_write)
            read_data = repository.read(offset, len(data_to_write))
            assert data_to_write == read_data

    def test_in_memory_repository_pages_access_random_success(self):
        for n in range(1, 1000):
            page_size = random.randint(1, 4097)
            data_count = random.randint(1, page_size * 16)
            data_count = data_count * 2 if data_count % 2 == 0 else data_count
            data_count = data_count - 1 if data_count % 5 == 0 else data_count
            offset = random.randint(0, page_size)
            repository = InMemoryRepository(page_size)
            data_to_write = bytearray()
            for chunk in range(1, data_count // 256):
                data_to_write.extend([k for k in range(256)])
            data_to_write.extend([k for k in range(data_count % 256)])
            repository.write(offset, data_to_write)
            read_data = repository.read(offset, len(data_to_write))
            assert data_to_write == read_data

    def test_in_memory_repository_random_success(self):
        for n in range(1, 1000):
            page_size = random.randint(1, random.randint(2049, 65636))
            data_count = random.randint(1, page_size * 16)
            data_count = data_count * 2 if data_count % 2 == 0 else data_count
            data_count = data_count - 1 if data_count % 5 == 0 else data_count
            offset = random.randint(0, page_size)
            repository = InMemoryRepository(page_size)
            data_to_write = DomainHelper.generate_random_bytes(data_count)
            for chunk in range(1, data_count // 256):
                data_to_write.extend([k for k in range(256)])
            data_to_write.extend([k for k in range(data_count % 256)])
            repository.write(offset, data_to_write)
            read_data = repository.read(offset, len(data_to_write))
            assert data_to_write == read_data

    def test_branch_tree_serialization_success(self):
        fanout = 5
        btree_branch = Index.BTreeBranch(0, fanout)
        keys0 = ['Key1သည်', 'Key2山乇ㄥ', 'Key3етств', 'Key4ɹoʇıp', 'Key5ಠ益ಠ']
        for k, key in enumerate(keys0):
            btree_branch.set_key(key, k)
        kids0 = [Index.BTreeBranch(k, fanout) for k in range(0, fanout + 1)]
        for k, kid in enumerate(kids0):
            btree_branch.set_kid(kid, k)
        buffer = btree_branch.serialize()
        assert len(buffer) == Index.BTreeBranch.calculate_size(fanout)
        header, keys_count, keys, kids = Index.BTreeBranch.deserialize(buffer)
        assert header == Index.TreeHeader
        assert keys == btree_branch.keys
        assert kids == btree_branch.kid_ids

    def test_leaf_tree_serialization_success(self):
        locale.getpreferredencoding = lambda: 'utf-8'
        fanout = 5
        btree_leaf = Index.BTreeLeaf(0, fanout)
        keys0 = ['Key1သည်', 'Key2山乇ㄥ', 'Key3етств', 'Key4ɹoʇıp', 'Key5ಠ益ಠ']
        for k, key in enumerate(keys0):
            btree_leaf.set_key(key, k)
        values0 = ['Value1သည်', 'Value2山乇ㄥ', 'Value3етств', 'Value4ɹoʇıp', 'Value5ಠ益ಠ']
        for k, value in enumerate(values0):
            btree_leaf.set_value(value, k)
        btree_leaf.prev_id = 1
        btree_leaf.next_id = 3
        buffer = btree_leaf.serialize()
        assert len(buffer) == Index.BTreeLeaf.calculate_size(fanout)
        header, keys_count, keys, values, prev_id, next_id = Index.BTreeLeaf.deserialize(buffer)
        assert header == Index.TreeHeader
        assert prev_id == 1
        assert next_id == 3
        assert keys == btree_leaf.keys
        assert values == btree_leaf.values

    def test_tree_calculate_offset_success(self):
        fanout = 4
        repository = InMemoryRepository(512)
        index = Index(repository, fanout=fanout)
        offset = index.calculate_offset(0)
        assert offset == Index.HeaderSize
        offset = index.calculate_offset(1)
        assert offset == Index.HeaderSize + Index.BTreeBranch.calculate_size(fanout)
        offset = index.calculate_offset(2)
        assert offset == Index.HeaderSize + 2 * Index.BTreeBranch.calculate_size(fanout)

    def test_branch_tree_load_save_success(self):
        fanout = 5
        btree_branch = Index.BTreeBranch(0, fanout)
        keys0 = ['Key1သည်', 'Key2山乇ㄥ', 'Key3етств', 'Key4ɹoʇıp', 'Key5ಠ益ಠ']
        for k, key in enumerate(keys0):
            btree_branch.set_key(key, k)
        kids0 = [Index.BTreeBranch(k, fanout) for k in range(0, fanout + 1)]
        for k, kid in enumerate(kids0):
            btree_branch.set_kid(kid, k)
        repository = InMemoryRepository(512)
        index = Index(repository, fanout=fanout)
        index.save_tree(btree_branch)
        btree = index.load_tree(btree_branch.id)
        assert btree == btree_branch

    def test_leaf_tree_load_save_success(self):
        fanout = 5
        btree_leaf = Index.BTreeLeaf(0, fanout)
        keys0 = ['Key1သည်', 'Key2山乇ㄥ', 'Key3етств', 'Key4ɹoʇıp', 'Key5ಠ益ಠ']
        for k, key in enumerate(keys0):
            btree_leaf.set_key(key, k)
        values0 = ['Value1သည်', 'Value2山乇ㄥ', 'Value3етств', 'Value4ɹoʇıp', 'Value5ಠ益ಠ']
        for k, value in enumerate(values0):
            btree_leaf.set_value(value, k)
        btree_leaf.prev_id = 1
        btree_leaf.next_id = 3
        repository = InMemoryRepository(512)
        index = Index(repository, fanout=fanout)
        index.save_tree(btree_leaf)
        btree = index.load_tree(btree_leaf.id, leaf=True)
        assert btree == btree_leaf

    def test_search_key_success(self):
        keys = sorted(['one', 'Keyသည်', 'Key山乇ㄥ', 'Keyетств', 'Keyɹoʇıp', 'Keyಠ益ಠ'])
        fanout = len(keys)
        btree_branch = Index.BTreeBranch(0, fanout)
        for k, key in enumerate(keys):
            btree_branch.set_key(key, k)
        assert btree_branch.search_key('one') == 5
        assert btree_branch.search_key('Keyသည်') == 3
        assert btree_branch.search_key('Key山乇ㄥ') == 4
        assert btree_branch.search_key('Keyетств') == 1
        assert btree_branch.search_key('Keyɹoʇıp') == 0
        assert btree_branch.search_key('Keyಠ益ಠ') == 2
        assert btree_branch.search_key('test') == -1

    def test_search_key_partial_success(self):
        keys = sorted(['one', 'Keyသည်', 'Key山乇ㄥ', 'Keyетств', 'Keyɹoʇıp', 'Keyಠ益ಠ', 'z', 'z'])
        fanout = len(keys)
        btree_branch = Index.BTreeBranch(0, fanout)
        for k, key in enumerate(keys):
            btree_branch.set_key(key, k)
        assert btree_branch.search_key('one', hi=5) == 5
        assert btree_branch.search_key('Keyသည်', hi=5) == 3
        assert btree_branch.search_key('Key山乇ㄥ', hi=5) == 4
        assert btree_branch.search_key('Keyетств', hi=5) == 1
        assert btree_branch.search_key('Keyɹoʇıp', hi=5) == 0
        assert btree_branch.search_key('Keyಠ益ಠ', hi=5) == 2
        assert btree_branch.search_key('test', hi=5) == -1

    def test_search_key_random_success(self):
        count = 1000
        keys = sorted([Text.generate_random_string(k) for k in range(0, count)])
        for k in range(1, len(keys)):
            key_index = random.randint(0, len(keys) - 1)
            fanout = len(keys)
            btree_branch = Index.BTreeBranch(0, fanout)
            for i, key in enumerate(keys):
                btree_branch.set_key(key, i)
            assert btree_branch.search_key(keys[key_index]) != -1

    def test_search_key_position_success(self):
        keys = []
        fanout = len(keys)
        btree_branch = Index.BTreeBranch(0, fanout)
        for k, key in enumerate(keys):
            btree_branch.set_key(key, k)
        assert btree_branch.search_key_position('a') == 0
        keys = [None]
        fanout = len(keys)
        btree_branch = Index.BTreeBranch(0, fanout)
        for k, key in enumerate(keys):
            btree_branch.set_key(key, k)
        assert btree_branch.search_key_position('a') == 1
        keys = [None, None]
        fanout = len(keys)
        btree_branch = Index.BTreeBranch(0, fanout)
        for k, key in enumerate(keys):
            btree_branch.set_key(key, k)
        assert btree_branch.search_key_position('a') == 2
        keys = [None, None, None, 'a', 'b']
        fanout = len(keys)
        btree_branch = Index.BTreeBranch(0, fanout)
        for k, key in enumerate(keys):
            btree_branch.set_key(key, k)
        assert btree_branch.search_key_position('a') == 4
        keys = [None, None, None, 'b']
        fanout = len(keys)
        btree_branch = Index.BTreeBranch(0, fanout)
        for k, key in enumerate(keys):
            btree_branch.set_key(key, k)
        assert btree_branch.search_key_position('a') == 3
        keys = sorted(['one', 'Keyသည်', 'Key山乇ㄥ', 'Keyетств', 'Keyɹoʇıp', 'Keyಠ益ಠ'])
        fanout = len(keys)
        btree_branch = Index.BTreeBranch(0, fanout)
        for k, key in enumerate(keys):
            btree_branch.set_key(key, k)
        assert btree_branch.search_key_position('one') == 6
        assert btree_branch.search_key_position('Keyသည်') == 4
        assert btree_branch.search_key_position('Key山乇ㄥ') == 5
        assert btree_branch.search_key_position('Keyетств') == 2
        assert btree_branch.search_key_position('Keyɹoʇıp') == 1
        assert btree_branch.search_key_position('Keyಠ益ಠ') == 3
        assert btree_branch.search_key_position('test') == 6

    def test_search_key_position_desc_success(self):
        keys = []
        fanout = len(keys)
        btree_branch = Index.BTreeBranch(0, fanout)
        for k, key in enumerate(keys):
            btree_branch.set_key(key, k)
        assert btree_branch.search_key_position('a', desc=True) == 0
        keys = [None]
        fanout = len(keys)
        btree_branch = Index.BTreeBranch(0, fanout)
        for k, key in enumerate(keys):
            btree_branch.set_key(key, k)
        assert btree_branch.search_key_position('a', desc=True) == 0
        keys = [None, None]
        fanout = len(keys)
        btree_branch = Index.BTreeBranch(0, fanout)
        for k, key in enumerate(keys):
            btree_branch.set_key(key, k)
        assert btree_branch.search_key_position('a', desc=True) == 0
        keys = ['a', 'b', None, None, None]
        fanout = len(keys)
        btree_branch = Index.BTreeBranch(0, fanout)
        for k, key in enumerate(keys):
            btree_branch.set_key(key, k)
        assert btree_branch.search_key_position('a', desc=True) == 1
        keys = ['b', None, None, None]
        fanout = len(keys)
        btree_branch = Index.BTreeBranch(0, fanout)
        for k, key in enumerate(keys):
            btree_branch.set_key(key, k)
        assert btree_branch.search_key_position('a', desc=True) == 0
        keys = sorted(['one', 'Keyသည်', 'Key山乇ㄥ', 'Keyетств', 'Keyɹoʇıp', 'Keyಠ益ಠ'])
        fanout = len(keys)
        btree_branch = Index.BTreeBranch(0, fanout)
        for k, key in enumerate(keys):
            btree_branch.set_key(key, k)
        assert btree_branch.search_key_position('one', desc=True) == 6
        assert btree_branch.search_key_position('Keyသည်', desc=True) == 4
        assert btree_branch.search_key_position('Key山乇ㄥ', desc=True) == 5
        assert btree_branch.search_key_position('Keyетств', desc=True) == 2
        assert btree_branch.search_key_position('Keyɹoʇıp', desc=True) == 1
        assert btree_branch.search_key_position('Keyಠ益ಠ', desc=True) == 3
        assert btree_branch.search_key_position('test', desc=True) == 6

    def test_search_key_position_partial_success(self):
        keys = sorted(['one', 'Keyသည်', 'Key山乇ㄥ', 'Keyетств', 'Keyɹoʇıp', 'Keyಠ益ಠ', 'z', 'z'])
        keys[6] = None
        keys[7] = None
        fanout = len(keys)
        btree_branch = Index.BTreeBranch(0, fanout)
        for k, key in enumerate(keys):
            btree_branch.set_key(key, k)
        assert btree_branch.search_key_position('one', hi=6) == 6
        assert btree_branch.search_key_position('Keyသည်', hi=6) == 4
        assert btree_branch.search_key_position('Key山乇ㄥ', hi=6) == 5
        assert btree_branch.search_key_position('Keyетств', hi=6) == 2
        assert btree_branch.search_key_position('Keyɹoʇıp', hi=6) == 1
        assert btree_branch.search_key_position('Keyಠ益ಠ', hi=6) == 3
        assert btree_branch.search_key_position('test', hi=6) == 6

    def test_insert_key_success(self):
        keys = [None]
        fanout = len(keys)
        btree_branch = Index.BTreeBranch(0, fanout)
        for k, key in enumerate(keys):
            btree_branch.set_key(key, k)
        keys, position = btree_branch.insert_key('a')
        fanout = len(keys)
        btree_branch = Index.BTreeBranch(0, fanout)
        for k, key in enumerate(keys):
            btree_branch.set_key(key, k)
        assert keys, position == (['a'], 0)
        keys = [None, None]
        fanout = len(keys)
        btree_branch = Index.BTreeBranch(0, fanout)
        for k, key in enumerate(keys):
            btree_branch.set_key(key, k)
        assert btree_branch.insert_key('a') == (['a', None], 0)
        keys = [None, None, None]
        fanout = len(keys)
        btree_branch = Index.BTreeBranch(0, fanout)
        for k, key in enumerate(keys):
            btree_branch.set_key(key, k)
        assert btree_branch.insert_key('a') == (['a', None, None], 0)
        keys = ['a', None, None, None]
        fanout = len(keys)
        btree_branch = Index.BTreeBranch(0, fanout)
        for k, key in enumerate(keys):
            btree_branch.set_key(key, k)
        assert btree_branch.insert_key('a') == (['a', 'a', None, None], 1)
        keys = ['a', 'b', None, None, None]
        fanout = len(keys)
        btree_branch = Index.BTreeBranch(0, fanout)
        for k, key in enumerate(keys):
            btree_branch.set_key(key, k)
        assert btree_branch.insert_key('a') == (['a', 'a', 'b', None, None], 1)
        keys = ['a', 'b', 'c', None]
        fanout = len(keys)
        btree_branch = Index.BTreeBranch(0, fanout)
        for k, key in enumerate(keys):
            btree_branch.set_key(key, k)
        assert btree_branch.insert_key('b') == (['a', 'b', 'b', 'c'], 2)
        keys = ['a', 'b', 'c']
        fanout = len(keys)
        btree_branch = Index.BTreeBranch(0, fanout)
        for k, key in enumerate(keys):
            btree_branch.set_key(key, k)
        assert btree_branch.insert_key('b') == (['a', 'b', 'b'], 2)
        keys = ['a', 'b', None, None, None]
        fanout = len(keys)
        btree_branch = Index.BTreeBranch(0, fanout)
        for k, key in enumerate(keys):
            btree_branch.set_key(key, k)
        assert btree_branch.insert_key('a', hi=3) == (['a', 'a', 'b', None, None], 1)

    def test_split_branch_success(self):
        fanout = 3
        papa = Index.BTreeBranch(0, fanout)
        for k in range(fanout):
            papa.set_key(f'KeyPapa{k + 1}', k)
        for k in range(fanout + 1):
            kid = Index.BTreeBranch(k + 1, fanout)
            for i in range(fanout):
                kid.set_key(f'KeyKid{(i + 1) * 10}', i)
            for i in range(fanout + 1):
                kid.set_kid(Index.BTreeBranch((i + 1) * 10, fanout), i)
            papa.set_kid(kid, k)
        repository = InMemoryRepository(512)
        index = Index(repository, fanout=fanout)
        papa, kid, new_kid = index.split_branch(papa, papa.kids[0])
        pass

    def test_split_leaf_success(self):
        fanout = 3
        papa = Index.BTreeBranch(0, fanout)
        for k in range(fanout):
            papa.set_key(f'KeyPapa{k + 1}', k)
        for k in range(fanout + 1):
            kid = Index.BTreeLeaf(k + 1, fanout)
            for i in range(fanout):
                kid.set_key(f'KeyKid{(i + 1) * 10}', i)
                kid.set_value(f'ValueKid{(i + 1) * 10}', i)
            papa.set_kid(kid, k)
        repository = InMemoryRepository(512)
        index = Index(repository, fanout=fanout)
        papa, kid, new_kid = index.split_leaf(papa, papa.kids[0])
        pass

    def test_index_insert_5937128604_success(self):
        fanout = 3
        repository = InMemoryRepository(512)
        index = Index(repository, fanout=fanout)
        index.insert('5', '5*')
        print(Index.to_string(index.root))
        index.insert('9', '9*')
        print(Index.to_string(index.root))
        index.insert('3', '3*')
        print(Index.to_string(index.root))
        index.insert('7', '7*')
        print(Index.to_string(index.root))
        index.insert('1', '1*')
        print(Index.to_string(index.root))
        index.insert('2', '2*')
        print(Index.to_string(index.root))
        index.insert('8', '8*')
        print(Index.to_string(index.root))
        index.insert('6', '6*')
        print(Index.to_string(index.root))
        index.insert('0', '0*')
        print(Index.to_string(index.root))
        index.insert('4', '4*')
        print(Index.to_string(index.root))
        assert index.height == 3
        assert index.number_of_branches == 3
        assert index.number_of_leaves == 4
        assert index.number_of_nodes == 7
        tree, value, position = index.search('5')
        assert tree is None
        assert value == '5'
        assert position == 0
        tree, value, position = index.search('9')
        assert tree is None
        assert value == '9'
        assert position == 0
        tree, value, position = index.search('3')
        assert tree is None
        assert value == '3'
        assert position == 0
        tree, value, position = index.search('7')
        assert tree is None
        assert value == '7'
        assert position == 0
        tree, value, position = index.search('1')
        assert tree is None
        assert value == '1'
        assert position == 0
        tree, value, position = index.search('2')
        assert tree is None
        assert value == '2'
        assert position == 0
        tree, value, position = index.search('8')
        assert tree is None
        assert value == '8'
        assert position == 0
        tree, value, position = index.search('6')
        assert tree is None
        assert value == '6'
        assert position == 0
        tree, value, position = index.search('0')
        assert tree is None
        assert value == '0'
        assert position == 0
        tree, value, position = index.search('4')
        assert tree is None
        assert value == '4'
        assert position == 0


if __name__ == '__main__':
    """
    """
    unittest.main()
