import unittest
from app.fellow import Fellow
from app.person import Person


class TestFellow(unittest.TestCase):

    def test_fellow_instance(self):
        bruce = Fellow('Bruce')
        self.assertIsInstance(bruce, Fellow, msg='The object should be an instance of the `Fellow` class')

    #def test_fellow_object_type(self):
       # bruce = Fellow('Bruce')
        #self.assertTrue((type(bruce) is Person), msg='The object should be a type of `Fellow`')

    def test_fellow_properties(self):
        donna = Fellow('Donna')
        self.assertListEqual(['Donna', None, None,False],
                             [donna.name, donna.office, donna.living_space, donna.wants_accomodation],
                             msg='The fellow name, office, living_space and wants_accomodation should be a property of the car')

    def test_default_fellow_wants_accomodation(self):
        donna = Fellow('Donna')
        self.assertEqual(False, donna.wants_accomodation,
                         msg="The car's wants_accomodatiion should be False by default")

