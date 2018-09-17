from abc import ABCMeta, abstractmethod
class Person():
    __metaclass__ = ABCMeta

    def __init__(self, name, office = None, wants_accomodation=False ):
        self.name = name
        self.office = office
        self.wants_accomodation = wants_accomodation
