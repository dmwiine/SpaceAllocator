import unittest
from app.staff import Staff


class TestStaff(unittest.TestCase):

    def test_staff_instance(self):
        bruce = Staff('Bruce')
        self.assertIsInstance(bruce, Staff, msg='The object should be an instance of the `Staff` class')

    #def test_staff_object_type(self):
        #bruce = Staff('Bruce')
        #self.assertTrue((type(bruce) is Staff), msg='The object should be a type of `Staff`')

    def test_staff_properties(self):
        donna = Staff('Donna')
        self.assertListEqual(['Donna', None],
                             [donna.name, donna.office],
                             msg='The staff name and office should be a property of the car')
