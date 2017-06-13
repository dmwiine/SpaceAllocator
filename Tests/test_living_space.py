import unittest
from app.living_space import LivingSpace
from app.fellow import Fellow


class TestLivingSpace(unittest.TestCase):

    def test_living_space_instance(self):
        yellow = LivingSpace('Yellow')
        self.assertIsInstance(yellow, LivingSpace, msg='The object should be an instance of the `LivingSpace` class')

    #def test_living_space_object_type(self):
        #yellow = LivingSpace('Yellow')
        #self.assertTrue((type(yellow) is LivingSpace), msg='The object should be a type of `LivingSpace`')

    def test_living_space_properties(self):
        x = LivingSpace('X')
        self.assertListEqual(['X', 4, []],
                             [x.name, x.space_available, x.occupants],
                             msg='The name, space_available and occupants should be properties of the LivingSpace')

    def test_has_space_if_living_space_has_no_space(self):
        x = LivingSpace('X')
        x.space_available = 0
        self.assertEqual(False, x.has_space(), msg='The living_space has_space should return False')

    def test_has_space_if_office_has_space(self):
        x = LivingSpace('X')
        x.space_available = 2
        self.assertEqual(True, x.has_space(), msg='The living_space has_space should return True')

    def test_default_available_living_space(self):
        x = LivingSpace('X')
        self.assertEqual(4, x.space_available,
                         msg="The living_space default space_available should be 4")