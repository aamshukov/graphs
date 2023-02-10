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
        for n in range(1, 10000):
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
        for n in range(1, 10000):
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

    def test_inner_tree_serialization_success(self):
        fanout = 4
        btree_inner = Index.BTree(0, fanout)
        keys = ['Key1သည်', 'Key2山乇ㄥ', 'Key3етств', 'Key4ɹoʇıp', 'Key5ಠ益ಠ']
        for key in keys:
            btree_inner.add_key(key)
        kids = [Index.BTree(k, fanout) for k in range(1, 7)]
        import bisect
        for kid in kids:
            btree_inner.set_kid(kid)
        buffer = btree_inner.serialize()
        assert len(buffer) == Index.BTree.calculate_size(fanout)
        header, keys_count, keys, kid_ids = Index.BTree.deserialize(buffer)
        assert header == Index.TreeHeader
        assert keys == btree_inner.keys
        assert kids == btree_inner.kids
        assert kid_ids == [kid.id for kid in btree_inner._kids]

    def test_leaf_tree_serialization_success(self):
        locale.getpreferredencoding = lambda: 'utf-8'
        btree_leaf = Index.BTreeLeaf(0,
                                     4,
                                     keys=['Key1သည်', 'Key2山乇ㄥ', 'Key3етств', 'Key4ɹoʇıp', 'Key5ಠ益ಠ'],
                                     values=['Value1သည်', 'Value2山乇ㄥ', 'Value3етств', 'Value4ɹoʇıp', 'Value5ಠ益ಠ'])
        btree_leaf._kids = [Index.BTree(k, 4) for k in range(1, 6)]
        btree_leaf._prev_id = 1
        btree_leaf._next_id = 3
        buffer = btree_leaf.serialize()
        assert len(buffer) == Index.BTreeLeaf.calculate_size()
        header, keys_count, keys, values, kids, prev_id, next_id = Index.BTreeLeaf.deserialize(buffer)
        assert header == Index.TreeHeader
        assert prev_id == 1
        assert next_id == 3
        assert keys == btree_leaf._keys
        assert values == btree_leaf._values
        assert kids == [kid.id for kid in btree_leaf._kids]

    def test_tree_calculate_offset_success(self):
        offset = Index.calculate_offset(0)
        assert offset == Index.HeaderSize
        offset = Index.calculate_offset(1)
        assert offset == Index.HeaderSize + Index.BTree.calculate_size()
        offset = Index.calculate_offset(2)
        assert offset == Index.HeaderSize + 2 * Index.BTree.calculate_size()

    def test_inner_tree_load_save_success(self):
        btree_inner = Index.BTree(0, 4, keys=['Key1သည်', 'Key2山乇ㄥ', 'Key3етств', 'Key4ɹoʇıp', 'Key5ಠ益ಠ'])
        btree_inner._kids = [Index.BTree(k, 4) for k in range(1, 7)]
        repository = InMemoryRepository(512)
        index = Index(repository)
        index.save_tree(btree_inner)
        btree = index.load_tree(btree_inner.id)
        assert btree == btree_inner

    def test_leaf_tree_load_save_success(self):
        locale.getpreferredencoding = lambda: 'utf-8'
        btree_leaf = Index.BTreeLeaf(0,
                                     4,
                                     keys=['Key1သည်', 'Key2山乇ㄥ', 'Key3етств', 'Key4ɹoʇıp', 'Key5ಠ益ಠ'],
                                     values=['Value1သည်', 'Value2山乇ㄥ', 'Value3етств', 'Value4ɹoʇıp', 'Value5ಠ益ಠ'])
        btree_leaf._kids = [Index.BTree(k, 4) for k in range(1, 6)]
        btree_leaf._prev_id = 1
        btree_leaf._next_id = 3
        repository = InMemoryRepository(512)
        index = Index(repository)
        index.save_tree(btree_leaf)
        btree = index.load_tree(btree_leaf.id, leaf=True)
        assert btree == btree_leaf

    def test_search_key_success(self):
        keys = sorted(['one', 'Keyသည်', 'Key山乇ㄥ', 'Keyетств', 'Keyɹoʇıp', 'Keyಠ益ಠ'])
        assert Index.search_key('one', keys) == 5
        assert Index.search_key('Keyသည်', keys) == 3
        assert Index.search_key('Key山乇ㄥ', keys) == 4
        assert Index.search_key('Keyетств', keys) == 1
        assert Index.search_key('Keyɹoʇıp', keys) == 0
        assert Index.search_key('Keyಠ益ಠ', keys) == 2
        assert Index.search_key('test', keys) == -1

    def test_search_key_partial_success(self):
        keys = sorted(['one', 'Keyသည်', 'Key山乇ㄥ', 'Keyетств', 'Keyɹoʇıp', 'Keyಠ益ಠ', 'z', 'z'])
        assert Index.search_key('one', keys, hi=5) == 5
        assert Index.search_key('Keyသည်', keys, hi=5) == 3
        assert Index.search_key('Key山乇ㄥ', keys, hi=5) == 4
        assert Index.search_key('Keyетств', keys, hi=5) == 1
        assert Index.search_key('Keyɹoʇıp', keys, hi=5) == 0
        assert Index.search_key('Keyಠ益ಠ', keys, hi=5) == 2
        assert Index.search_key('test', keys, hi=5) == -1

    def test_search_key_random_success(self):
        count = 1000
        keys = sorted([Text.generate_random_string(k) for k in range(0, count)])
        for k in range(1, len(keys)):
            key_index = random.randint(0, len(keys) - 1)
            assert Index.search_key(keys[key_index], keys) != -1

    def test_search_key_position_success(self):
        keys = []
        assert Index.search_key_position('a', keys) == 0
        keys = [None]
        assert Index.search_key_position('a', keys) == 1
        keys = [None, None]
        assert Index.search_key_position('a', keys) == 2
        keys = [None, None, None, 'a', 'b']
        assert Index.search_key_position('a', keys) == 4
        keys = [None, None, None, 'b']
        assert Index.search_key_position('a', keys) == 3
        keys = sorted(['one', 'Keyသည်', 'Key山乇ㄥ', 'Keyетств', 'Keyɹoʇıp', 'Keyಠ益ಠ'])
        assert Index.search_key_position('one', keys) == 6
        assert Index.search_key_position('Keyသည်', keys) == 4
        assert Index.search_key_position('Key山乇ㄥ', keys) == 5
        assert Index.search_key_position('Keyетств', keys) == 2
        assert Index.search_key_position('Keyɹoʇıp', keys) == 1
        assert Index.search_key_position('Keyಠ益ಠ', keys) == 3
        assert Index.search_key_position('test', keys) == 6

    def test_search_key_position_desc_success(self):
        keys = []
        assert Index.search_key_position('a', keys, desc=True) == 0
        keys = [None]
        assert Index.search_key_position('a', keys, desc=True) == 0
        keys = [None, None]
        assert Index.search_key_position('a', keys, desc=True) == 0
        keys = ['a', 'b', None, None, None]
        assert Index.search_key_position('a', keys, desc=True) == 1
        keys = ['b', None, None, None]
        assert Index.search_key_position('a', keys, desc=True) == 0
        keys = sorted(['one', 'Keyသည်', 'Key山乇ㄥ', 'Keyетств', 'Keyɹoʇıp', 'Keyಠ益ಠ'])
        assert Index.search_key_position('one', keys, desc=True) == 6
        assert Index.search_key_position('Keyသည်', keys, desc=True) == 4
        assert Index.search_key_position('Key山乇ㄥ', keys, desc=True) == 5
        assert Index.search_key_position('Keyетств', keys, desc=True) == 2
        assert Index.search_key_position('Keyɹoʇıp', keys, desc=True) == 1
        assert Index.search_key_position('Keyಠ益ಠ', keys, desc=True) == 3
        assert Index.search_key_position('test', keys, desc=True) == 6

    def test_search_key_position_partial_success(self):
        keys = sorted(['one', 'Keyသည်', 'Key山乇ㄥ', 'Keyетств', 'Keyɹoʇıp', 'Keyಠ益ಠ', 'z', 'z'])
        keys[6] = None
        keys[7] = None
        assert Index.search_key_position('one', keys, hi=6) == 6
        assert Index.search_key_position('Keyသည်', keys, hi=6) == 4
        assert Index.search_key_position('Key山乇ㄥ', keys, hi=6) == 5
        assert Index.search_key_position('Keyетств', keys, hi=6) == 2
        assert Index.search_key_position('Keyɹoʇıp', keys, hi=6) == 1
        assert Index.search_key_position('Keyಠ益ಠ', keys, hi=6) == 3
        assert Index.search_key_position('test', keys, hi=6) == 6

    def test_set_key_partial_success(self):
        keys = sorted(['one', 'Keyသည်', 'Key山乇ㄥ', 'Keyетств', 'Keyɹoʇıp', 'Keyಠ益ಠ', 'z', 'z'])
        keys[6] = None
        keys[7] = None
        assert Index.set_key('one', keys, hi=6) == 6
        assert Index.set_key('Keyသည်', keys, hi=6) == 4
        assert Index.set_key('Key山乇ㄥ', keys, hi=6) == 5
        assert Index.set_key('Keyетств', keys, hi=6) == 2
        assert Index.set_key('Keyɹoʇıp', keys, hi=6) == 1
        assert Index.set_key('Keyಠ益ಠ', keys, hi=6) == 3
        assert keys == ['Keyɹoʇıp', 'Keyɹoʇıp', 'Keyетств', 'Keyಠ益ಠ', 'Keyသည်', 'Key山乇ㄥ', 'one', None]

    def test_insert_key_success(self):
        keys = [None]
        keys, position = Index.insert_key('a', keys)
        assert keys, position == (['a'], 0)
        keys = [None, None]
        assert Index.insert_key('a', keys) == (['a', None], 0)
        keys = [None, None, None]
        assert Index.insert_key('a', keys) == (['a', None, None], 0)
        keys = ['a', None, None, None]
        assert Index.insert_key('a', keys) == (['a', 'a', None, None], 1)
        keys = ['a', 'b', None, None, None]
        assert Index.insert_key('a', keys) == (['a', 'a', 'b', None, None], 1)
        keys = ['a', 'b', 'c', None]
        assert Index.insert_key('b', keys) == (['a', 'b', 'b', 'c'], 2)
        keys = ['a', 'b', 'c']
        assert Index.insert_key('b', keys) == (['a', 'b', 'b'], 2)
        keys = ['a', 'b', None, None, None]
        assert Index.insert_key('a', keys, hi=3) == (['a', 'a', 'b', None, None], 1)


if __name__ == '__main__':
    """
    """
    unittest.main()
