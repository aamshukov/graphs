#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import os
import unittest
from graph.core.flags import Flags
from graph.core.logger import Logger
from graph.core.text import Text
from graph.core.domainhelper import DomainHelper
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
        DomainHelper.collect_by_category('Cf')


if __name__ == '__main__':
    """
    """
    unittest.main()
