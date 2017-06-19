import unittest
import sqlite3
from app.dojo import Dojo
from app.fellow import Fellow
from app.staff import Staff
from app.office import Office
from app.living_space import LivingSpace

class TestDojo(unittest.TestCase):
    def setUp(self):
        self.dojo = Dojo()

    def test_creates_office_successfully(self):

        initial_office_count = len(self.dojo.all_offices)
        self.dojo.create_room("office",["Blue"])

        new_office_count = len(self.dojo.all_offices)
        self.assertEqual(new_office_count - initial_office_count, len(["Blue"]))

    def test_creates_living_space_successfully(self):
        initial_living_space_count = len(self.dojo.all_living_spaces)
        self.dojo.create_room("living_space",["Blue"])
        new_room_count = len(self.dojo.all_living_spaces)
        self.assertEqual(new_room_count - initial_living_space_count, 1)

    def test_add_fellow_successfully(self):
        self.dojo.create_room("office", ["Blue", "Green", "Pink"])
        self.dojo.create_room("living_space", ["A", "B", "C"])
        initial_fellow_count = len(self.dojo.all_fellows)
        fellow = self.dojo.add_fellow("Donna",'Y')
        self.assertTrue(fellow)
        new_fellow_count = len(self.dojo.all_fellows)
        self.assertEqual(new_fellow_count - initial_fellow_count, 1)

    def test_add_staff_successfully(self):
        initial_staff_count = len(self.dojo.all_staff)
        staff = self.dojo.add_staff("Donna")
        self.assertTrue(staff)
        new_staff_count = len(self.dojo.all_staff)
        self.assertEqual(new_staff_count - initial_staff_count, 1)

    def test_create_room_takes_only_string_parameters(self):
        self.assertRaises(TypeError, self.dojo.create_room, 1, [6])
        self.assertRaises(TypeError, self.dojo.create_room, 3.5, [0.87])

    def test_create_room_doesnt_take_empty__parameters(self):
        self.assertRaises(ValueError, self.dojo.create_room, "", [])
        self.assertRaises(ValueError, self.dojo.create_room, "Green", [])
        self.assertRaises(ValueError, self.dojo.create_room, "", ["office"])

    def test_fellow_is_assigned_an_office_if_offices_available(self):
        self.dojo.create_room("office", ["Red"])
        fellow = self.dojo.add_fellow("Daph", 'Y')
        self.assertIsNotNone(fellow.office, msg="Fellow should be assigned an office")

    def test_staff_is_assigned_an_office_if_offices_are_available(self):
        self.dojo.create_room("office", ["Purple"])
        staff = self.dojo.add_staff("Daph")
        self.assertIsNotNone(staff.office, msg="Fellow should be assigned an office")

    def test_fellow_is_not_assigned_living_space_if_not_specified(self):
        self.dojo.create_room("living_space",["X","Y","Z"])
        fellow = self.dojo.add_fellow("Daph", 'N')
        self.assertIsNone(fellow.living_space, msg="Fellow should not be assigned living space if N")

    def test_fellow_is_assigned_living_space_if_specified(self):
        self.dojo.create_room("living_space",["A","B","C"])
        fellow = self.dojo.add_fellow("Daph", 'Y')
        self.assertIsNotNone(fellow.living_space, msg="Fellow should be assigned an office")

    def test_fellow_is_not_assigned_living_space_if_no_living_space_is_available(self):
        self.dojo.create_room("office", ["Blue", "Green", "Pink"])
        self.dojo.create_room("living_space", ["A", "B", "C"])
        self.dojo.available_living_spaces = []
        fellow = self.dojo.add_fellow("Daph", 'Y')
        self.assertIsNone(fellow.living_space,
                          msg="Fellow should not be assigned living space if no living space is available")

    def test_staff_is_not_assigned_office_if_no_office_is_available(self):
        self.dojo.available_offices = []
        staff = self.dojo.add_staff("Daph")
        self.assertIsNone(staff.office, 
                          msg="Staff should not be assigned office if no office is available")

    def test_fellow_is_not_assigned_office_if_no_office_is_available(self):
        self.dojo.create_room("office", ["Blue", "Green", "Pink"])
        self.dojo.create_room("living_space", ["A", "B", "C"])
        self.dojo.available_offices = []
        fellow = self.dojo.add_fellow("Daph", "Y")
        self.assertIsNone(fellow.office,
                          msg="Fellow should not be assigned office if no office is available")

    def test_reallocate_person_successfully_reallocates_person(self):
        self.dojo.create_room("living_space", ["A"])
        fellow = self.dojo.add_fellow("Daph", 'Y')
        self.dojo.create_room("living_space", ["B"])
        fellow_room = fellow.living_space.name
        self.dojo.reallocate_person("Daph", "B")
        new_fellow_room = fellow.living_space.name
        self.assertNotEqual(new_fellow_room, fellow_room, msg="Person was not reallocated")

    def test_add_person_to_office(self):
        bruce = Fellow('Bruce')
        x = Office('X')
        self.dojo.add_person_to_office(bruce, x)
        self.assertListEqual(['X', 5], [x.name, x.space_available],
                             msg="The space available should have reduced")
        self.assertEqual(x, bruce.office, msg='The person office should be x')
        self.assertEqual([bruce], self.dojo.allocations[x.name])

    def test_add_person(self):
        bruce = Fellow('Bruce')
        x = LivingSpace('X')
        self.dojo.add_fellow_to_living_space(bruce, x)
        #x.add_person(bruce)
        self.assertListEqual(['X', 3],
                             [x.name, x.space_available],
                             msg='The space available should have reduced')
        self.assertEqual(x, bruce.living_space, msg='The person office should be x')
        self.assertEqual([bruce], self.dojo.allocations[x.name])

    def test_load_people(self):
        self.dojo.create_room("office", ["Blue", "Green", "Pink"])
        self.dojo.create_room("living_space", ["A", "B", "C"])
        self.dojo.load_people("inputs.txt")
        self.assertEqual(4, len(self.dojo.all_fellows), msg="All fellows must be 4")
        self.assertEqual(3, len(self.dojo.all_staff), msg="All staff must be 3")
        office_allocated = True
        staff_allocated = True
        living_allocated = True
        for fellow in self.dojo.all_fellows:
            if fellow.office is None:
                office_allocated = False
            if fellow.living_space is None:
                living_allocated = False
        for staff in self.dojo.all_staff:
            if staff.office is None:
                staff_allocated = False
        self.assertTrue(office_allocated, msg="All fellows should be allocated offices")
        self.assertTrue(living_allocated, msg="Fellows should have been allocated living spaces")
        self.assertTrue(staff_allocated, msg="All staff should be allocated offices")

    def test_print_allocations_to_file(self):
        self.dojo.create_room("office", ["Blue", "Green", "Pink"])
        self.dojo.create_room("living_space", ["A", "B", "C"])
        self.dojo.load_people("inputs.txt")

        self.dojo.print_allocations_to_a_file("allocations.txt")
        self.dojo.print_unallocated_to_file("unallocatted.txt")

        allocations_file = open("./Files/allocations.txt")
        self.assertTrue(allocations_file, msg="Should create an allocations.txt file")
        allocations_file.close()

        unallocated_file = open("./Files/unallocatted.txt")
        self.assertTrue(unallocated_file, msg="Should create an unallocated.txt file")
        unallocated_file.close()

    def test_save_state(self):
        self.dojo.create_room("office", ["Blue", "Green", "Pink"])
        self.dojo.create_room("living_space", ["A", "B", "C"])
        self.dojo.load_people("inputs.txt")

        self.dojo.save_state()
        self.assertTrue(sqlite3.connect('./dojo.db'), msg="Can't connect to saved db")

    def test_load_state(self):
        self.dojo_instance = Dojo()
        self.dojo_instance.create_room("office", ["Blue", "Green", "Pink"])
        self.dojo_instance.create_room("living_space", ["A", "B", "C"])
        self.dojo_instance.load_people("inputs.txt")
        self.dojo_instance.save_state()

        self.new_dojo_instance = Dojo()
        self.new_dojo_instance.load_state()

        self.assertEqual(len(self.new_dojo_instance.all_fellows), 4,
                         msg="Loaded fellows should be 4")
        self.assertEqual(len(self.new_dojo_instance.all_staff), 3, msg="Loaded staff should be 3")
        self.assertEqual(len(self.new_dojo_instance.all_living_spaces), 3,
                         msg="Living spaces loaded should be 3")
        self.assertEqual(len(self.new_dojo_instance.all_offices), 3,
                         msg="Offices loaded should be 3")




    