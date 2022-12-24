#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import inspect
import os
import sys

sys.path.append(os.path.abspath('src/adt'))
sys.path.append(os.path.abspath('src/core'))
sys.path.append(os.path.abspath('src/patterns'))
sys.path.append(os.path.abspath('src/algorithms'))
sys.path.append(os.path.abspath('src'))
ss = os.path.abspath('src/core')
cd = os.getcwd()

from core.logger import Logger
from core.value import Value
from core.entity import Entity
from core.colors import Colors
from core.flags import Flags


class Person(Entity):
    def __init__(self, name, age, address, manager=None):
        super().__init__('2.1')
        self.name = name
        self.age = age
        self.manager = manager
        self.address = address

    @property    
    def get_name(self):
        return self.name

    @property    
    def get_age(self):
        return self.age

    @property    
    def get_manager(self):
        return self.manager

    @property    
    def get_address(self):
        return self.address

    def validate(self):
        pass


class Address(Value):
    __slots__ = 'street', 'city'

    def __init__(self, street, city):
        super().__init__('2.1')
        self.street = street
        self.city = city

    @property    
    def get_street(self):
        return self.street

    @property    
    def get_city(self):
        return self.city

    def validate(self):
        pass


"""
"""
def main(args):
    logger = Logger(path=r'd:\tmp')
    logger.debug('kuku')

    color = Colors.RED
    flags = Flags.CLEAR

    address = Address('Marine Drive', 'Oakville')
    address.validate()
    manager = Person('Arthur', 50, address)
    manager.validate()
    person = Person('Eric', 28, address, manager)
    manager.validate()

    equal_managers = manager == manager
    print(equal_managers)
    equal_persons = person == manager
    print(equal_persons)
    equal_persons = person == person
    print(equal_persons)

    try:
        pass
    except Exception as ex:
        print(ex)
    return 1


"""
"""
if __name__ == '__main__':
    main(sys.argv[1:])
    # buggy microsoft cannot fix the crap --- sys.exit(main(sys.argv[1:]))
