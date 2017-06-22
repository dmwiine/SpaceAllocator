
import random
import string
from app.office import Office
from app.living_space import LivingSpace
from app.staff import Staff
from app.fellow import Fellow
from Models.models import engine
from sqlalchemy.orm import sessionmaker

from Models.models import OfficeModel, FellowModel, StaffModel, LivingSpaceModel


class Dojo():
    """This is the main Dojo class"""
    def __init__(self):
        self.all_offices = []
        self.all_living_spaces = []
        self.all_staff = []
        self.all_fellows = []
        self.available_offices = []
        self.available_living_spaces = []
        self.allocations = {}

    def room_exists(self, room_name):
        all_rooms = self.all_offices + self.all_living_spaces
        is_created = [room for room in all_rooms if room.name == room_name]
        if len(is_created) > 0:
            return True
        else:
            return False

    def fellow_exists(self, person_name):
        is_created = [person for person in self.all_fellows if person.name == person_name]
        if len(is_created) > 0:
            return True
        else:
            return False

    def staff_exists(self, person_name):
        is_created = [person for person in self.all_staff if person.name == person_name]
        if len(is_created) > 0:
            return True
        else:
            return False

    def create_room(self, room_type, name_list):
        """ This function creates new rooms which are either offices or living spaces"""

        if room_type != "" and name_list != []:
            for name in name_list:
                if isinstance(name, str) and name.isalpha():
                    if not self.room_exists(name.upper()):
                        if room_type == "office":
                            office = Office(name.upper())
                            self.all_offices.append(office)
                            self.available_offices.append(office)
                        elif room_type == "living_space":
                            living_space = LivingSpace(name.upper())
                            self.all_living_spaces.append(living_space)
                            self.available_living_spaces.append(living_space)
                        else:
                            raise ValueError("Ooops!, Room type should be either office or Living_space")
                    else:
                        raise ValueError("Ooops!, Room has already been created")
                else:
                    raise TypeError("Ooops!, Please enter a valid office name")
        else:
            raise ValueError()

    def add_fellow(self, name, wants_accomodation):
        """Function to add a fellow and allocate him/her a room"""
        if len(self.all_offices) == 0 and len(self.all_living_spaces) == 0:
            raise ValueError("Ooops!!!, Rooms must be created before a person is added")
        if not self.has_invalid_chars(name):
            if not self.fellow_exists(name):
                fellow = Fellow(name)
                available_office = self.get_available_office()
                if available_office:
                    if fellow.office is None:
                        fellow = self.add_person_to_office(fellow, available_office)
                if wants_accomodation == 'Y':
                    fellow.wants_accomodation = True
                    living_space = self.get_available_living_space()
                    if living_space:
                        if fellow.living_space is None:
                            fellow = self.add_fellow_to_living_space(fellow, living_space)
                self.all_fellows.append(fellow)
                self.update_available_offices()
                self.update_available_living_spaces()
                return fellow
            else:
                raise ValueError("Ooops!!, Person already exists in the system")
        else:
            raise ValueError("Ooops!!!, The person's name contains invalid characters. Try again!")

    def add_staff(self, name):
        """Function to add a staff and allocate him/her a room"""
        if not self.has_invalid_chars(name):
            if not self.staff_exists(name):
                staff = Staff(name)
                available_office = self.get_available_office()
                if available_office:
                    if staff.office is None:
                        staff = self.add_person_to_office(staff, available_office)
                self.all_staff.append(staff)
                self.update_available_offices()
                return staff
            else:
                raise ValueError("Ooops!!, Person already exists in the system")
        else:
            raise ValueError("Ooops!!!, Invalid person name")

    def add_person_to_office(self, person, office):
        """Function to add a person to a an office"""
        if office.space_available > 0:
            person.office = office
            office.space_available -= 1
            if office.name not in self.allocations.keys():
                self.allocations[office.name] = [person]
            else:
                if person not in self.allocations[office.name]:
                    self.allocations[office.name].append(person)
        return person

    def add_fellow_to_living_space(self, fellow, living_space):
        """Fuction to add a person to a living space"""
        if living_space.space_available > 0:
            fellow.living_space = living_space
            living_space.space_available -= 1
            if living_space.name not in self.allocations.keys():
                self.allocations[living_space.name] = [fellow]
            else:
                if fellow not in self.allocations[living_space.name]:
                    self.allocations[living_space.name].append(fellow)
            return fellow

    def get_available_living_space(self):
        """ This function randomizes the living_space selection"""

        if len(self.available_living_spaces) != 0:
            living_space = random.choice(self.available_living_spaces)
            return living_space
        else:
            return False

    def get_available_office(self):
        """This function randomizes the office selection"""

        if len(self.available_offices) != 0:
            office = random.choice(self.available_offices)
            return office
        else:
            return False

    def update_available_offices(self):
        """Function to check and update available offices"""

        for office in self.available_offices:
            if not office.has_space():
                self.available_offices.remove(office)
        return self.available_offices

    def update_available_living_spaces(self):
        """Function to check and update available living_spaces"""

        for living_space in self.available_living_spaces:
            if not living_space.has_space():
                self.available_living_spaces.remove(living_space)
        return self.available_living_spaces

    def print_room(self, name):
        """This function prints the occupants in a room"""
        if not self.room_exists(name):
            raise ValueError("Ooops!, Roomname does not exist in the system")
        print("**** Room " + name + " occupants ****")
        print()
        if self.allocations[name]:
            for person in self.allocations[name]:
                print(person.name)
        else:
            print("No people have been allocated to this room")

    def print_allocations(self):
        """Print rooms and their corresponding allocations"""
        for key, value in self.allocations.items():
            print()
            print(key)
            print("-----------------------------------------------------")
            print(",".join(occupant.name for occupant in value).upper())

    def print_allocations_to_a_file(self, filename):
        """Prints room allocations to a text file"""
        if not isinstance(filename, str):
            raise ValueError("Ooops!, Please enter a valid filename")

        file = open('./Files/' + filename, 'w')
        for key, value in self.allocations.items():
            file.write('\n' + key + '\n')
            file.write("-----------------------------------------------------"'\n')
            file.write(",".join(occupant.name for occupant in value).upper() + '\n')

    def print_unallocated(self):
        """Prints all the people who haven't been allocated rooms"""

        print("**** UnAllocated Fellows ****")
        count = 0
        for fellow in self.all_fellows:
            if fellow.living_space is None or fellow.office is None:
                print(fellow.name)
                count += 1
        if count == 0:
            print("None found")

        print()
        print("**** UnAllocated Staff ****")
        counter = 0
        for staff in self.all_staff:
            if staff.office is None:
                print(staff.name)
                counter += 1
        if counter == 0:
            print("None found")

    def print_unallocated_to_file(self, filename):
        """Prints all the people who haven't been allocated rooms to a text file"""
        if not isinstance(filename, str):
            raise ValueError("Ooops!, Please enter a valid filename")
        file = file = open('./Files/' + filename, 'w')
        file.write('\n'"**** UnAllocated Fellows ****"'\n')
        for fellow in self.all_fellows:
            if fellow.living_space is None or fellow.office is None:
                file.write(fellow.name + '\n')
        file.write('\n')
        file.write('\n'"**** UnAllocated Staff ****"'\n')
        for staff in self.all_staff:
            if staff.office is None:
                file.write(staff.name + '\n')


    def find_person(self, person_name):
        """Function to find a person object given their name"""

        all_people = self.all_fellows + self.all_staff
        for person in all_people:
            if person.name == person_name:
                return person
            #else:
                #return False

    def find_room(self, room_name):
        """Function to find a room object given room name"""

        all_rooms = self.all_offices + self.all_living_spaces
        for room in all_rooms:
            if room.name == room_name:
                return room
            #else:
                #return False

    def reallocate_person(self, person_name, room_name):
        """Function to reallocate a person to a new room"""

        person = self.find_person(person_name)
        room = self.find_room(room_name)
        #if person is False:
            #return "Person could not be found."
        #if room is False:
            #return "Room could not be found."

        if isinstance(room, LivingSpace) and room in self.available_living_spaces:
            old_living_space = person.living_space
            #print("ols space: {0} name: {1}".format(old_living_space.name, person.name))
            self.remove_person_from_room(old_living_space.name, person)
            self.add_fellow_to_living_space(person, room)
        elif isinstance(room, Office) and room in self.available_offices:
            old_office = person.office
            #print("old office: {0} name: {1}".format(old_office.name, person.name))
            self.remove_person_from_room(old_office.name, person)
            self.add_person_to_office(person, room)
        else:
            raise ValueError("Room selected has no available space")

    def remove_person_from_room(self, room_name, person):
        """ This function removes a person from their current room before
        they can be reallocated to a new room.
        """
        self.allocations[room_name].remove(person)
        old_room = self.find_room(room_name)
        old_room.space_available += 1

    def print_all_available_rooms(self):
        """Prints all the rooms that have available space"""

        print("**** Available Offices ****")
        for office in self.available_offices:
            print(office.name + " has " + str(office.space_available) + " available space(s).")
        print()
        print("**** Available Living Spaces ****")
        for living_space in self.available_living_spaces:
            print(living_space.name + " has " + str(living_space.space_available) + " available space(s).")

    def load_people(self, file_name):
        """Function to load people from a text file"""

        file = open(file_name, 'r')
        wants_accomodation = "N"

        for line in file.readlines():
            inputs = line.split()
            name = inputs[0] + " " + inputs[1]
            person_type = inputs[2]

            if len(inputs) == 4:
                wants_accomodation = inputs[3]
            if person_type == "FELLOW":
                self.add_fellow(name, wants_accomodation)
            elif person_type == "STAFF":
                self.add_staff(name)

    def save_state(self):
        """Function to save session data into the database"""

        # create a Session
        Session = sessionmaker(bind=engine)
        session = Session()

        session.query(OfficeModel).delete()
        session.query(LivingSpaceModel).delete()
        session.query(FellowModel).delete()
        session.query(StaffModel).delete()

        session.commit()

        # Create objects
        for living_space in self.all_living_spaces:
            living_space_model = LivingSpaceModel(living_space.name, living_space.space_available)
            session.add(living_space_model)

        for office in self.all_offices:
            office_model = OfficeModel(office.name, office.space_available)
            session.add(office_model)
        session.commit()

        for fellow in self.all_fellows:
            with session.no_autoflush:
                living_space = None
                office = None
                office_query = None
                space_query = None
                if fellow.living_space:
                    space_query = session.query(LivingSpaceModel).filter_by(
                        name=fellow.living_space.name).first()
                if fellow.office:
                    office_query = session.query(OfficeModel).filter_by(
                        name=fellow.office.name).first()
                if space_query:
                    living_space = space_query.living_space_id
                if office_query:
                    office = office_query.office_id
                fellow_model = FellowModel(living_space, office, fellow.name)
                session.add(fellow_model)

        for staff in self.all_staff:
            with session.no_autoflush:
                office = None
                office_query = None
                if staff.office:
                    office_query = session.query(OfficeModel).filter_by(
                        name=staff.office.name).first()
                if office_query:
                    office = office_query.office_id

                staff_model = StaffModel(office, staff.name)
                session.add(staff_model)

        # commit the record the database
        session.commit()

    def load_state(self):
        """Function to load data from the database"""

        Session = sessionmaker(bind=engine)
        session = Session()

        # Create objects
        for living_space in session.query(LivingSpaceModel).order_by(
                LivingSpaceModel.living_space_id):
            new_space = LivingSpace(living_space.name)
            new_space.space_available = living_space.spaces_available
            self.all_living_spaces.append(new_space)
            self.available_living_spaces.append(new_space)

        for office in session.query(OfficeModel).order_by(OfficeModel.office_id):
            new_office = Office(office.name)
            new_office.space_available = office.spaces_available
            self.all_offices.append(new_office)
            self.available_offices.append(new_office)

        for fellow in session.query(FellowModel).order_by(FellowModel.fellow_id):
            new_fellow = Fellow(fellow.name)
            if fellow.living_space:
                fellow_space = LivingSpace(fellow.living_space.name)
                fellow_space.space_available = fellow.living_space.spaces_available
                new_fellow.living_space = fellow_space

                if fellow_space.name not in self.allocations.keys():
                    self.allocations[fellow_space.name] = [new_fellow]
                else:
                    if new_fellow not in self.allocations[fellow_space.name]:
                        self.allocations[fellow_space.name].append(new_fellow)

            if fellow.office:
                office = Office(fellow.office.name)
                office.space_available = fellow.office.spaces_available
                new_fellow.office = office

                if office.name not in self.allocations.keys():
                    self.allocations[office.name] = [new_fellow]
                else:
                    if new_fellow not in self.allocations[office.name]:
                        self.allocations[office.name].append(new_fellow)

            self.all_fellows.append(new_fellow)

        for staff in session.query(StaffModel).order_by(StaffModel.staff_id):
            new_staff = Staff(staff.name)
            if staff.office:
                office = Office(staff.office.name)
                office.space_available = staff.office.spaces_available
                new_staff.office = office

                if office.name not in self.allocations.keys():
                    self.allocations[office.name] = [new_staff]
                else:
                    if new_staff not in self.allocations[office.name]:
                        self.allocations[office.name].append(new_staff)
            self.all_staff.append(new_staff)
    
    @staticmethod
    def has_invalid_chars(my_string):
        # Populate a list of invalid special characters
        integers = set(['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'])
        _chars = set(string.punctuation.replace("_", ""))
        invalid_chars = _chars | integers
        if any(char in invalid_chars for char in my_string):
            return True
        else:
            return False

