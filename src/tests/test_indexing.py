#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import random
import unittest
import locale
from graph.core.domain_helper import DomainHelper
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
        btree_inner = Index.BTree(0, 4)
        btree_inner._keys = ['Key1သည်', 'Key2山乇ㄥ', 'Key3етств', 'Key4ɹoʇıp', 'Key5ಠ益ಠ']
        btree_inner._kids = [Index.BTree(k, 4) for k in range(1, 7)]
        buffer = btree_inner.serialize()
        assert len(buffer) == Index.BTree.calculate_size()
        header, keys, kids = Index.BTree.deserialize(buffer)
        assert header == Index.TreeHeader
        assert keys == btree_inner._keys
        assert kids == [kid.id for kid in btree_inner._kids]

    def test_leaf_tree_serialization_success(self):
        locale.getpreferredencoding = lambda: 'utf-8'
        btree_leaf = Index.BTreeLeaf(0, 4)
        btree_leaf._kids = [Index.BTree(k, 4) for k in range(1, 7)]
        btree_leaf._keys = ['Key1သည်', 'Key2山乇ㄥ', 'Key3етств', 'Key4ɹoʇıp', 'Key5ಠ益ಠ']
        btree_leaf._values = ['Value1သည်', 'Value2山乇ㄥ', 'Value3етств', 'Value4ɹoʇıp', 'Value5ಠ益ಠ']
        btree_leaf._prev_id = 1
        btree_leaf._next_id = 3
        buffer = btree_leaf.serialize()
        assert len(buffer) == Index.BTreeLeaf.calculate_size()
        header, keys, values, kids, prev_id, next_id = Index.BTreeLeaf.deserialize(buffer)
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
        btree_inner = Index.BTree(0, 4)
        btree_inner._keys = ['Key1သည်', 'Key2山乇ㄥ', 'Key3етств', 'Key4ɹoʇıp', 'Key5ಠ益ಠ']
        btree_inner._kids = [Index.BTree(k, 4) for k in range(1, 7)]
        repository = InMemoryRepository(512)
        index = Index(repository)
        index.save_tree(btree_inner)
        btree = index.load_tree(btree_inner.id)
        assert btree == btree_inner

    def test_leaf_tree_load_save_success(self):
        locale.getpreferredencoding = lambda: 'utf-8'
        btree_leaf = Index.BTreeLeaf(0, 4)
        btree_leaf._kids = [Index.BTree(k, 4) for k in range(1, 7)]
        btree_leaf._keys = ['Key1သည်', 'Key2山乇ㄥ', 'Key3етств', 'Key4ɹoʇıp', 'Key5ಠ益ಠ']
        btree_leaf._values = ['Value1သည်', 'Value2山乇ㄥ', 'Value3етств', 'Value4ɹoʇıp', 'Value5ಠ益ಠ']
        btree_leaf._prev_id = 1
        btree_leaf._next_id = 3
        repository = InMemoryRepository(512)
        index = Index(repository)
        index.save_tree(btree_leaf)
        btree = index.load_tree(btree_leaf.id, leaf=True)
        assert btree == btree_leaf


if __name__ == '__main__':
    """
    """
    unittest.main()
