import unittest
from app.living_space import LivingSpace
from app.fellow import Fellow


class TestLivingSpace(unittest.TestCase):

    def test_living_space_instance(self):
        yellow = LivingSpace('Yellow')
        self.assertIsInstance(yellow, LivingSpace,
                              msg='The object should be an instance of the `LivingSpace` class')

    def test_living_space_properties(self):
        room = LivingSpace('Blue')
        self.assertListEqual(['Blue', 4],
                             [room.name, room.space_available],
                             msg='The name, space_available should be X and 4')

    def test_has_space_if_living_space_has_no_space(self):
        room = LivingSpace('Ruby')
        room.space_available = 0
        self.assertEqual(False, room.has_space(), msg='Should return False')

    def test_has_space_if_office_has_space(self):
        room = LivingSpace('Valhala')
        room.space_available = 2
        self.assertEqual(True, room.has_space(), msg='Should return True')

    def test_default_available_living_space(self):
        room = LivingSpace('Horgwarts')
        self.assertEqual(4, room.space_available,
                         msg="The living_space default space_available should be 4")
