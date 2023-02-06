# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
"""  B-Tree based Index implementation """
import struct
from collections import namedtuple
from enum import IntEnum
from functools import lru_cache

from graph.core.domain_helper import DomainHelper
from graph.core.text import Text
from graph.adt.tree import Tree
from graph.core.entity import Entity


class Index(Entity):
    """
    """
    M = 12  # inner node order or branching factor, also fanout factor (number of kids to child nodes)
    L = 6  # leaf node order, kvp
    Endianness = '<'
    Header = 'AA'  # index header, common preamble of the index
    HeaderSize = 64  # bytes
    TreeHeader = 'AA'  # tree/record header
    TreeHeaderSize = 28  # bytes
    KeySize = 36  # bytes
    ValueSize = 56  # bytes
    PtrSize = 4  # bytes, integer
    Kvp = namedtuple('Kvp', 'key value')

    def __init__(self,
                 repository,
                 fanout=M,
                 id=0,
                 label='',
                 version='1.0'):
        """
        """
        super().__init__(id, version)
        self._label = label
        self._repository = repository
        self._fanout = fanout
        self._root = None
        self._number_of_nodes = 0

    def __repr__(self):
        """
        """
        return f"{type(self).__name__}:{self._id}:{self._label}:{self._version}"

    __str__ = __repr__

    def __hash__(self):
        """
        """
        result = super().__hash__()
        result ^= hash(self._label)
        return result

    def __eq__(self, other):
        """
        """
        result = super().__eq__(other) and Text.equal(self._label, other.label)
        return result

    def __lt__(self, other):
        """
        """
        result = (super().__lt__(other) and
                  self._label < other.label)
        return result

    def __le__(self, other):
        """
        """
        result = (super().__le__(other) and
                  self._label <= other.label)
        return result

    class BTree(Tree):
        """
        """

        def __init__(self,
                     id,
                     fanout,
                     keys=None,
                     kid_ids=None,
                     version='1.0'):
            """
            """
            super().__init__(id, version)
            self._fanout = fanout
            self._keys = [key for key in keys] if keys else [None] * fanout  # list of keys
            self._kid_ids = [id for id in kid_ids] if kid_ids else [0] * fanout  # list of kid ids for io

        def __repr__(self):
            """
            """
            return f"{type(self).__name__}"

        __str__ = __repr__

        def __hash__(self):
            """
            """
            return super().__hash__()

        def __eq__(self, other):
            """
            """
            return super().__eq__(other)

        def __lt__(self, other):
            """
            """
            return super().__lt__(other)

        @property
        def keys(self):
            """
            """
            return self._keys

        def __le__(self, other):
            """
            """
            return super().__le__(other)

        def validate(self):
            """
            """
            pass

        def accept(self, visitor, *args, **kwargs):
            """
            """
            pass

        @staticmethod
        @lru_cache
        def calculate_size():
            """
            """
            result = Index.TreeHeaderSize
            result += (Index.M + 1) * Index.PtrSize
            result += Index.M * Index.KeySize
            return result

        @staticmethod
        def get_count_pack_template():
            """
            """
            count_template = f"I"
            return count_template

        @staticmethod
        def get_address_pack_template():
            """
            """
            address_template = f"Q"
            return address_template

        @staticmethod
        def get_string_pack_template(string, string_size, string_bytes_len=0):
            """
            """
            string_bytes_len = len(bytes(string, 'utf-8')) if string else string_bytes_len
            count_template = Index.BTree.get_count_pack_template()
            string_template = f"{string_bytes_len}s"
            padding_size = max(0, string_size - struct.calcsize(count_template) - struct.calcsize(string_template))
            string_template = f"{count_template}{string_template}{padding_size}x"
            assert struct.calcsize(string_template) == string_size, "Invalid pack template. Size mismatch."
            if not string:
                string_template = string_template[1:]
            return string_template

        @staticmethod
        def get_header_pack_template(header, header_size):
            """
            """
            count_template = Index.BTree.get_count_pack_template()
            count_template_size = struct.calcsize(count_template)
            header_template = f"{Index.BTree.get_string_pack_template(header, header_size - count_template_size)}"
            header_template += count_template
            assert struct.calcsize(header_template) == Index.TreeHeaderSize
            return header_template

        @staticmethod
        def calculate_buffer_size(header, header_size, kids, keys, key_size):
            """
            """
            header_template = Index.BTree.get_header_pack_template(header, header_size)
            core_template = f"{header_template}{len(kids)}I"
            keys_template = ""
            for key in keys:
                keys_template += Index.BTree.get_string_pack_template(key, key_size)
            return struct.calcsize(core_template) + struct.calcsize(keys_template)

        def serialize(self):
            """
            TreeHeader | Pn | P(0) | ... | P(i-1) | P(i) | Kn | K(0) | ... | K(i-1)
            TreeHeader: ... | len(P) | ...
            P - kid pointer id, K - key.
            """
            kids = [kid.id for kid in self._kids]
            buffer_size = Index.BTree.calculate_buffer_size(Index.TreeHeader,
                                                            Index.TreeHeaderSize,
                                                            kids,
                                                            self._keys,
                                                            Index.KeySize)
            offset = 0
            buffer = bytearray(buffer_size)
            header_template = f"{Index.Endianness}" \
                              f"{Index.BTree.get_header_pack_template(Index.TreeHeader, Index.TreeHeaderSize)}"
            header_bytes = bytes(Index.TreeHeader, 'utf-8')
            struct.pack_into(header_template,
                             buffer,
                             offset,
                             len(header_bytes),
                             header_bytes,
                             len(kids))
            offset = struct.calcsize(header_template)
            kids_template = f"{len(kids)}I"
            struct.pack_into(kids_template, buffer, offset, *kids)
            offset += struct.calcsize(kids_template)
            for key in self._keys:
                key_template = f"{Index.Endianness}{Index.BTree.get_string_pack_template(key, Index.KeySize)}"
                key_template_size = struct.calcsize(key_template)
                assert key_template_size == Index.KeySize
                key_bytes = bytes(key, 'utf-8')
                struct.pack_into(key_template, buffer, offset, len(key_bytes), key_bytes)
                offset += key_template_size
            padding_size = Index.BTree.calculate_size() - len(buffer)
            buffer.extend(b'\x00' * padding_size)
            return buffer

        @staticmethod
        def deserialize(buffer):
            """
            """
            offset = 0
            header_template = f"{Index.Endianness}" \
                              f"{Index.BTree.get_header_pack_template(Index.TreeHeader, Index.TreeHeaderSize)}"
            _, header, kids_count, *tail = struct.unpack_from(header_template, buffer, 0)
            header = header.decode('utf-8').strip()
            assert Text.equal(header, Index.TreeHeader), "Invalid header. Content mismatch."
            offset += struct.calcsize(header_template)
            kids_template = f"{Index.Endianness}{kids_count}I"
            kids = struct.unpack_from(kids_template, buffer, offset)
            kids = list(kids)
            assert len(kids) == kids_count, "Invalid kids. Size mismatch."
            offset += struct.calcsize(kids_template)
            keys_count = kids_count - 1
            count_template = f"{Index.Endianness}{Index.BTree.get_count_pack_template()}"
            count_size = struct.calcsize(count_template)
            keys = list()
            for _ in range(keys_count):
                key_bytes_len, *tail = struct.unpack_from(count_template, buffer, offset)
                offset += count_size
                key_template = f"{Index.Endianness}" \
                               f"{Index.BTree.get_string_pack_template(None, Index.KeySize, key_bytes_len)}"
                key_size = struct.calcsize(key_template)
                key, *tail = struct.unpack_from(key_template, buffer, offset)
                key = key.decode('utf-8').strip()
                keys.append(key)
                offset += key_size
            assert len(keys) == keys_count, "Invalid keys. Size mismatch."
            return header, keys, kids

    class BTreeLeaf(BTree):
        """
        """

        def __init__(self,
                     id,
                     fanout,
                     keys=None,
                     values=None,
                     kid_ids=None,
                     prev_id=0,
                     next_id=0,
                     version='1.0'):
            """
            """
            super().__init__(id, fanout, keys=keys, kid_ids=kid_ids, version=version)
            self._values = [value for value in values] if values else [None] * fanout  # list of values
            self._prev = None  # leaf node links
            self._prev_id = prev_id
            self._next = None
            self._next_id = next_id

        def __repr__(self):
            """
            """
            return f"{type(self).__name__}"

        __str__ = __repr__

        def __hash__(self):
            """
            """
            return super().__hash__()

        def __eq__(self, other):
            """
            """
            return super().__eq__(other)

        def __lt__(self, other):
            """
            """
            return super().__lt__(other)

        def __le__(self, other):
            """
            """
            return super().__le__(other)

        @property
        def values(self):
            """
            """
            return self._values

        @property
        def prev(self):
            """
            """
            return self._prev

        @property
        def next(self):
            """
            """
            return self._next

        def validate(self):
            """
            """
            pass

        def accept(self, visitor, *args, **kwargs):
            """
            """
            pass

        @staticmethod
        def get_header_pack_template(header, header_size):
            """
            """
            count_template = Index.BTree.get_count_pack_template()
            count_template_size = struct.calcsize(count_template)
            header_template = f"{Index.BTree.get_string_pack_template(header, header_size - 3 * count_template_size)}"
            header_template += f"3{count_template}"
            assert struct.calcsize(header_template) == Index.TreeHeaderSize
            return header_template

        @staticmethod
        def calculate_leaf_buffer_size(header, header_size, kids, keys, key_size, values, value_size):
            """
            """
            header_template = Index.BTreeLeaf.get_header_pack_template(header, header_size)
            core_template = f"{header_template}{len(kids)}I"
            keys_template = ""
            for key in keys:
                keys_template += Index.BTree.get_string_pack_template(key, key_size)
            values_template = ""
            for value in values:
                values_template += Index.BTree.get_string_pack_template(value, value_size)
            return struct.calcsize(core_template) + struct.calcsize(keys_template) + struct.calcsize(values_template)

        def serialize(self):
            """
            TreeHeader | Pn | P(0) | ... | P(i-1) | P(i) | KVPn | KVP(0) | ... | KVP(i-1)
            TreeHeader: ... | Prev | Next | len(P) | ...
            P - kid pointer id, KVP - key:value pair.
            """
            kids = [kid.id for kid in self._kids]
            buffer_size = Index.BTreeLeaf.calculate_leaf_buffer_size(Index.TreeHeader,
                                                                     Index.TreeHeaderSize,
                                                                     kids,
                                                                     self._keys,
                                                                     Index.KeySize,
                                                                     self._values,
                                                                     Index.ValueSize)
            offset = 0
            buffer = bytearray(buffer_size)
            header_template = f"{Index.Endianness}" \
                              f"{Index.BTreeLeaf.get_header_pack_template(Index.TreeHeader, Index.TreeHeaderSize)}"
            header_bytes = bytes(Index.TreeHeader, 'utf-8')
            struct.pack_into(header_template,
                             buffer,
                             offset,
                             len(header_bytes),
                             header_bytes,
                             self._prev_id,
                             self._next_id,
                             len(kids))
            offset = struct.calcsize(header_template)
            kids_template = f"{len(kids)}I"
            struct.pack_into(kids_template, buffer, offset, *kids)
            offset += struct.calcsize(kids_template)
            for kvp in zip(self._keys, self._values):
                key, value = kvp
                key_template = f"{Index.Endianness}{Index.BTree.get_string_pack_template(key, Index.KeySize)}"
                key_template_size = struct.calcsize(key_template)
                assert key_template_size == Index.KeySize
                key_bytes = bytes(key, 'utf-8')
                struct.pack_into(key_template, buffer, offset, len(key_bytes), key_bytes)
                offset += key_template_size
                value_template = f"{Index.Endianness}{Index.BTree.get_string_pack_template(value, Index.ValueSize)}"
                value_template_size = struct.calcsize(value_template)
                assert value_template_size == Index.ValueSize
                value_bytes = bytes(value, 'utf-8')
                struct.pack_into(value_template, buffer, offset, len(value_bytes), value_bytes)
                offset += value_template_size
            padding_size = Index.BTree.calculate_size() - len(buffer)
            buffer.extend(b'\x00' * padding_size)
            return buffer

        @staticmethod
        def deserialize(buffer):
            """
            """
            offset = 0
            header_template = f"{Index.Endianness}" \
                              f"{Index.BTreeLeaf.get_header_pack_template(Index.TreeHeader, Index.TreeHeaderSize)}"
            _, header, prev_id, next_id, kids_count, *tail = struct.unpack_from(header_template, buffer, 0)
            header = header.decode('utf-8').strip()
            assert Text.equal(header, Index.TreeHeader), "Invalid header. Content mismatch."
            offset += struct.calcsize(header_template)
            kids_template = f"{Index.Endianness}{kids_count}I"
            kids = struct.unpack_from(kids_template, buffer, offset)
            kids = list(kids)
            assert len(kids) == kids_count, "Invalid kids. Size mismatch."
            offset += struct.calcsize(kids_template)
            keys_count = kids_count - 1
            values_count = kids_count - 1
            count_template = f"{Index.Endianness}{Index.BTree.get_count_pack_template()}"
            count_size = struct.calcsize(count_template)
            keys = list()
            values = list()
            for _ in range(keys_count):
                key_bytes_len, *tail = struct.unpack_from(count_template, buffer, offset)
                offset += count_size
                key_template = f"{Index.Endianness}" \
                               f"{Index.BTree.get_string_pack_template(None, Index.KeySize, key_bytes_len)}"
                key_size = struct.calcsize(key_template)
                key, *tail = struct.unpack_from(key_template, buffer, offset)
                key = key.decode('utf-8').strip()
                keys.append(key)
                offset += key_size
                value_bytes_len, *tail = struct.unpack_from(count_template, buffer, offset)
                offset += count_size
                value_template = f"{Index.Endianness}" \
                                 f"{Index.BTree.get_string_pack_template(None, Index.ValueSize, value_bytes_len)}"
                value_size = struct.calcsize(value_template)
                value, *tail = struct.unpack_from(value_template, buffer, offset)
                value = value.decode('utf-8').strip()
                values.append(value)
                offset += value_size
            assert len(keys) == keys_count, "Invalid keys. Size mismatch."
            assert len(values) == values_count, "Invalid values. Size mismatch."
            return header, keys, values, kids, prev_id, next_id

    def create(self):
        """
        """
        pass

    def search(self, key):
        """
        """
        pass

    def insert(self, key, value):
        """
        """
        pass

    def load(self, kvps):
        """
        """
        pass

    def remove(self, key):
        """
        """
        pass

    def save_tree(self, tree):
        """
        """
        offset = Index.calculate_offset(tree.id)
        buffer = tree.serialize()
        self._repository.write(offset, buffer)

    def load_tree(self, id, leaf=False):
        """
        """
        offset = Index.calculate_offset(id)
        size = Index.BTree.calculate_size()
        buffer = self._repository.read(offset, size)
        if leaf:
            header, keys, values, kids, prev_id, next_id = Index.BTreeLeaf.deserialize(buffer)
            result = Index.BTreeLeaf(id, Index.M, keys, values, kids, prev_id, next_id)
        else:
            header, keys, kids = Index.BTree.deserialize(buffer)
            result = Index.BTree(id, Index.M, keys, kids)
        return result

    @staticmethod
    def calculate_offset(id):
        offset = Index.HeaderSize
        offset += id * Index.BTree.calculate_size()
        return offset
