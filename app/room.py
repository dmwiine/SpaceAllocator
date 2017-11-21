from abc import ABCMeta, abstractmethod
class Room():
    __metaclass__ = ABCMeta

    def __init__(self,name):
        self.name = name
        self.space_available = 0


    def __has_space(self):
        """ Method to check whether a room has available space """
        if self.space_available == 0:
            return False
        else:
            return True

