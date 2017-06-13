from app.person import Person
class Staff(Person):

    def __init__(self,name):
        Person.__init__(self, name, None)

