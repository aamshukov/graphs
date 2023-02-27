# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
"""  B-Tree based Index implementation """
import math
import struct
from collections import namedtuple
from functools import lru_cache
from graph.core.text import Text
from graph.adt.tree import Tree
from graph.core.entity import Entity


class Index(Entity):
    """
    """
    M = 12  # inner node order or branching factor, also fanout factor (number of keys)
    L = 6  # leaf node order, kvp
    Endianness = '<'
    Header = 'AA'  # index header, common preamble of the index
    HeaderSize = 64  # bytes
    TreeHeader = 'AA 1.0.0'  # tree/record header
    TreeHeaderSize = 28  # bytes
    KeySize = 36  # bytes
    ValueSize = 56  # bytes
    PtrSize = 4  # bytes, integer
    Kvp = namedtuple('Kvp', 'key value')
    Counter = 0

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
        self._height = 0
        self._number_of_branches = 0
        self._number_of_leaves = 0

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

    @property
    def fanout(self):
        """
        """
        return self._fanout

    @property
    def root(self):
        """
        """
        return self._root

    @property
    def height(self):
        """
        """
        return self._height

    @property
    def number_of_branches(self):
        """
        """
        return self._number_of_branches

    @property
    def number_of_leaves(self):
        """
        """
        return self._number_of_leaves

    @property
    def number_of_nodes(self):
        """
        """
        return self._number_of_branches + self._number_of_leaves

    @staticmethod
    def get_next_id():
        """
        """
        Index.Counter += 1
        return Index.Counter

    class BTreeBranch(Tree):
        """
        """

        def __init__(self,
                     id,
                     fanout,
                     version='1.0'):
            """
            """
            super().__init__(id, version)
            self._fanout = fanout
            self._keys = [None] * fanout  # list of keys
            self._keys_count = 0  # occupancy, number of keys currently stored
            self._kids = [None] * (fanout + 1)  # list of kids
            self._kid_ids = [0] * (fanout + 1)  # list of kid ids for i/o

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

        def full(self):
            """
            """
            return self._keys_count == self._fanout

        @property
        def keys(self):
            """
            """
            return self._keys

        def set_key(self, key, position):
            """
            """
            assert position < len(self._keys), "Invalid position."
            self._keys[position] = key
            self._keys_count = sum(k is not None for k in self._keys)

        def remove_key(self, position):
            """
            """
            assert position < len(self._keys), "Invalid position."
            self._keys[position] = None
            self._keys_count = sum(k is not None for k in self._keys)

        def search_key(self, key, lo=0, hi=None):
            """
            """
            assert key is not None, "Key must be non None."

            def binary_search(_key, _keys, _lo=0, _hi=None):
                result = -1
                if _hi is None:
                    _hi = len(_keys) - 1
                while _lo <= _hi:
                    mid = (_hi + _lo) // 2
                    cmp = Text.compare(_key, _keys[mid])
                    if cmp > 0:
                        _lo = mid + 1
                    elif cmp < 0:
                        _hi = mid - 1
                    else:
                        result = mid
                        break
                return result

            return binary_search(key, self._keys, lo, hi)

        def search_key_position(self, key, lo=0, hi=None, desc=False):
            """
            """
            assert key is not None, "Key must be non None."

            def locate(_key, _keys, _lo=0, _hi=None):
                if _hi is None:
                    _hi = len(_keys)
                while _lo < _hi:
                    mid = (_hi + _lo) // 2
                    if _keys[mid] is None:
                        cmp = -1 if desc else 1  # None is always less/bigger than key
                    else:
                        cmp = Text.compare(_key, _keys[mid])
                    if cmp < 0:
                        _hi = mid
                    else:
                        _lo = mid + 1
                return _lo

            return locate(key, self._keys, lo, hi)

        def insert_key(self, key, lo=0, hi=None):
            """
            Inserts key to the right of the found position (handles duplicates).
            hi should be _keys_count + 1, + 1 to include the next slot in keys.
            """
            if hi is None:
                hi = len(self._keys)
            position = self.search_key_position(key, lo, hi, desc=True)
            assert position < hi, "Invalid position calculated."
            for k in range(hi - 1, position, -1):
                self._keys[k] = self._keys[k - 1]
            self._keys[position] = key
            self._keys_count = sum(k is not None for k in self._keys)
            return self._keys, position

        def shift_kids_right(self, position):
            """
            """
            for k in range(len(self._kids) - 1, position, -1):
                self._kids[k] = self._kids[k - 1]
                self._kid_ids[k] = self._kid_ids[k - 1]

        def set_kid(self, kid, position):
            """
            """
            assert kid is not None, "Invalid kid."
            assert position < len(self._kids), "Invalid position."
            self._kids[position] = kid
            self._kid_ids[position] = kid.id

        def remove_kid(self, position):
            """
            """
            assert position < len(self._kids), "Invalid position."
            self._kids[position] = None
            self._kid_ids[position] = 0

        @property
        def kid_ids(self):
            """
            """
            return self._kid_ids

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
        def calculate_size(fanout):
            """
            """
            result = Index.TreeHeaderSize
            result += fanout * Index.KeySize
            result += (fanout + 1) * Index.PtrSize
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
            string_bytes_len = len(bytes(string, 'utf-8')) if not string_bytes_len else string_bytes_len
            count_template = Index.BTreeBranch.get_count_pack_template()
            string_template = f"{string_bytes_len}s"
            padding_size = max(0, string_size - struct.calcsize(count_template) - struct.calcsize(string_template))
            string_template = f"{count_template}{string_template}{padding_size}x"
            assert struct.calcsize(string_template) == string_size, "Invalid pack template. Size mismatch."
            return string_template

        @staticmethod
        def get_header_pack_template(header, header_size):
            """
            """
            count_template = Index.BTreeBranch.get_count_pack_template()
            count_template_size = struct.calcsize(count_template)
            header_template = f"{Index.BTreeBranch.get_string_pack_template(header, header_size - 2 * count_template_size)}"
            header_template += f"2{count_template}"
            assert struct.calcsize(header_template) == Index.TreeHeaderSize
            return header_template

        @staticmethod
        def calculate_buffer_size(header, header_size, fanout, keys, key_size):
            """
            """
            header_template = Index.BTreeBranch.get_header_pack_template(header, header_size)
            core_template = f"{header_template}{fanout + 1}I"
            keys_template = ""
            for key in keys:
                key = '' if not key else key
                keys_template += Index.BTreeBranch.get_string_pack_template(key, key_size)
            return struct.calcsize(core_template) + struct.calcsize(keys_template)

        def serialize(self):
            """
            TreeHeader | P(0) | ... | P(i-1) | P(i) | Kn | K(0) | ... | K(i-1)
            TreeHeader: ... | Fanout | KeysCount
            P - kid pointer id, K - key.
            """
            buffer_size = Index.BTreeBranch.calculate_buffer_size(Index.TreeHeader,
                                                                  Index.TreeHeaderSize,
                                                                  self._fanout,
                                                                  self._keys,
                                                                  Index.KeySize)
            offset = 0
            buffer = bytearray(buffer_size)
            header_template = f"{Index.Endianness}" \
                              f"{Index.BTreeBranch.get_header_pack_template(Index.TreeHeader, Index.TreeHeaderSize)}"
            header_bytes = bytes(Index.TreeHeader, 'utf-8')
            struct.pack_into(header_template,
                             buffer,
                             offset,
                             len(header_bytes),
                             header_bytes,
                             self._fanout,
                             self._keys_count)
            offset = struct.calcsize(header_template)
            kids_count = self._fanout + 1
            kids_template = f"{kids_count}I"
            struct.pack_into(kids_template, buffer, offset, *self._kid_ids)
            offset += struct.calcsize(kids_template)
            for key in self._keys:
                key = '' if not key else key
                key_template = f"{Index.Endianness}{Index.BTreeBranch.get_string_pack_template(key, Index.KeySize)}"
                key_template_size = struct.calcsize(key_template)
                assert key_template_size == Index.KeySize
                key_bytes = bytes(key, 'utf-8')
                struct.pack_into(key_template, buffer, offset, len(key_bytes), key_bytes)
                offset += key_template_size
            padding_size = Index.BTreeBranch.calculate_size(self._fanout) - len(buffer)
            buffer.extend(b'\x00' * padding_size)
            return buffer

        @staticmethod
        def deserialize(buffer):
            """
            """
            offset = 0
            header_template = f"{Index.Endianness}" \
                              f"{Index.BTreeBranch.get_header_pack_template(Index.TreeHeader, Index.TreeHeaderSize)}"
            _, header, fanout, keys_count, *tail = struct.unpack_from(header_template, buffer, 0)
            header = header.decode('utf-8').strip()
            assert Text.equal(header, Index.TreeHeader), "Invalid header. Content mismatch."
            offset += struct.calcsize(header_template)
            kids_count = fanout + 1
            kids_template = f"{Index.Endianness}{kids_count}I"
            kids = struct.unpack_from(kids_template, buffer, offset)
            kids = list(kids)
            assert len(kids) == kids_count, "Invalid kids. Size mismatch."
            offset += struct.calcsize(kids_template)
            count_template = f"{Index.Endianness}{Index.BTreeBranch.get_count_pack_template()}"
            count_size = struct.calcsize(count_template)
            keys = list()
            for _ in range(keys_count):
                key_bytes_len, *tail = struct.unpack_from(count_template, buffer, offset)
                offset += count_size
                key_template = f"{Index.Endianness}" \
                               f"{Index.BTreeBranch.get_string_pack_template(None, Index.KeySize, key_bytes_len)}"
                key_template = key_template[2:]
                key_size = struct.calcsize(key_template)
                key, *tail = struct.unpack_from(key_template, buffer, offset)
                key = key.decode('utf-8').strip()
                keys.append(key)
                offset += key_size
            assert len(keys) == keys_count, "Invalid keys. Size mismatch."
            return header, keys_count, keys, kids

    class BTreeLeaf(BTreeBranch):
        """
        """

        def __init__(self,
                     id,
                     fanout,
                     version='1.0'):
            """
            """
            super().__init__(id, fanout, version=version)
            self._values = [None] * fanout  # list of values
            self._kids = None  # None for now, might be list of pointers to records
            self._kid_ids = None  # None for now, might be list of pointers to records
            self._prev = None  # leaf node links
            self._prev_id = 0
            self._next = None
            self._next_id = 0

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

        def full(self):
            """
            """
            return self._keys_count == self._fanout

        @property
        def values(self):
            """
            """
            return self._values

        def set_value(self, value, position):
            """
            """
            assert position < len(self._values), "Invalid position."
            self._values[position] = value

        def remove_value(self, position):
            """
            """
            assert position < len(self._values), "Invalid position."
            self._values[position] = None

        def insert_key_value(self, key, value, lo=0, hi=None):
            """
            Inserts key:value based on a key to the right of the found position (handles duplicates).
            hi should be _keys_count + 1, + 1 to include the next slot in keys.
            """
            if hi is None:
                hi = len(self._keys)
            position = self.search_key_position(key, lo, hi, desc=True)
            assert position < hi, "Invalid position calculated."
            for k in range(hi - 1, position, -1):
                self._keys[k] = self._keys[k - 1]
                self._values[k] = self._values[k - 1]
            self._keys[position] = key
            self._values[position] = value
            self._keys_count = sum(k is not None for k in self._keys)
            return self._keys, self._values, position

        @property
        def prev(self):
            """
            """
            return self._prev

        @prev.setter
        def prev(self, prev):
            """
            """
            self._prev = prev

        @property
        def prev_id(self):
            """
            """
            return self._prev_id

        @prev_id.setter
        def prev_id(self, id):
            """
            """
            self._prev_id = id

        @property
        def next(self):
            """
            """
            return self._next

        @next.setter
        def next(self, nxt):
            """
            """
            self._next = nxt

        @property
        def next_id(self):
            """
            """
            return self._next_id

        @next_id.setter
        def next_id(self, id):
            """
            """
            self._next_id = id

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
        def calculate_size(fanout):
            """
            """
            result = Index.TreeHeaderSize
            result += fanout * Index.KeySize
            result += fanout * Index.ValueSize
            # result += (fanout + 1) * Index.PtrSize
            return result

        @staticmethod
        def get_header_pack_template(header, header_size):
            """
            """
            count_template = Index.BTreeBranch.get_count_pack_template()
            count_template_size = struct.calcsize(count_template)
            header_template =\
                f"{Index.BTreeBranch.get_string_pack_template(header, header_size - 4 * count_template_size)}"
            header_template += f"4{count_template}"
            assert struct.calcsize(header_template) == Index.TreeHeaderSize
            return header_template

        @staticmethod
        def calculate_leaf_buffer_size(header, header_size, keys, key_size, values, value_size):
            """
            """
            header_template = Index.BTreeLeaf.get_header_pack_template(header, header_size)
            keys_template = ""
            for key in keys:
                key = '' if not key else key
                keys_template += Index.BTreeBranch.get_string_pack_template(key, key_size)
            values_template = ""
            for value in values:
                value = '' if not value else value
                values_template += Index.BTreeBranch.get_string_pack_template(value, value_size)
            return struct.calcsize(header_template) + struct.calcsize(keys_template) + struct.calcsize(values_template)

        def serialize(self):
            """
            TreeHeader | KVPn | KVP(0) | ... | KVP(i-1)
            TreeHeader: ... | Prev | Next | Fanout | KeysCount | ...
            P - data pointer id (overflow page), KVP - key:value pair.
            """
            buffer_size = Index.BTreeLeaf.calculate_leaf_buffer_size(Index.TreeHeader,
                                                                     Index.TreeHeaderSize,
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
                             self._fanout,
                             self._keys_count)
            offset = struct.calcsize(header_template)
            for kvp in zip(self._keys, self._values):
                key, value = kvp
                key = '' if not key else key
                key_template = f"{Index.Endianness}" \
                               f"{Index.BTreeBranch.get_string_pack_template(key, Index.KeySize)}"
                key_template_size = struct.calcsize(key_template)
                assert key_template_size == Index.KeySize
                key_bytes = bytes(key, 'utf-8')
                struct.pack_into(key_template, buffer, offset, len(key_bytes), key_bytes)
                offset += key_template_size
                value = '' if not value else value
                value_template = f"{Index.Endianness}{Index.BTreeBranch.get_string_pack_template(value, Index.ValueSize)}"
                value_template_size = struct.calcsize(value_template)
                assert value_template_size == Index.ValueSize
                value_bytes = bytes(value, 'utf-8')
                struct.pack_into(value_template, buffer, offset, len(value_bytes), value_bytes)
                offset += value_template_size
            padding_size = Index.BTreeLeaf.calculate_size(self._fanout) - len(buffer)
            buffer.extend(b'\x00' * padding_size)
            return buffer

        @staticmethod
        def deserialize(buffer):
            """
            """
            offset = 0
            header_template = f"{Index.Endianness}" \
                              f"{Index.BTreeLeaf.get_header_pack_template(Index.TreeHeader, Index.TreeHeaderSize)}"
            _, header, prev_id, next_id, fanout, keys_count, *tail = struct.unpack_from(header_template, buffer, 0)
            header = header.decode('utf-8').strip()
            assert Text.equal(header, Index.TreeHeader), "Invalid header. Content mismatch."
            values_count = keys_count
            offset += struct.calcsize(header_template)
            count_template = f"{Index.Endianness}{Index.BTreeBranch.get_count_pack_template()}"
            count_size = struct.calcsize(count_template)
            keys = list()
            values = list()
            for _ in range(keys_count):
                key_bytes_len, *tail = struct.unpack_from(count_template, buffer, offset)
                offset += count_size
                key_template = f"{Index.Endianness}" \
                               f"{Index.BTreeBranch.get_string_pack_template(None, Index.KeySize, key_bytes_len)}"
                key_template = key_template[2:]
                key_size = struct.calcsize(key_template)
                key, *tail = struct.unpack_from(key_template, buffer, offset)
                key = key.decode('utf-8').strip()
                keys.append(key)
                offset += key_size
                value_bytes_len, *tail = struct.unpack_from(count_template, buffer, offset)
                offset += count_size
                value_template = f"{Index.Endianness}" \
                                 f"{Index.BTreeBranch.get_string_pack_template(None, Index.ValueSize, value_bytes_len)}"
                value_template = value_template[2:]
                value_size = struct.calcsize(value_template)
                value, *tail = struct.unpack_from(value_template, buffer, offset)
                value = value.decode('utf-8').strip()
                values.append(value)
                offset += value_size
            assert len(keys) == keys_count, "Invalid keys. Size mismatch."
            assert len(values) == values_count, "Invalid values. Size mismatch."
            return header, keys_count, keys, values, prev_id, next_id

    def search(self, key):
        """
        """
        tree = None
        value = None
        position = 0
        return tree, value, position

    def create_branch(self):
        result = Index.BTreeBranch(Index.get_next_id(), self._fanout)
        self._number_of_branches += 1
        return result

    def create_leaf(self):
        result = Index.BTreeLeaf(Index.get_next_id(), self._fanout)
        self._number_of_leaves += 1
        return result

    def insert(self, key, value, replace=True):
        """
        """
        if not self._root:
            self._root = self.create_leaf()
            self.save_tree(self._root)
        root = self._root
        if root.full():
            new_root = self.create_branch()
            new_root.set_kid(root, 0)
            self._root = new_root
            self._height += 1
            self.split_branch(new_root, root)
            self.insert_non_full(new_root, key, value)
        else:
            self.insert_non_full(root, key, value)

    def insert_non_full(self, tree, key, value, level=0):
        """
        """
        leaf = level == self._height
        if leaf:
            tree.insert_key_value(key, value)
            self.save_tree(tree)
        else:
            position = tree.search_key(key) + 1
            kid = self.load_tree(tree.kids[position].id, leaf)
            if tree.full():
                if leaf:
                    _, kid, new_kid = self.split_leaf(tree, kid)
                else:
                    _, kid, new_kid = self.split_branch(tree, kid)
                cmp = Text.compare(key, tree.keys[position])
                if cmp > 0:  # which of the kids to proceed with - old or new one
                    tree = new_kid
                else:
                    tree = kid
            self.insert_non_full(tree, key, value, level + 1)

    def split_branch(self, papa, kid):
        """
        """
        keys_mid = int(math.floor(self._fanout / 2))
        kids_mid = int(math.floor((self._fanout + 1) / 2))
        new_kid = self.create_branch()
        for i, k in enumerate(range(keys_mid + 1, self._fanout)):  # +1 push up mid-key
            new_kid.set_key(kid.keys[k], i)
        for i, k in enumerate(range(kids_mid, self._fanout + 1)):
            new_kid.set_kid(kid.kids[k], i)
        mid_key = kid.keys[keys_mid]
        mid_key_position = papa.search_key_position(mid_key)
        for k in range(keys_mid, self._fanout):
            kid.remove_key(k)
        for k in range(kids_mid, self._fanout + 1):
            kid.remove_kid(k)
        papa.insert_key(mid_key, mid_key_position)
        papa.shift_kids_right(mid_key_position)
        papa.set_kid(new_kid, mid_key_position)
        self.save_tree(papa)
        self.save_tree(kid)
        self.save_tree(new_kid)
        return papa, kid, new_kid

    def split_leaf(self, papa, kid):
        """
        """
        keys_mid = int(math.floor(self._fanout / 2))
        new_kid = self.create_leaf()
        for i, k in enumerate(range(keys_mid, self._fanout)):  # copy up mid-key, preserve mid-key
            new_kid.set_key(kid.keys[k], i)
            new_kid.set_value(kid.values[k], i)
        mid_key = kid.keys[keys_mid]
        mid_key_position = papa.search_key_position(mid_key)
        for k in range(keys_mid, self._fanout):
            kid.remove_key(k)
            kid.remove_value(k)
        papa.insert_key(mid_key, mid_key_position)
        papa.shift_kids_right(mid_key_position)
        papa.set_kid(new_kid, mid_key_position)
        if kid.next:
            next_leaf = self.load_tree(kid.next_id, leaf=True)
            next_leaf.prev_id = new_kid.id
            self.save_tree(next_leaf)
        new_kid.prev = kid
        new_kid.prev_id = kid.id
        new_kid.next = kid.next
        new_kid.next_id = kid.next_id
        kid.next = new_kid
        kid.next_id = new_kid.id
        self.save_tree(papa)
        self.save_tree(kid)
        self.save_tree(new_kid)
        return papa, kid, new_kid

    def load(self, kvps):
        """
        Bulk insert.
        """
        pass

    def remove(self, key):
        """
        """
        pass

    def save_tree(self, tree):
        """
        """
        buffer = tree.serialize()
        offset = self.calculate_offset(tree.id)
        self._repository.write(offset, buffer)

    def load_tree(self, id, leaf=False):
        """
        """
        offset = self.calculate_offset(id)
        if leaf:
            size = Index.BTreeLeaf.calculate_size(self._fanout)
            buffer = self._repository.read(offset, size)
            header, keys_count, keys, values, prev_id, next_id = Index.BTreeLeaf.deserialize(buffer)
            result = Index.BTreeLeaf(id, Index.M)
            for k, key in enumerate(keys):
                result.set_key(key, k)
            for k, value in enumerate(values):
                result.set_value(value, k)
            result.prev_id = prev_id
            result.next_id = next_id
        else:
            size = Index.BTreeBranch.calculate_size(self._fanout)
            buffer = self._repository.read(offset, size)
            header, keys_count, keys, kids = Index.BTreeBranch.deserialize(buffer)
            result = Index.BTreeBranch(id, Index.M)
            for k, key in enumerate(keys):
                result.set_key(key, k)
            for k, kid in enumerate(kids):
                result.kid_ids[k] = kid
        return result

    @lru_cache
    def calculate_offset(self, id):
        """
        """
        offset = Index.HeaderSize
        offset += id * Index.BTreeBranch.calculate_size(self._fanout)
        return offset

    # @staticmethod
    # def search_key(key, keys, lo=0, hi=None):
    #     """
    #     """
    #     assert key is not None, "Key must be non None."
    #
    #     def binary_search(_key, _keys, _lo=0, _hi=None):
    #         result = -1
    #         if _hi is None:
    #             _hi = len(keys) - 1
    #         while _lo <= _hi:
    #             mid = (_hi + _lo) // 2
    #             cmp = Text.compare(_key, _keys[mid])
    #             if cmp > 0:
    #                 _lo = mid + 1
    #             elif cmp < 0:
    #                 _hi = mid - 1
    #             else:
    #                 result = mid
    #                 break
    #         return result
    #     return binary_search(key, keys, lo, hi)
    #
    # @staticmethod
    # def search_key_position(key, keys, lo=0, hi=None, desc=False):
    #     """
    #     """
    #     assert key is not None, "Key must be non None."
    #
    #     def locate(_key, _keys, _lo=0, _hi=None):
    #         if _hi is None:
    #             _hi = len(keys)
    #         while _lo < _hi:
    #             mid = (_hi + _lo) // 2
    #             if _keys[mid] is None:
    #                 cmp = -1 if desc else 1  # None is always less/bigger than key
    #             else:
    #                 cmp = Text.compare(_key, _keys[mid])
    #             if cmp < 0:
    #                 _hi = mid
    #             else:
    #                 _lo = mid + 1
    #         return _lo
    #     return locate(key, keys, lo, hi)

    # @staticmethod
    # def set_key(key, keys, lo=0, hi=None):
    #     """
    #     """
    #     position = Index.search_key_position(key, keys, lo, hi)
    #     assert position < len(keys), "Invalid position calculated."
    #     keys[position] = key
    #     return position

    # @staticmethod
    # def set_value(value, values, position):
    #     """
    #     """
    #     assert position < len(values), "Invalid position."
    #     values[position] = value
    #     return position

    # @staticmethod
    # def insert_key(key, keys, lo=0, hi=None):
    #     """
    #     Inserts key to the right of the found position (handles duplicates).
    #     hi should be _keys_count + 1, + 1 to include the next slot in keys.
    #     """
    #     if hi is None:
    #         hi = len(keys)
    #     position = Index.search_key_position(key, keys, lo, hi, desc=True)
    #     assert position < hi, "Invalid position calculated."
    #     for k in range(hi - 1, position, -1):
    #         keys[k] = keys[k - 1]
    #     keys[position] = key
    #     return keys, position
