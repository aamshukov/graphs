#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import os
import struct
import unittest
from graph.core.flags import Flags
from graph.core.logger import Logger
from graph.core.text import Text
from graph.core.domain_helper import DomainHelper
from graph.core.value import Value
from graph.core.entity import Entity


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

    def __lt__(self, other):
        result = (super().__lt__(other) and
                  self._age < other.age)
        return result

    def __le__(self, other):
        result = (super().__le__(other) and
                  self._age <= other.age)
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

    def __lt__(self, other):
        result = super().__lt__(other)
        return result

    def __le__(self, other):
        result = super().__le__(other)
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

    def test_strings_compare_success(self):
        assert Text.compare('', '') == 0
        assert Text.compare('Rit\u0113', 'Rite\u0304') == 0
        assert Text.compare('', ' ') == -1
        assert Text.compare('(ノಠ益ಠ)ノ彡 ɹoʇıpƎ ʇxǝ⊥', '(ノಠ益ಠ)ノ彡 ɹoʇıpƎ ʇxǝ⊥') == 0
        assert Text.compare('သည် ဇော်ဂျီ နှင့် မြန်မာ ယူနီကုတ် တို့ကို အပြန်အလှန် ပြောင်းပေးနိုင်သည့်အပြင် အင်တာနက်မရှိချိန်တွင်လည်း '
                            'offline အသုံးပြုနိုင်တဲ့ converter တစ်',
                            'သည် ဇော်ဂျီ နှင့် မြန်မာ ယူနီကုတ် တို့ကို အပြန်အလှန် ပြောင်းပေးနိုင်သည့်အပြင် အင်တာနက်မရှိချိန်တွင်လည်း '
                            'offline အသုံးပြုနိုင်တဲ့ converter တစ်') == 0
        assert Text.compare('Я с детства хотел завести собаку', 'Я с детства хотел завести собаку') == 0
        assert Text.compare('Я c детства хотел завести собаку', 'Я с детства хотел завести собаку') == -1
        assert Text.compare('english text', 'english text') == 0
        assert Text.compare('山乇ㄥ匚ㄖ爪乇　ㄒㄖ　ㄒ卄乇　爪ㄖ丂ㄒ　匚ㄖ爪卩ㄥ乇ㄒ乇　ﾌ卂卩卂几乇丂乇',
                            '山乇ㄥ匚ㄖ爪乇　ㄒㄖ　ㄒ卄乇　爪ㄖ丂ㄒ　匚ㄖ爪卩ㄥ乇ㄒ乇　ﾌ卂卩卂几乇丂乇') == 0
        assert Text.compare('enGlisH texT', 'EngLish TeXt', case_insensitive=True) == 0
        assert Text.compare('Я с дЕТства хоТЕЛ зАВестИ Собаку',
                            'я с деТСтвА ХотЕЛ ЗАВЕСТИ СОБАКУ',
                            case_insensitive=True) == 0
        assert Text.compare('habit', 'hat') == -1
        assert Text.compare('bat', 'bail') == 1
        assert Text.compare('HELLO', 'Hello') == -1
        assert Text.compare('HELLO', 'Hello', case_insensitive=True) == 0

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

    def test_collect_by_category(self):
        Text.collect_by_category('Cf')

    def test_string_kind_success(self):
        kind = Text.get_string_kind('a')
        print(kind)
        # assert kind == Text.PyUnicodeObject.PyUnicode_2BYTE_KIND
        kind = Text.get_string_kind('Я')
        print(kind)
        # assert kind == Text.PyUnicodeObject.PyUnicode_2BYTE_KIND
        kind = Text.get_string_kind('爪')
        print(kind)
        # assert kind == Text.PyUnicodeObject.PyUnicode_2BYTE_KIND
        kind = Text.get_string_kind('🐍')
        print(kind)
        # assert kind == Text.PyUnicodeObject.PyUnicode_2BYTE_KIND
        kind = Text.get_string_kind('သည်')
        print(kind)
        # assert kind == Text.PyUnicodeObject.PyUnicode_2BYTE_KIND

    def test_serialize_string_success(self):
        string1 = 'Hdr'
        data = DomainHelper.serialize_string(string1)
        string2 = DomainHelper.deserialize_string(data)
        assert Text.equal(string1, string2)
        string1 = 'Long long text'
        data = DomainHelper.serialize_string(string1)
        string2 = DomainHelper.deserialize_string(data)
        assert Text.equal(string1, string2)

    @staticmethod
    def build_template(hdr, hdr_size, ptrs, keys, key_size):
        core_template = '<'  # little-endian
        core_template += f"{len(bytes(DomainHelper.pad_string(hdr, hdr_size), 'utf-8'))}s"
        core_template += f"{len(ptrs)}I"
        keys_template = '<'
        for key in keys:
            key = DomainHelper.pad_string(key, key_size)
            key_bytes = bytes(key, 'utf-8')
            keys_template += f"{len(key_bytes)}s"
        return core_template, keys_template

    def test_serialize_data_success(self):
        header = 'TreeHeader'
        header_size = 16
        pointers = [1, 2, 3, 4, 5, 6]
        keys = ['Key1', 'Key2', 'Key3', 'Key4', 'Key5']
        key_size = 16
        core_template, keys_template = Test.build_template(header, header_size, pointers, keys, key_size)
        core_size = struct.calcsize(core_template)
        full_size = core_size + struct.calcsize(keys_template)
        buffer = bytearray(full_size)
        struct.pack_into(core_template,
                         buffer,
                         0,
                         bytes(DomainHelper.pad_string(header, header_size), 'utf-8'),
                         *pointers)
        offset = core_size
        for key in keys:
            key = DomainHelper.pad_string(key, key_size)
            key_bytes = bytes(key, 'utf-8')
            key_template = f"{len(key_bytes)}s"
            struct.pack_into(key_template, buffer, offset, key_bytes)
            offset += len(key_bytes)
        core_data = struct.unpack_from(core_template, buffer, 0)
        header1, *pointers1 = core_data
        header1 = header1.decode('utf-8').strip()
        assert header == header1
        assert pointers == pointers1
        keys_data = struct.unpack_from(keys_template, buffer, core_size)
        keys1 = list()
        for key in keys_data:
            key = key.decode('utf-8').strip()
            keys1.append(key)
        assert keys == keys1


if __name__ == '__main__':
    """
    """
    unittest.main()
