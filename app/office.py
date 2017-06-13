from app.room import Room

class Office(Room):
    def __init__(self, name):
        Room.__init__(self, name)
        self.space_available = 6
        self.occupants = []


    def has_space(self):
        """ Method to check whether an office has available space """
        if self.space_available == 0:
            return False
        else:
            return True

    '''def add_person(self, person):
        if self.space_available > 0:
            person.office = self
            self.space_available -= 1
            self.occupants.append(person)
        return person

    def print_allocations(self):
        if len(self.occupants) > 0:
            print(self.name)
            print("-----------------------------------------------------")
            print(",".join(occupant.name for occupant in self.occupants).upper())
            print()
        else:
            print(self.name)
            print("-----------------------------------------------------")
            print("Room is empty")

    def print_allocations_to_file(self):
        file = open('./Files/allocations.txt', 'w')
        file.write('\n' + self.name + '\n')
        file.write("-----------------------------------------------------"'\n')
        file.write(",".join(occupant.name for occupant in self.occupants).upper()+'\n')'''
