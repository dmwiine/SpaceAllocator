import unittest
from app.office import Office
from app.fellow import Fellow

class TestOffice(unittest.TestCase):

    def test_Office_instance(self):
        yellow = Office('Yellow')
        self.assertIsInstance(yellow, Office,
                              msg='The object should be an instance of the `Office` class')

    def test_office_properties(self):
        office = Office('Black')
        self.assertListEqual(['Black', 6],
                             [office.name, office.space_available],
                             msg='The name, space_available should be X and 6')

    def test_has_space_if_office_has_no_space(self):
        office = Office('Yellow')
        office.space_available = 0
        self.assertEqual(False, office.has_space(), msg='The office has_space should return False')

    def test_has_space_if_office_has_space(self):
        office = Office('Red')
        office.space_available = 4
        self.assertEqual(True, office.has_space(), msg='The office has_space should return True')

    def test_default_office_available_space(self):
        office = Office('Blue')
        self.assertEqual(6, office.space_available,
                         msg="The office default space_available should be 6")
