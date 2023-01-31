#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import random
import unittest
from graph.core.domain_helper import DomainHelper
from graph.btrees.btree_memory_repository import BTreeInMemoryRepository


class Test(unittest.TestCase):
    def test_btree_in_memory_repository_init_success(self):
        for n in range(1, 127):
            page_size = n
            repository = BTreeInMemoryRepository(page_size)
            data_to_write = bytearray([k + 1 for k in range(page_size)])
            print([str(ch) for ch in data_to_write])
            repository.write(0, data_to_write)
            read_data = repository.read(0, len(data_to_write))
            assert data_to_write == read_data

    def test_btree_in_memory_repository_access_success(self):
        for n in range(1, 127):
            page_size = n
            repository = BTreeInMemoryRepository(page_size)
            data_to_write = bytearray([k + 1 for k in range(2 * page_size - 1)])
            print([str(ch) for ch in data_to_write])
            repository.write(10, data_to_write)
            read_data = repository.read(10, len(data_to_write))
            assert data_to_write == read_data

    def test_btree_in_memory_repository_page_access_random_success(self):
        for n in range(1, 10000):
            page_size = random.randint(1, 4097)
            data_count = random.randint(1, page_size)
            data_count = data_count * 2 if data_count % 2 == 0 else data_count
            data_count = data_count - 1 if data_count % 5 == 0 else data_count
            offset = random.randint(0, page_size)
            repository = BTreeInMemoryRepository(page_size)
            data_to_write = bytearray()
            for chunk in range(1, data_count // 256):
                data_to_write.extend([k + 1 for k in range(chunk)])
            data_to_write.extend([k + 1 for k in range(data_count % 256)])
            if page_size < 128:
                print([str(ch) for ch in data_to_write])
            repository.write(offset, data_to_write)
            read_data = repository.read(offset, len(data_to_write))
            assert data_to_write == read_data

    def test_btree_in_memory_repository_pages_access_random_success(self):
        for n in range(1, 10000):
            page_size = random.randint(1, 4097)
            data_count = random.randint(1, page_size * 16)
            data_count = data_count * 2 if data_count % 2 == 0 else data_count
            data_count = data_count - 1 if data_count % 5 == 0 else data_count
            offset = random.randint(0, page_size)
            repository = BTreeInMemoryRepository(page_size)
            data_to_write = bytearray()
            for chunk in range(1, data_count // 256):
                data_to_write.extend([k for k in range(256)])
            data_to_write.extend([k for k in range(data_count % 256)])
            repository.write(offset, data_to_write)
            read_data = repository.read(offset, len(data_to_write))
            assert data_to_write == read_data

    def test_btree_in_memory_repository_random_success(self):
        for n in range(1, 10000):
            page_size = random.randint(1, random.randint(2049, 65636))
            data_count = random.randint(1, page_size * 16)
            data_count = data_count * 2 if data_count % 2 == 0 else data_count
            data_count = data_count - 1 if data_count % 5 == 0 else data_count
            offset = random.randint(0, page_size)
            repository = BTreeInMemoryRepository(page_size)
            data_to_write = DomainHelper.generate_random_bytes(data_count)
            for chunk in range(1, data_count // 256):
                data_to_write.extend([k for k in range(256)])
            data_to_write.extend([k for k in range(data_count % 256)])
            repository.write(offset, data_to_write)
            read_data = repository.read(offset, len(data_to_write))
            assert data_to_write == read_data


if __name__ == '__main__':
    """
    """
    unittest.main()
