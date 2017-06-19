from abc import ABCMeta, abstractmethod
class Person():
    __metaclass__ = ABCMeta

    def __init__(self, name, office = None):
        self.name = name
        self.office = office
