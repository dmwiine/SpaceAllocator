from app.room import Room
class LivingSpace(Room):
    def __init__(self,name):
        Room.__init__(self, name)
        self.space_available = 4
        self.occupants = []


    def has_space(self):
        """ Method to check whether an office has available space """
        if self.space_available == 0:
            return False
        else:
            return True

    '''def add_person(self, fellow):
        if self.space_available > 0:
            fellow.living_space = self
            self.space_available -= 1
            self.occupants.append(fellow)
        return fellow

    def print_allocations(self):
        if len(self.occupants) > 0:
            print(self.name)
            print("-----------------------------------------------------")
            print(",".join(occupant.name for occupant in self.occupants).upper())
        else:
            print(self.name)
            print("-----------------------------------------------------")
            print("Room is empty")

    def print_allocations_to_file(self):
        file = open('./Files/allocations.txt', 'w')
        file.write('\n' + self.name + '\n')
        file.write("-----------------------------------------------------"'\n')
        file.write(",".join(occupant.name for occupant in self.occupants).upper()+'\n')'''
