from app.person import Person
class Fellow(Person):

    def __init__(self, name):
        Person.__init__(self, name, None)
        self.living_space = None
        